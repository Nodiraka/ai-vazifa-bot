"""AI Vazifa Bot - @aislidebot uslubida professional bot"""

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
from ai_service import generate_presentation, generate_text

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
(LANG_SELECT, MAIN_MENU, PRES_PACKAGE, PRES_SLIDES, PRES_TEMPLATE, PRES_TOPIC,
 PRES_CONFIRM, TEXT_TYPE, TEXT_TOPIC, PAYMENT_PACKAGE, PAYMENT_RECEIPT,
 ADMIN_BROADCAST) = range(12)

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


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


def slides_grid_keyboard(lang: str, package_key: str) -> InlineKeyboardMarkup:
    """@aislidebot uslubida 6-30 gacha grid tugmalar"""
    keyboard = []
    row = []
    for i in range(6, 31):
        row.append(InlineKeyboardButton(str(i), callback_data=f"slides_{i}"))
        if len(row) == 5:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton(t("btn_cancel", lang), callback_data="menu_back")])
    return InlineKeyboardMarkup(keyboard)


def template_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Dizayn tanlash tugmalari - @aislidebot uslubida"""
    templates = list(PRESENTATION_TEMPLATES.items())
    keyboard = []
    for i in range(0, len(templates), 2):
        row = []
        key1, tmpl1 = templates[i]
        row.append(InlineKeyboardButton(
            tmpl1.get(f"name_{lang}", tmpl1["name_uz"]),
            callback_data=f"tmpl_{key1}"
        ))
        if i + 1 < len(templates):
            key2, tmpl2 = templates[i + 1]
            row.append(InlineKeyboardButton(
                tmpl2.get(f"name_{lang}", tmpl2["name_uz"]),
                callback_data=f"tmpl_{key2}"
            ))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")])
    return InlineKeyboardMarkup(keyboard)


# ===== /start =====
async def start_command(update: Update, context) -> int:
    user = update.effective_user
    existing_user = get_user(user.id)
    if not existing_user:
        create_user(user.id, user.username or "", user.full_name or "")
        context.user_data["is_new"] = True
    else:
        context.user_data["is_new"] = False
        context.user_data["language"] = existing_user["language"]

    await update.message.reply_text(
        "🌐 Tilni tanlang / Выберите язык / Choose language:",
        reply_markup=language_keyboard()
    )
    return LANG_SELECT


async def language_selected(update: Update, context) -> int:
    query = update.callback_query
    await query.answer()
    lang_code = query.data.replace("lang_", "")
    context.user_data["language"] = lang_code
    user_id = query.from_user.id
    update_user_language(user_id, lang_code)

    is_subscribed = await check_subscription(user_id, context)
    if not is_subscribed:
        await query.edit_message_text(
            text=t("subscribe_channel", lang_code),
            reply_markup=subscription_keyboard(lang_code)
        )
        return LANG_SELECT

    return await show_main_menu(query, context)


async def check_sub_callback(update: Update, context) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(context)
    user_id = query.from_user.id

    is_subscribed = await check_subscription(user_id, context)
    if not is_subscribed:
        await query.answer(t("not_subscribed", lang), show_alert=True)
        return LANG_SELECT

    return await show_main_menu(query, context)


async def show_main_menu(query, context) -> int:
    lang = get_user_lang(context)
    user_id = query.from_user.id
    balance = get_user_balance(user_id)
    is_new = context.user_data.get("is_new", False)

    if is_new:
        text = t("welcome", lang, balance=format_sum(balance))
        context.user_data["is_new"] = False
    else:
        text = t("welcome_back", lang, balance=format_sum(balance))

    await query.edit_message_text(
        text=text,
        reply_markup=main_menu_keyboard(lang)
    )
    return MAIN_MENU


# ===== Menyu callback =====
async def menu_callback(update: Update, context) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(context)
    user_id = query.from_user.id
    data = query.data

    if data == "menu_presentation":
        # 1-qadam: Paket tanlash (Oddiy / Premium)
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

    elif data == "menu_text_writing":
        balance = get_user_balance(user_id)
        if balance < TEXT_WRITING_PRICE:
            keyboard = [[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")]]
            await query.edit_message_text(
                text=t("not_enough_balance", lang,
                       balance=format_sum(balance),
                       needed=format_sum(TEXT_WRITING_PRICE)),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return MAIN_MENU

        keyboard = [
            [
                InlineKeyboardButton(t("btn_essay", lang), callback_data="text_essay"),
                InlineKeyboardButton(t("btn_article", lang), callback_data="text_article"),
            ],
            [InlineKeyboardButton(t("btn_report", lang), callback_data="text_report")],
            [InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")]
        ]
        await query.edit_message_text(
            text=t("text_type_select", lang),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return TEXT_TYPE

    elif data == "menu_balance":
        balance = get_user_balance(user_id)
        keyboard = [[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")]]
        await query.edit_message_text(
            text=t("balance_info", lang,
                   balance=format_sum(balance),
                   text_price=format_sum(TEXT_WRITING_PRICE)),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )
        return MAIN_MENU

    elif data == "menu_change_lang":
        await query.edit_message_text(
            text="🌐 Tilni tanlang / Выберите язык / Choose language:",
            reply_markup=language_keyboard()
        )
        return LANG_SELECT

    elif data == "menu_help":
        keyboard = [[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")]]
        await query.edit_message_text(
            text=t("help_text", lang),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )
        return MAIN_MENU

    elif data == "menu_back":
        balance = get_user_balance(user_id)
        await query.edit_message_text(
            text=t("welcome_back", lang, balance=format_sum(balance)),
            reply_markup=main_menu_keyboard(lang)
        )
        return MAIN_MENU

    return MAIN_MENU


# ===== Taqdimot - 1-qadam: Paket tanlash =====
async def presentation_package_selected(update: Update, context) -> int:
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

    package_key = data.replace("pkg_", "")
    context.user_data["pres_package"] = package_key

    # 2-qadam: Slaydlar soni tanlash (6-30 grid)
    await query.edit_message_text(
        text=t("presentation_choose_slides", lang),
        reply_markup=slides_grid_keyboard(lang, package_key),
        parse_mode=ParseMode.HTML
    )
    return PRES_SLIDES


# ===== Taqdimot - 2-qadam: Sahifalar soni =====
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

    # 3-qadam: Dizayn tanlash - Mini App orqali
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


# ===== Taqdimot - 3a-qadam: Mini App dan shablon ma'lumotini qabul qilish =====
async def presentation_webapp_data(update: Update, context) -> int:
    """Mini App dan shablon tanlash ma'lumotini qabul qilish"""
    lang = get_user_lang(context)
    user_id = update.effective_user.id
    
    try:
        # Mini App dan kelgan ma'lumot
        web_app_data = json.loads(update.effective_message.web_app_data.data)
        
        # {"category": "1_biznes_moliya", "id": 3}
        category = web_app_data.get("category", "")
        template_id = web_app_data.get("id", 1)
        
        # Template key yaratish
        template_key = f"{category}_{template_id}"
        context.user_data["pres_template"] = template_key
        context.user_data["pres_template_category"] = category
        context.user_data["pres_template_id"] = template_id
        
        # 4-qadam: Mavzu yozish
        keyboard = [[InlineKeyboardButton(t("btn_cancel", lang), callback_data="menu_back")]]
        await update.message.reply_text(
            text=t("presentation_topic", lang),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )
        return PRES_TOPIC
        
    except Exception as e:
        logger.error(f"WebApp data error: {e}")
        keyboard = [[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")]]
        await update.message.reply_text(
            text="❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return MAIN_MENU


# ===== Taqdimot - 3-qadam: Dizayn tanlash =====
async def presentation_template_selected(update: Update, context) -> int:
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

    template_key = data.replace("tmpl_", "")
    context.user_data["pres_template"] = template_key

    # 4-qadam: Mavzu yozish
    keyboard = [[InlineKeyboardButton(t("btn_cancel", lang), callback_data="menu_back")]]
    await query.edit_message_text(
        text=t("presentation_topic", lang),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )
    return PRES_TOPIC


# ===== Taqdimot - 4-qadam: Mavzu kiritish va xulosa ko'rsatish =====
async def presentation_topic_received(update: Update, context) -> int:
    lang = get_user_lang(context)
    user_id = update.effective_user.id
    topic = update.message.text

    context.user_data["pres_topic"] = topic

    package_key = context.user_data.get("pres_package", "standard")
    slides_count = context.user_data.get("pres_slides", 10)
    price = context.user_data.get("pres_price", 3000)
    template_key = context.user_data.get("pres_template", "business")

    # Paket nomi
    package_info = PRESENTATION_PACKAGES.get(package_key, {})
    package_name = package_info.get(f"name_{lang}", package_info.get("name_uz", ""))

    # Shablon nomi
    template_info = PRESENTATION_TEMPLATES.get(template_key, {})
    template_name = template_info.get(f"name_{lang}", template_info.get("name_uz", template_key))

    # Til nomi
    lang_names = {"uz": "🇺🇿 O'zbekcha", "ru": "🇷🇺 Русский", "en": "🇬🇧 English"}
    lang_name = lang_names.get(lang, "O'zbekcha")

    # Xulosa ko'rsatish
    keyboard = [
        [InlineKeyboardButton(t("btn_create", lang), callback_data="pres_create")],
        [InlineKeyboardButton(t("btn_cancel", lang), callback_data="menu_back")]
    ]

    await update.message.reply_text(
        text=t("presentation_summary", lang,
               topic=topic,
               package=package_name,
               template=template_name,
               slides=slides_count,
               lang_name=lang_name,
               price=format_sum(price)),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )
    return PRES_CONFIRM


# ===== Taqdimot - 5-qadam: Tasdiqlash va yaratish =====
async def presentation_confirm(update: Update, context) -> int:
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

    # Ma'lumotlarni olish
    topic = context.user_data.get("pres_topic", "")
    package_key = context.user_data.get("pres_package", "standard")
    slides_count = context.user_data.get("pres_slides", 10)
    price = context.user_data.get("pres_price", 3000)
    template_key = context.user_data.get("pres_template", "business")

    package_info = PRESENTATION_PACKAGES.get(package_key, {})
    has_ai_images = package_info.get("has_ai_images", False)

    template_info = PRESENTATION_TEMPLATES.get(template_key, {})
    template_name = template_info.get(f"name_{lang}", template_info.get("name_uz", template_key))

    # Balansdan yechish
    if not deduct_balance(user_id, price):
        balance = get_user_balance(user_id)
        keyboard = [[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")]]
        await query.edit_message_text(
            text=t("not_enough_balance", lang,
                   balance=format_sum(balance),
                   needed=format_sum(price)),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return MAIN_MENU

    # Progress ko'rsatish
    progress_steps = {
        1: t("progress_step1", lang),
        2: t("progress_step2", lang),
        3: t("progress_step3", lang),
        4: t("progress_step4", lang),
    }

    progress_emojis = {
        1: "📝",
        2: "🖼",
        3: "🎨",
        4: "✅",
    }

    await query.edit_message_text(
        text=f"{progress_emojis[1]} {progress_steps[1]}",
        parse_mode=ParseMode.HTML
    )

    status_msg = query.message

    async def progress_callback(step: int, step_type: str):
        """Progress yangilash callback"""
        try:
            emoji = progress_emojis.get(step, "⏳")
            text = progress_steps.get(step, "...")
            # Progress bar
            filled = step
            total = 4
            bar = "█" * filled + "░" * (total - filled)
            progress_text = f"{emoji} {text}\n\n[{bar}] {step}/{total}"
            await status_msg.edit_text(progress_text, parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.warning(f"Progress yangilashda xatolik: {e}")

    try:
        # Template ma'lumotlarini olish
        template_category = context.user_data.get("pres_template_category")
        template_id = context.user_data.get("pres_template_id")
        
        # Agar template tanlangan bo'lsa - template asosida yaratish
        if template_category and template_id:
            from ai_service import generate_presentation_with_template
            file_path = await generate_presentation_with_template(
                topic, slides_count, lang, OUTPUT_DIR,
                template_category=template_category,
                template_id=template_id,
                has_ai_images=has_ai_images,
                progress_callback=progress_callback
            )
        else:
            # Eski usul - scratch dan yaratish
            file_path = await generate_presentation(
                topic, slides_count, lang, OUTPUT_DIR,
                template_key=template_key,
                has_ai_images=has_ai_images,
                progress_callback=progress_callback
            )

        # Tayyor
        try:
            await status_msg.edit_text(
                text=f"✅ {progress_steps[4]}\n\n[████] 4/4",
                parse_mode=ParseMode.HTML
            )
        except:
            pass

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
        update_balance(user_id, price)
        try:
            await status_msg.edit_text(t("error_ai", lang))
        except:
            await context.bot.send_message(chat_id=user_id, text=t("error_ai", lang))

    balance = get_user_balance(user_id)
    await context.bot.send_message(
        chat_id=user_id,
        text=t("welcome_back", lang, balance=format_sum(balance)),
        reply_markup=main_menu_keyboard(lang)
    )
    return MAIN_MENU


# ===== Matn yozish =====
async def text_type_selected(update: Update, context) -> int:
    query = update.callback_query
    await query.answer()
    lang = get_user_lang(context)
    text_type = query.data.replace("text_", "")
    context.user_data["text_type"] = text_type

    type_names = {
        "essay": {"uz": "esse", "ru": "эссе", "en": "essay"},
        "article": {"uz": "maqola", "ru": "статьи", "en": "article"},
        "report": {"uz": "referat", "ru": "реферата", "en": "report"}
    }
    type_name = type_names.get(text_type, {}).get(lang, text_type)

    keyboard = [[InlineKeyboardButton(t("btn_cancel", lang), callback_data="menu_back")]]
    await query.edit_message_text(
        text=t("text_topic", lang, text_type=type_name),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return TEXT_TOPIC


async def text_topic_received(update: Update, context) -> int:
    lang = get_user_lang(context)
    user_id = update.effective_user.id
    topic = update.message.text
    text_type = context.user_data.get("text_type", "essay")

    if not deduct_balance(user_id, TEXT_WRITING_PRICE):
        balance = get_user_balance(user_id)
        keyboard = [[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")]]
        await update.message.reply_text(
            text=t("not_enough_balance", lang,
                   balance=format_sum(balance),
                   needed=format_sum(TEXT_WRITING_PRICE)),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return MAIN_MENU

    status_msg = await update.message.reply_text(t("text_generating", lang))

    try:
        result_text = await generate_text(topic, text_type, lang)
        await status_msg.delete()

        if len(result_text) > 4000:
            file_path = os.path.join(OUTPUT_DIR, f"{text_type}_{user_id}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(result_text)
            with open(file_path, "rb") as f:
                await update.message.reply_document(
                    document=f,
                    filename=f"{text_type}_{topic[:20]}.txt",
                    caption=t("text_ready", lang)
                )
            try:
                os.remove(file_path)
            except:
                pass
        else:
            await update.message.reply_text(f"{t('text_ready', lang)}\n\n{result_text}")

        increment_tasks(user_id)

    except Exception as e:
        logger.error(f"Matn yozishda xatolik: {e}")
        update_balance(user_id, TEXT_WRITING_PRICE)
        await status_msg.edit_text(t("error_ai", lang))

    balance = get_user_balance(user_id)
    await update.message.reply_text(
        text=t("welcome_back", lang, balance=format_sum(balance)),
        reply_markup=main_menu_keyboard(lang)
    )
    return MAIN_MENU


# ===== /buy =====
async def buy_command(update: Update, context) -> int:
    user_id = update.effective_user.id
    user = get_user(user_id)
    if user:
        context.user_data["language"] = user["language"]

    lang = get_user_lang(context)
    keyboard = []
    for key, pkg in BALANCE_PACKAGES.items():
        keyboard.append([InlineKeyboardButton(pkg["label"], callback_data=f"buy_{key}")])
    keyboard.append([InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")])

    await update.message.reply_text(
        text=t("buy_balance_info", lang),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return PAYMENT_PACKAGE


# ===== To'lov =====
async def payment_package_selected(update: Update, context) -> int:
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

    package_key = data.replace("buy_", "")
    package = BALANCE_PACKAGES.get(package_key)
    if not package:
        return MAIN_MENU

    context.user_data["payment_amount"] = package["amount"]
    keyboard = [[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")]]

    await query.edit_message_text(
        text=t("payment_instructions", lang,
               amount=format_sum(package["amount"]),
               card_number=PAYMENT_CARD_NUMBER,
               card_holder=PAYMENT_CARD_HOLDER),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML
    )
    return PAYMENT_RECEIPT


async def payment_receipt_received(update: Update, context) -> int:
    lang = get_user_lang(context)
    user_id = update.effective_user.id

    if not update.message.photo:
        await update.message.reply_text(
            "❌ Iltimos, chek rasmini yuboring / Пожалуйста, отправьте фото чека / Please send a receipt photo"
        )
        return PAYMENT_RECEIPT

    photo = update.message.photo[-1]
    file = await photo.get_file()
    photo_path = os.path.join(OUTPUT_DIR, f"receipt_{user_id}_{photo.file_unique_id}.jpg")
    await file.download_to_drive(photo_path)

    amount = context.user_data.get("payment_amount", 0)
    payment_id = create_payment(user_id, amount, photo_path)

    await update.message.reply_text(t("payment_received", lang))

    for admin_id in ADMIN_IDS:
        try:
            user = get_user(user_id)
            admin_text = (
                f"💳 Yangi to'lov #{payment_id}\n\n"
                f"👤 {user['full_name']} (@{user['username']})\n"
                f"💰 {format_sum(amount)} so'm\n"
            )
            keyboard = [
                [
                    InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"admin_approve_{payment_id}"),
                    InlineKeyboardButton("❌ Rad etish", callback_data=f"admin_reject_{payment_id}")
                ]
            ]
            with open(photo_path, "rb") as f:
                await context.bot.send_photo(
                    chat_id=admin_id, photo=f, caption=admin_text,
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
        except Exception as e:
            logger.error(f"Adminga xabar yuborishda xatolik: {e}")

    user_balance = get_user_balance(user_id)
    await update.message.reply_text(
        text=t("welcome_back", lang, balance=format_sum(user_balance)),
        reply_markup=main_menu_keyboard(lang)
    )
    return MAIN_MENU


# ===== Admin =====
async def admin_command(update: Update, context) -> int:
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Sizda ruxsat yo'q / Access denied")
        return MAIN_MENU

    lang = get_user_lang(context)
    stats = get_stats()

    keyboard = [
        [InlineKeyboardButton(t("btn_admin_payments", lang), callback_data="admin_payments")],
        [InlineKeyboardButton(t("btn_admin_broadcast", lang), callback_data="admin_broadcast")],
        [InlineKeyboardButton(t("btn_admin_stats", lang), callback_data="admin_stats")]
    ]

    await update.message.reply_text(
        text=t("admin_panel", lang,
               users=stats["total_users"],
               tasks=stats["total_tasks"],
               payments=stats["total_payments"],
               revenue=format_sum(stats["total_revenue"])),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return MAIN_MENU


async def admin_callback(update: Update, context) -> int:
    query = update.callback_query
    user_id = query.from_user.id
    if user_id not in ADMIN_IDS:
        return MAIN_MENU

    lang = get_user_lang(context)
    data = query.data

    if data.startswith("admin_approve_"):
        payment_id = int(data.replace("admin_approve_", ""))
        payment = approve_payment(payment_id, user_id)
        if payment:
            target_user_id = payment["user_id"]
            target_amount = payment["amount"]
            target_balance = get_user_balance(target_user_id)
            target_lang = "uz"
            target_user = get_user(target_user_id)
            if target_user:
                target_lang = target_user["language"]
            try:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=t("payment_approved_user", target_lang,
                           amount=format_sum(target_amount),
                           balance=format_sum(target_balance))
                )
            except:
                pass
        await query.edit_message_caption(caption=query.message.caption + "\n\n✅ TASDIQLANDI")

    elif data.startswith("admin_reject_"):
        payment_id = int(data.replace("admin_reject_", ""))
        payment = reject_payment(payment_id, user_id)
        if payment:
            target_user_id = payment["user_id"]
            target_lang = "uz"
            target_user = get_user(target_user_id)
            if target_user:
                target_lang = target_user["language"]
            try:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=t("payment_rejected_user", target_lang)
                )
            except:
                pass
        await query.edit_message_caption(caption=query.message.caption + "\n\n❌ RAD ETILDI")

    elif data == "admin_payments":
        payments = get_pending_payments()
        if not payments:
            await query.edit_message_text(t("no_pending_payments", lang))
            return MAIN_MENU
        for p in payments:
            text = (
                f"💳 To'lov #{p['id']}\n"
                f"👤 {p['full_name']} (@{p['username']})\n"
                f"💰 {format_sum(p['amount'])} so'm\n"
                f"📅 {p['created_at']}"
            )
            keyboard = [
                [
                    InlineKeyboardButton("✅", callback_data=f"admin_approve_{p['id']}"),
                    InlineKeyboardButton("❌", callback_data=f"admin_reject_{p['id']}")
                ]
            ]
            try:
                if p['receipt_photo'] and os.path.exists(p['receipt_photo']):
                    with open(p['receipt_photo'], "rb") as f:
                        await context.bot.send_photo(
                            chat_id=user_id, photo=f, caption=text,
                            reply_markup=InlineKeyboardMarkup(keyboard)
                        )
                else:
                    await context.bot.send_message(
                        chat_id=user_id, text=text,
                        reply_markup=InlineKeyboardMarkup(keyboard)
                    )
            except Exception as e:
                logger.error(f"To'lov ko'rsatishda xatolik: {e}")

    elif data == "admin_broadcast":
        await query.edit_message_text(t("broadcast_prompt", lang))
        return ADMIN_BROADCAST

    elif data == "admin_stats":
        stats = get_stats()
        await query.edit_message_text(
            t("admin_panel", lang,
              users=stats["total_users"],
              tasks=stats["total_tasks"],
              payments=stats["total_payments"],
              revenue=format_sum(stats["total_revenue"]))
        )

    return MAIN_MENU


async def broadcast_message(update: Update, context) -> int:
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        return MAIN_MENU

    lang = get_user_lang(context)
    text = update.message.text
    users = get_all_users()

    sent_count = 0
    for user in users:
        try:
            await context.bot.send_message(chat_id=user["user_id"], text=text)
            sent_count += 1
        except:
            pass

    await update.message.reply_text(t("broadcast_sent", lang, count=sent_count))
    return MAIN_MENU


# ===== Fallback =====
async def cancel(update: Update, context) -> int:
    lang = get_user_lang(context)
    user_id = update.effective_user.id
    balance = get_user_balance(user_id)
    await update.message.reply_text(
        text=t("welcome_back", lang, balance=format_sum(balance)),
        reply_markup=main_menu_keyboard(lang)
    )
    return MAIN_MENU


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


def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start_command),
            CommandHandler("admin", admin_command),
            CommandHandler("buy", buy_command),
        ],
        states={
            LANG_SELECT: [
                CallbackQueryHandler(language_selected, pattern="^lang_"),
                CallbackQueryHandler(check_sub_callback, pattern="^check_sub$"),
            ],
            MAIN_MENU: [
                CallbackQueryHandler(menu_callback, pattern="^menu_"),
                CallbackQueryHandler(admin_callback, pattern="^admin_"),
            ],
            PRES_PACKAGE: [
                CallbackQueryHandler(presentation_package_selected, pattern="^(pkg_|menu_back)"),
            ],
            PRES_SLIDES: [
                CallbackQueryHandler(presentation_slides_selected, pattern="^(slides_|menu_back)"),
            ],
            PRES_TEMPLATE: [
                MessageHandler(filters.StatusUpdate.WEB_APP_DATA, presentation_webapp_data),
                CallbackQueryHandler(presentation_template_selected, pattern="^(tmpl_|menu_back)"),
            ],
            PRES_TOPIC: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, presentation_topic_received),
                CallbackQueryHandler(handle_back_button, pattern="^menu_back$"),
            ],
            PRES_CONFIRM: [
                CallbackQueryHandler(presentation_confirm, pattern="^(pres_create|menu_back)"),
            ],
            TEXT_TYPE: [
                CallbackQueryHandler(text_type_selected, pattern="^text_"),
                CallbackQueryHandler(handle_back_button, pattern="^menu_back$"),
            ],
            TEXT_TOPIC: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, text_topic_received),
                CallbackQueryHandler(handle_back_button, pattern="^menu_back$"),
            ],
            PAYMENT_PACKAGE: [
                CallbackQueryHandler(payment_package_selected, pattern="^(buy_|menu_back)"),
            ],
            PAYMENT_RECEIPT: [
                MessageHandler(filters.PHOTO, payment_receipt_received),
                CallbackQueryHandler(handle_back_button, pattern="^menu_back$"),
            ],
            ADMIN_BROADCAST: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, broadcast_message),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("start", start_command),
            CommandHandler("admin", admin_command),
            CommandHandler("buy", buy_command),
        ],
        allow_reentry=True,
    )

    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(admin_callback, pattern="^admin_"))

    logger.info("Bot ishga tushdi!")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
