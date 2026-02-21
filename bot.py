"""AI Vazifa Bot - YANGILANGAN VERSIYA"""

import os
import json
import logging
import asyncio
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, ReplyKeyboardRemove, WebAppInfo
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ConversationHandler, filters
)
from telegram.constants import ParseMode, ChatMemberStatus

from config import (
    BOT_TOKEN, MANDATORY_CHANNEL_ID, MANDATORY_CHANNEL_LINK,
    ADMIN_IDS, PRESENTATION_PACKAGES, SLIDE_COUNT_OPTIONS,
    TEXT_WRITING_PRICE, BALANCE_PACKAGES, PAYMENT_CARD_NUMBER,
    PAYMENT_CARD_HOLDER, PRESENTATION_TEMPLATES
)
from database import (
    init_db, get_user, create_user, update_user_language,
    get_user_balance, deduct_balance, update_balance, increment_tasks,
    create_payment, get_pending_payments, approve_payment,
    reject_payment, get_all_users, get_all_users_count, get_stats
)
from texts import t
from ai_service import generate_presentation_with_template, generate_text

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# YANGI STATES
(LANG_SELECT, MAIN_MENU, 
 PRES_TOPIC, PRES_AUTHOR, PRES_LANGUAGE, PRES_PACKAGE, PRES_SLIDES, 
 PRES_TEMPLATE, PRES_SUMMARY, PRES_PLAN_CHOICE, 
 PRES_PLAN_1, PRES_PLAN_2, PRES_PLAN_3, PRES_CONFIRM,
 TEXT_TYPE, TEXT_TOPIC, 
 PAYMENT_PACKAGE, PAYMENT_RECEIPT,
 ADMIN_BROADCAST) = range(19)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Tillar
PRESENTATION_LANGUAGES = {
    "uz": {"name": "🇺🇿 O'zbek tili", "code": "uz"},
    "ru": {"name": "🇷🇺 Rus tili", "code": "ru"},
    "en": {"name": "🇬🇧 Ingliz tili", "code": "en"},
    "de": {"name": "🇩🇪 Nemis tili", "code": "de"},
    "tj": {"name": "🇹🇯 Tojik tili", "code": "tj"},
    "tr": {"name": "🇹🇷 Turk tili", "code": "tr"}
}


def get_user_lang(context) -> str:
    return context.user_data.get("language", "uz")


def format_sum(amount: int) -> str:
    return f"{amount:,}".replace(",", " ")


async def check_subscription(user_id: int, context) -> bool:
    try:
        member = await context.bot.get_chat_member(
            chat_id=MANDATORY_CHANNEL_ID, user_id=user_id
        )
        return member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ]
    except Exception as e:
        logger.warning(f"Obuna tekshirishda xatolik: {e}")
        return True


def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(t("btn_presentation", lang), callback_data="menu_presentation")],
        [InlineKeyboardButton(t("btn_text_writing", lang), callback_data="menu_text_writing")],
        [
            InlineKeyboardButton(t("btn_balance", lang), callback_data="menu_balance"),
            InlineKeyboardButton(t("btn_help", lang), callback_data="menu_help")
        ],
        [InlineKeyboardButton(t("btn_change_language", lang), callback_data="menu_change_lang")],
    ]
    return InlineKeyboardMarkup(keyboard)


def subscription_keyboard(lang: str) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(t("subscribe_button", lang), url=MANDATORY_CHANNEL_LINK)],
        [InlineKeyboardButton(t("check_subscription", lang), callback_data="check_sub")]
    ]
    return InlineKeyboardMarkup(keyboard)


def language_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang_uz"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def presentation_language_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Taqdimot tili tanlash - 6 ta til"""
    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 O'zbek", callback_data="preslang_uz"),
            InlineKeyboardButton("🇷🇺 Rus", callback_data="preslang_ru")
        ],
        [
            InlineKeyboardButton("🇬🇧 Ingliz", callback_data="preslang_en"),
            InlineKeyboardButton("🇩🇪 Nemis", callback_data="preslang_de")
        ],
        [
            InlineKeyboardButton("🇹🇯 Tojik", callback_data="preslang_tj"),
            InlineKeyboardButton("🇹🇷 Turk", callback_data="preslang_tr")
        ],
        [InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")]
    ]
    return InlineKeyboardMarkup(keyboard)


def slides_grid_keyboard(lang: str, package_key: str) -> InlineKeyboardMarkup:
    """Sahifalar soni tanlash - 6 dan 30 gacha"""
    keyboard = []
    row = []
    for count in range(6, 31, 2):
        price = SLIDE_COUNT_OPTIONS.get(count, {}).get(package_key, 3000)
        row.append(InlineKeyboardButton(
            f"{count} - {format_sum(price)}",
            callback_data=f"slides_{count}"
        ))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    
    if row:
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")])
    return InlineKeyboardMarkup(keyboard)


# ========== START ==========
async def start_command(update: Update, context) -> int:
    user = update.effective_user
    db_user = get_user(user.id)
    
    if not db_user:
        create_user(user.id, user.username, user.first_name)
        db_user = get_user(user.id)
    
    lang = db_user.get("language", "uz")
    context.user_data["language"] = lang
    
    subscribed = await check_subscription(user.id, context)
    if not subscribed:
        await update.message.reply_text(
            text=t("subscribe_channel", lang),
            reply_markup=subscription_keyboard(lang),
            parse_mode=ParseMode.HTML
        )
        return LANG_SELECT
    
    balance = get_user_balance(user.id)
    await update.message.reply_text(
        text=t("welcome_back", lang, balance=format_sum(balance)),
        reply_markup=main_menu_keyboard(lang),
        parse_mode=ParseMode.HTML
    )
    return MAIN_MENU


# ========== MENU CALLBACK ==========
async def menu_callback(update: Update, context) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(context)
    user_id = query.from_user.id
    data = query.data
    
    if data == "menu_presentation":
        # YANGI: Mavzu so'rash
        keyboard = [[InlineKeyboardButton(t("btn_cancel", lang), callback_data="menu_back")]]
        await query.edit_message_text(
            text=t("presentation_topic_input", lang),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )
        return PRES_TOPIC
    
    elif data == "menu_back":
        balance = get_user_balance(user_id)
        await query.edit_message_text(
            text=t("welcome_back", lang, balance=format_sum(balance)),
            reply_markup=main_menu_keyboard(lang)
        )
        return MAIN_MENU
    
    # ... boshqa menu handlerlar ...
    
    return MAIN_MENU


# ========== QADAM 1: Mavzu ==========
async def presentation_topic_received(update: Update, context) -> int:
    lang = get_user_lang(context)
    topic = update.message.text
    
    context.user_data["pres_topic"] = topic
    
    # QADAM 2: Ism-familya so'rash
    keyboard = [[InlineKeyboardButton(t("btn_cancel", lang), callback_data="menu_back")]]
    await update.message.reply_text(
        text=t("presentation_author_input", lang),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )
    return PRES_AUTHOR


# ========== QADAM 2: Ism-familya ==========
async def presentation_author_received(update: Update, context) -> int:
    lang = get_user_lang(context)
    author = update.message.text
    
    context.user_data["pres_author"] = author
    
    # QADAM 3: Til tanlash (6 ta)
    await update.message.reply_text(
        text=t("presentation_language_select", lang),
        reply_markup=presentation_language_keyboard(lang),
        parse_mode=ParseMode.HTML
    )
    return PRES_LANGUAGE


# ========== QADAM 3: Til tanlash ==========
async def presentation_language_selected(update: Update, context) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(context)
    data = query.data
    
    if data == "menu_back":
        user_id = query.from_user.id
        balance = get_user_balance(user_id)
        await query.edit_message_text(
            text=t("welcome_back", lang, balance=format_sum(balance)),
            reply_markup=main_menu_keyboard(lang)
        )
        return MAIN_MENU
    
    pres_lang = data.replace("preslang_", "")
    context.user_data["pres_language"] = pres_lang
    
    # QADAM 4: Paket tanlash
    keyboard = [
        [InlineKeyboardButton(t("btn_package_standard", lang), callback_data="pkg_standard")],
        [InlineKeyboardButton(t("btn_package_premium", lang), callback_data="pkg_premium")],
        [InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")]
    ]
    await query.edit_message_text(
        text=t("presentation_choose_package", lang),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )
    return PRES_PACKAGE


# ========== QADAM 4: Paket ==========
async def presentation_package_selected(update: Update, context) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(context)
    data = query.data
    
    if data == "menu_back":
        user_id = query.from_user.id
        balance = get_user_balance(user_id)
        await query.edit_message_text(
            text=t("welcome_back", lang, balance=format_sum(balance)),
            reply_markup=main_menu_keyboard(lang)
        )
        return MAIN_MENU
    
    package_key = data.replace("pkg_", "")
    context.user_data["pres_package"] = package_key
    
    # QADAM 5: Sahifalar soni
    await query.edit_message_text(
        text=t("presentation_choose_slides", lang),
        reply_markup=slides_grid_keyboard(lang, package_key),
        parse_mode=ParseMode.HTML
    )
    return PRES_SLIDES


# ========== QADAM 5: Sahifalar soni ==========
async def presentation_slides_selected(update: Update, context) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(context)
    user_id = query.from_user.id
    data = query.data
    
    if data == "menu_back":
        balance = get_user_balance(user_id)
        await query.edit_message_text(
            text=t("welcome_back", lang, balance=format_sum(balance)),
            reply_markup=main_menu_keyboard(lang)
        )
        return MAIN_MENU
    
    slides_count = int(data.replace("slides_", ""))
    package_key = context.user_data.get("pres_package", "standard")
    price = SLIDE_COUNT_OPTIONS.get(slides_count, {}).get(package_key, 3000)
    
    # Balans tekshirish
    balance = get_user_balance(user_id)
    if balance < price:
        keyboard = [[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")]]
        await query.edit_message_text(
            text=t("not_enough_balance", lang,
                   balance=format_sum(balance),
                   needed=format_sum(price)),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return MAIN_MENU
    
    context.user_data["pres_slides"] = slides_count
    context.user_data["pres_price"] = price
    
    # QADAM 6: Shablon tanlash - Mini App
    keyboard = [
        [InlineKeyboardButton(
            t("btn_choose_template", lang),
            web_app=WebAppInfo(url="https://nodiraka.github.io/bot-templates-miniapp/")
        )],
        [InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")]
    ]
    await query.edit_message_text(
        text=t("presentation_choose_template", lang),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )
    return PRES_TEMPLATE

# ========== QADAM 6a: Mini App dan shablon ==========
async def presentation_webapp_data(update: Update, context) -> int:
    """Mini App dan shablon ma'lumotini qabul qilish"""
    lang = get_user_lang(context)
    
    try:
        web_app_data = json.loads(update.effective_message.web_app_data.data)
        
        category = web_app_data.get("category", "")
        template_id = web_app_data.get("id", 1)
        
        context.user_data["pres_template_category"] = category
        context.user_data["pres_template_id"] = template_id
        
        # QADAM 7: XULOSA ko'rsatish
        topic = context.user_data.get("pres_topic", "")
        author = context.user_data.get("pres_author", "")
        pres_lang = context.user_data.get("pres_language", "uz")
        package_key = context.user_data.get("pres_package", "standard")
        slides_count = context.user_data.get("pres_slides", 10)
        price = context.user_data.get("pres_price", 10000)
        
        # Til nomi
        lang_name = PRESENTATION_LANGUAGES.get(pres_lang, {}).get("name", "O'zbek")
        
        # Paket nomi
        package_info = PRESENTATION_PACKAGES.get(package_key, {})
        package_name = package_info.get(f"name_{lang}", package_info.get("name_uz", ""))
        
        # JAMI sahifalar = n + 3
        total_slides = slides_count + 3
        
        # Xulosa matn
        summary_text = t("presentation_summary_new", lang,
                        topic=topic,
                        author=author,
                        language_name=lang_name,
                        package=package_name,
                        slides=slides_count,
                        total_slides=total_slides,
                        price=format_sum(price))
        
        keyboard = [
            [InlineKeyboardButton(t("btn_plan_manual", lang), callback_data="plan_manual")],
            [InlineKeyboardButton(t("btn_plan_auto", lang), callback_data="plan_auto")],
            [InlineKeyboardButton(t("btn_cancel", lang), callback_data="menu_back")]
        ]
        
        await update.message.reply_text(
            text=summary_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )
        return PRES_SUMMARY
        
    except Exception as e:
        logger.error(f"WebApp data error: {e}")
        keyboard = [[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")]]
        await update.message.reply_text(
            text="❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return MAIN_MENU


# ========== QADAM 7: XULOSA - Reja yoki Avtomatik ==========
async def presentation_summary_choice(update: Update, context) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(context)
    data = query.data
    
    if data == "menu_back":
        user_id = query.from_user.id
        balance = get_user_balance(user_id)
        await query.edit_message_text(
            text=t("welcome_back", lang, balance=format_sum(balance)),
            reply_markup=main_menu_keyboard(lang)
        )
        return MAIN_MENU
    
    if data == "plan_manual":
        # REJA KIRITISH - 1-rejani so'rash
        context.user_data["plan_mode"] = "manual"
        keyboard = [[InlineKeyboardButton(t("btn_cancel", lang), callback_data="menu_back")]]
        await query.edit_message_text(
            text=t("presentation_plan_1", lang),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )
        return PRES_PLAN_1
    
    elif data == "plan_auto":
        # AVTOMATIK - darhol yaratish
        context.user_data["plan_mode"] = "auto"
        context.user_data["plan_1"] = None
        context.user_data["plan_2"] = None
        context.user_data["plan_3"] = None
        
        # Yaratishni boshlash
        await start_presentation_creation(query, context)
        return PRES_CONFIRM


# ========== QADAM 8: 1-REJA ==========
async def presentation_plan_1_received(update: Update, context) -> int:
    lang = get_user_lang(context)
    plan_1 = update.message.text
    
    context.user_data["plan_1"] = plan_1
    
    # 2-rejani so'rash
    keyboard = [[InlineKeyboardButton(t("btn_cancel", lang), callback_data="menu_back")]]
    await update.message.reply_text(
        text=t("presentation_plan_2", lang),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )
    return PRES_PLAN_2


# ========== QADAM 9: 2-REJA ==========
async def presentation_plan_2_received(update: Update, context) -> int:
    lang = get_user_lang(context)
    plan_2 = update.message.text
    
    context.user_data["plan_2"] = plan_2
    
    # 3-rejani so'rash
    keyboard = [[InlineKeyboardButton(t("btn_cancel", lang), callback_data="menu_back")]]
    await update.message.reply_text(
        text=t("presentation_plan_3", lang),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )
    return PRES_PLAN_3


# ========== QADAM 10: 3-REJA ==========
async def presentation_plan_3_received(update: Update, context) -> int:
    lang = get_user_lang(context)
    plan_3 = update.message.text
    
    context.user_data["plan_3"] = plan_3
    
    # Yaratishni boshlash
    await start_presentation_creation_message(update.message, context)
    return PRES_CONFIRM


# ========== YARATISH BOSHLASH ==========
async def start_presentation_creation(query, context):
    """Callback query orqali yaratish"""
    lang = get_user_lang(context)
    user_id = query.from_user.id
    
    # Ma'lumotlarni yig'ish
    topic = context.user_data.get("pres_topic")
    author = context.user_data.get("pres_author")
    pres_lang = context.user_data.get("pres_language", "uz")
    slides_count = context.user_data.get("pres_slides")
    price = context.user_data.get("pres_price")
    package_key = context.user_data.get("pres_package", "standard")
    template_category = context.user_data.get("pres_template_category")
    template_id = context.user_data.get("pres_template_id")
    plan_mode = context.user_data.get("plan_mode", "auto")
    plan_1 = context.user_data.get("plan_1")
    plan_2 = context.user_data.get("plan_2")
    plan_3 = context.user_data.get("plan_3")
    
    has_ai_images = (package_key == "premium")
    
    # Balansni ayirish
    deduct_balance(user_id, price)
    
    # Progress statusini ko'rsatish
    status_msg = await query.edit_message_text(
        text=f"🔄 {t('progress_content', lang)}\n\n[░░░░] 1/4",
        parse_mode=ParseMode.HTML
    )
    
    progress_steps = {
        1: t("progress_content", lang),
        2: t("progress_template", lang),
        3: t("progress_design", lang),
        4: t("progress_done", lang)
    }
    
    async def progress_callback(step: int, status: str):
        try:
            emoji = "🔄" if step < 4 else "✅"
            text = progress_steps.get(step, "")
            filled = step
            total = 4
            bar = "█" * filled + "░" * (total - filled)
            progress_text = f"{emoji} {text}\n\n[{bar}] {step}/{total}"
            await status_msg.edit_text(progress_text, parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.warning(f"Progress yangilashda xatolik: {e}")
    
    try:
        # AI bilan taqdimot yaratish
        file_path = await generate_presentation_with_template(
            topic=topic,
            author=author,
            slides_count=slides_count,
            language=pres_lang,
            output_dir=OUTPUT_DIR,
            template_category=template_category,
            template_id=template_id,
            has_ai_images=has_ai_images,
            progress_callback=progress_callback,
            plan_mode=plan_mode,
            plan_1=plan_1,
            plan_2=plan_2,
            plan_3=plan_3
        )
        
        # Tayyor
        try:
            await status_msg.edit_text(
                text=f"✅ {progress_steps[4]}\n\n[████] 4/4",
                parse_mode=ParseMode.HTML
            )
        except:
            pass
        
        # Faylni yuborish
        with open(file_path, "rb") as f:
            await context.bot.send_document(
                chat_id=user_id,
                document=f,
                filename=os.path.basename(file_path),
                caption=t("presentation_ready", lang)
            )
        
        increment_tasks(user_id)
        
        try:
            os.remove(file_path)
        except:
            pass
        
    except Exception as e:
        logger.error(f"Taqdimot yaratishda xatolik: {e}")
        await status_msg.edit_text(
            text=t("presentation_error", lang),
            parse_mode=ParseMode.HTML
        )


async def start_presentation_creation_message(message, context):
    """Message orqali yaratish"""
    lang = get_user_lang(context)
    user_id = message.from_user.id
    
    # Ma'lumotlarni yig'ish
    topic = context.user_data.get("pres_topic")
    author = context.user_data.get("pres_author")
    pres_lang = context.user_data.get("pres_language", "uz")
    slides_count = context.user_data.get("pres_slides")
    price = context.user_data.get("pres_price")
    package_key = context.user_data.get("pres_package", "standard")
    template_category = context.user_data.get("pres_template_category")
    template_id = context.user_data.get("pres_template_id")
    plan_mode = context.user_data.get("plan_mode", "manual")
    plan_1 = context.user_data.get("plan_1")
    plan_2 = context.user_data.get("plan_2")
    plan_3 = context.user_data.get("plan_3")
    
    has_ai_images = (package_key == "premium")
    
    # Balansni ayirish
    deduct_balance(user_id, price)
    
    # Progress statusini ko'rsatish
    status_msg = await message.reply_text(
        text=f"🔄 {t('progress_content', lang)}\n\n[░░░░] 1/4",
        parse_mode=ParseMode.HTML
    )
    
    progress_steps = {
        1: t("progress_content", lang),
        2: t("progress_template", lang),
        3: t("progress_design", lang),
        4: t("progress_done", lang)
    }
    
    async def progress_callback(step: int, status: str):
        try:
            emoji = "🔄" if step < 4 else "✅"
            text = progress_steps.get(step, "")
            filled = step
            total = 4
            bar = "█" * filled + "░" * (total - filled)
            progress_text = f"{emoji} {text}\n\n[{bar}] {step}/{total}"
            await status_msg.edit_text(progress_text, parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.warning(f"Progress yangilashda xatolik: {e}")
    
    try:
        # AI bilan taqdimot yaratish
        file_path = await generate_presentation_with_template(
            topic=topic,
            author=author,
            slides_count=slides_count,
            language=pres_lang,
            output_dir=OUTPUT_DIR,
            template_category=template_category,
            template_id=template_id,
            has_ai_images=has_ai_images,
            progress_callback=progress_callback,
            plan_mode=plan_mode,
            plan_1=plan_1,
            plan_2=plan_2,
            plan_3=plan_3
        )
        
        # Tayyor
        try:
            await status_msg.edit_text(
                text=f"✅ {progress_steps[4]}\n\n[████] 4/4",
                parse_mode=ParseMode.HTML
            )
        except:
            pass
        
        # Faylni yuborish
        with open(file_path, "rb") as f:
            await context.bot.send_document(
                chat_id=user_id,
                document=f,
                filename=os.path.basename(file_path),
                caption=t("presentation_ready", lang)
            )
        
        increment_tasks(user_id)
        
        try:
            os.remove(file_path)
        except:
            pass
        
    except Exception as e:
        logger.error(f"Taqdimot yaratishda xatolik: {e}")
        await status_msg.edit_text(
            text=t("presentation_error", lang),
            parse_mode=ParseMode.HTML
        )


async def handle_back_button(update: Update, context) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(context)
    user_id = query.from_user.id
    balance = get_user_balance(user_id)
    await query.edit_message_text(
        text=t("welcome_back", lang, balance=format_sum(balance)),
        reply_markup=main_menu_keyboard(lang)
    )
    return MAIN_MENU


async def cancel(update: Update, context) -> int:
    lang = get_user_lang(context)
    await update.message.reply_text(t("cancel_message", lang))
    return ConversationHandler.END

echo "✅ Bot.py qism 2 yaratildi (Shablon, Xulosa, Reja, Yaratish)"


# ========== ADMIN VA BOSHQA FUNKTSIYALAR ==========
# (Eski koddan ko'chirish - Admin, Payment, Text Writing)
# Bu qismni qisqartiramiz, chunki asosiy vazifa Presentation

async def admin_command(update: Update, context) -> int:
    # ... eski admin kod ...
    pass

async def buy_command(update: Update, context) -> int:
    # ... eski buy kod ...
    pass

# ========== MAIN ==========
def main():
    init_db()
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start_command),
        ],
        states={
            LANG_SELECT: [
                CallbackQueryHandler(lambda u, c: start_command(u, c), pattern="^check_sub$"),
            ],
            MAIN_MENU: [
                CallbackQueryHandler(menu_callback, pattern="^menu_"),
            ],
            PRES_TOPIC: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, presentation_topic_received),
                CallbackQueryHandler(handle_back_button, pattern="^menu_back$"),
            ],
            PRES_AUTHOR: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, presentation_author_received),
                CallbackQueryHandler(handle_back_button, pattern="^menu_back$"),
            ],
            PRES_LANGUAGE: [
                CallbackQueryHandler(presentation_language_selected, pattern="^(preslang_|menu_back)"),
            ],
            PRES_PACKAGE: [
                CallbackQueryHandler(presentation_package_selected, pattern="^(pkg_|menu_back)"),
            ],
            PRES_SLIDES: [
                CallbackQueryHandler(presentation_slides_selected, pattern="^(slides_|menu_back)"),
            ],
            PRES_TEMPLATE: [
                MessageHandler(filters.StatusUpdate.WEB_APP_DATA, presentation_webapp_data),
                CallbackQueryHandler(handle_back_button, pattern="^menu_back$"),
            ],
            PRES_SUMMARY: [
                CallbackQueryHandler(presentation_summary_choice, pattern="^(plan_|menu_back)"),
            ],
            PRES_PLAN_1: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, presentation_plan_1_received),
                CallbackQueryHandler(handle_back_button, pattern="^menu_back$"),
            ],
            PRES_PLAN_2: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, presentation_plan_2_received),
                CallbackQueryHandler(handle_back_button, pattern="^menu_back$"),
            ],
            PRES_PLAN_3: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, presentation_plan_3_received),
                CallbackQueryHandler(handle_back_button, pattern="^menu_back$"),
            ],
            PRES_CONFIRM: [
                # Empty state - faqat yaratish jarayoni
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("start", start_command),
        ],
        allow_reentry=True,
    )
    
    app.add_handler(conv_handler)
    
    logger.info("✅ YANGI BOT ISHGA TUSHDI!")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
