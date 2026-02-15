"""AI Vazifa Bot - Asosiy bot fayli"""

import os
import json
import logging
import asyncio
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, ReplyKeyboardRemove
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ConversationHandler, filters
)
from telegram.constants import ParseMode, ChatMemberStatus

from config import (
    BOT_TOKEN, MANDATORY_CHANNEL_ID, MANDATORY_CHANNEL_LINK,
    ADMIN_IDS, PRESENTATION_PRICES, TEXT_WRITING_PRICE,
    BALANCE_PACKAGES, PAYMENT_CARD_NUMBER, PAYMENT_CARD_HOLDER,
    PRESENTATION_TEMPLATES
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
(LANG_SELECT, MAIN_MENU, PRES_PACKAGE, PRES_TEMPLATE, PRES_TOPIC, PRES_SLIDES,
 TEXT_TYPE, TEXT_TOPIC, PAYMENT_PACKAGE, PAYMENT_RECEIPT,
 ADMIN_BROADCAST) = range(11)

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_user_lang(context) -> str:
    """Foydalanuvchi tilini olish"""
    return context.user_data.get("language", "uz")


def format_sum(amount: int) -> str:
    """So'mni formatlash"""
    return f"{amount:,}".replace(",", " ")


async def check_subscription(user_id: int, context) -> bool:
    """Kanal obunasini tekshirish"""
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
    """Asosiy menyu klaviaturasi"""
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
    """Obuna tekshirish klaviaturasi"""
    keyboard = [
        [InlineKeyboardButton(t("subscribe_button", lang), url=MANDATORY_CHANNEL_LINK)],
        [InlineKeyboardButton(t("check_subscription", lang), callback_data="check_sub")]
    ]
    return InlineKeyboardMarkup(keyboard)


def language_keyboard() -> InlineKeyboardMarkup:
    """Til tanlash klaviaturasi"""
    keyboard = [
        [
            InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang_uz"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


# ===== /start buyrug'i =====
async def start_command(update: Update, context) -> int:
    """Start buyrug'i - har doim til tanlashdan boshlanadi"""
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
    """Til tanlangandan keyin"""
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
    """Obuna tekshirish callback"""
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
    """Asosiy menyuni ko'rsatish"""
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


# ===== Menyu callback handlerlari =====
async def menu_callback(update: Update, context) -> int:
    """Asosiy menyu callback handleri"""
    query = update.callback_query
    await query.answer()

    lang = get_user_lang(context)
    user_id = query.from_user.id
    data = query.data

    if data == "menu_presentation":
        # Paket tanlash
        keyboard = [
            [InlineKeyboardButton(t("btn_standard_15", lang), callback_data="pkg_standard_15")],
            [InlineKeyboardButton(t("btn_standard_25", lang), callback_data="pkg_standard_25")],
            [InlineKeyboardButton(t("btn_premium_15", lang), callback_data="pkg_premium_15")],
            [InlineKeyboardButton(t("btn_premium_25", lang), callback_data="pkg_premium_25")],
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
            [
                InlineKeyboardButton(t("btn_report", lang), callback_data="text_report"),
            ],
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


# ===== Taqdimot - Paket tanlash =====
async def presentation_package_selected(update: Update, context) -> int:
    """Taqdimot paketi tanlandi"""
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
    package = PRESENTATION_PRICES.get(package_key)

    if not package:
        return MAIN_MENU

    # Balans tekshirish
    balance = get_user_balance(user_id)
    if balance < package["price"]:
        keyboard = [[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")]]
        await query.edit_message_text(
            text=t("not_enough_balance", lang,
                   balance=format_sum(balance),
                   needed=format_sum(package["price"])),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return MAIN_MENU

    # Paket ma'lumotlarini saqlash
    context.user_data["pres_package"] = package_key
    context.user_data["pres_price"] = package["price"]
    context.user_data["pres_max_slides"] = package["max_slides"]
    context.user_data["pres_has_ai_images"] = package["has_ai_images"]

    # Shablon tanlash
    keyboard = [
        [
            InlineKeyboardButton(t("btn_template_business", lang), callback_data="tmpl_business"),
            InlineKeyboardButton(t("btn_template_education", lang), callback_data="tmpl_education"),
        ],
        [
            InlineKeyboardButton(t("btn_template_technology", lang), callback_data="tmpl_technology"),
            InlineKeyboardButton(t("btn_template_medical", lang), callback_data="tmpl_medical"),
        ],
        [
            InlineKeyboardButton(t("btn_template_creative", lang), callback_data="tmpl_creative"),
            InlineKeyboardButton(t("btn_template_minimal", lang), callback_data="tmpl_minimal"),
        ],
        [InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")]
    ]
    await query.edit_message_text(
        text=t("presentation_choose_template", lang),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return PRES_TEMPLATE


# ===== Taqdimot - Shablon tanlash =====
async def presentation_template_selected(update: Update, context) -> int:
    """Taqdimot shabloni tanlandi"""
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

    keyboard = [[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")]]
    await query.edit_message_text(
        text=t("presentation_topic", lang),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return PRES_TOPIC


# ===== Taqdimot - Mavzu =====
async def presentation_topic_received(update: Update, context) -> int:
    """Taqdimot mavzusi qabul qilindi"""
    lang = get_user_lang(context)
    context.user_data["pres_topic"] = update.message.text

    max_slides = context.user_data.get("pres_max_slides", 15)
    min_slides = 5

    keyboard = [[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")]]
    await update.message.reply_text(
        text=t("presentation_slides_count", lang, min_slides=min_slides, max_slides=max_slides),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return PRES_SLIDES


# ===== Taqdimot - Slayd soni =====
async def presentation_slides_received(update: Update, context) -> int:
    """Slaydlar soni qabul qilindi va taqdimot yaratish boshlandi"""
    lang = get_user_lang(context)
    user_id = update.effective_user.id

    max_slides = context.user_data.get("pres_max_slides", 15)
    min_slides = 5

    try:
        slides_count = int(update.message.text.strip())
        if slides_count < min_slides or slides_count > max_slides:
            raise ValueError()
    except ValueError:
        await update.message.reply_text(
            t("invalid_slides_count", lang, min_slides=min_slides, max_slides=max_slides)
        )
        return PRES_SLIDES

    price = context.user_data.get("pres_price", 3000)

    if not deduct_balance(user_id, price):
        balance = get_user_balance(user_id)
        keyboard = [[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")]]
        await update.message.reply_text(
            text=t("not_enough_balance", lang,
                   balance=format_sum(balance),
                   needed=format_sum(price)),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return MAIN_MENU

    topic = context.user_data.get("pres_topic", "")
    template_key = context.user_data.get("pres_template", "business")
    has_ai_images = context.user_data.get("pres_has_ai_images", False)

    # Shablon nomini olish
    template_info = PRESENTATION_TEMPLATES.get(template_key, {})
    lang_key = f"name_{lang}" if f"name_{lang}" in template_info else "name_uz"
    template_name = template_info.get(lang_key, template_key)

    status_msg = await update.message.reply_text(
        t("presentation_generating", lang,
          topic=topic, template=template_name, slides=slides_count)
    )

    try:
        file_path = await generate_presentation(
            topic, slides_count, lang, OUTPUT_DIR,
            template_key=template_key,
            has_ai_images=has_ai_images
        )

        with open(file_path, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename=os.path.basename(file_path),
                caption=t("presentation_ready", lang)
            )

        increment_tasks(user_id)

        await status_msg.delete()

        try:
            os.remove(file_path)
        except:
            pass

    except Exception as e:
        logger.error(f"Taqdimot yaratishda xatolik: {e}")
        update_balance(user_id, price)
        await status_msg.edit_text(t("error_ai", lang))

    balance = get_user_balance(user_id)
    await update.message.reply_text(
        text=t("welcome_back", lang, balance=format_sum(balance)),
        reply_markup=main_menu_keyboard(lang)
    )
    return MAIN_MENU


# ===== Matn yozish =====
async def text_type_selected(update: Update, context) -> int:
    """Matn turi tanlandi"""
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

    keyboard = [[InlineKeyboardButton(t("btn_back", lang), callback_data="menu_back")]]
    await query.edit_message_text(
        text=t("text_topic", lang, text_type=type_name),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return TEXT_TOPIC


async def text_topic_received(update: Update, context) -> int:
    """Matn mavzusi qabul qilindi"""
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
            await update.message.reply_text(
                f"{t('text_ready', lang)}\n\n{result_text}"
            )

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


# ===== /buy buyrug'i =====
async def buy_command(update: Update, context) -> int:
    """Balansni to'ldirish buyrug'i"""
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


# ===== To'lov tizimi =====
async def payment_package_selected(update: Update, context) -> int:
    """To'lov paketi tanlandi"""
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
    """To'lov cheki qabul qilindi"""
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
                    chat_id=admin_id,
                    photo=f,
                    caption=admin_text,
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


# ===== Admin funksiyalari =====
async def admin_command(update: Update, context) -> int:
    """Admin panel"""
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
    """Admin callback handleri"""
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

        await query.edit_message_caption(
            caption=query.message.caption + "\n\n✅ TASDIQLANDI"
        )

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

        await query.edit_message_caption(
            caption=query.message.caption + "\n\n❌ RAD ETILDI"
        )

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
                            chat_id=user_id,
                            photo=f,
                            caption=text,
                            reply_markup=InlineKeyboardMarkup(keyboard)
                        )
                else:
                    await context.bot.send_message(
                        chat_id=user_id,
                        text=text,
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
    """Barcha foydalanuvchilarga xabar yuborish"""
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
    """Bekor qilish"""
    lang = get_user_lang(context)
    user_id = update.effective_user.id
    balance = get_user_balance(user_id)

    await update.message.reply_text(
        text=t("welcome_back", lang, balance=format_sum(balance)),
        reply_markup=main_menu_keyboard(lang)
    )
    return MAIN_MENU


async def handle_back_button(update: Update, context) -> int:
    """Orqaga tugmasi"""
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
    """Botni ishga tushirish"""
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
            PRES_TEMPLATE: [
                CallbackQueryHandler(presentation_template_selected, pattern="^(tmpl_|menu_back)"),
            ],
            PRES_TOPIC: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, presentation_topic_received),
                CallbackQueryHandler(handle_back_button, pattern="^menu_back$"),
            ],
            PRES_SLIDES: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, presentation_slides_received),
                CallbackQueryHandler(handle_back_button, pattern="^menu_back$"),
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
