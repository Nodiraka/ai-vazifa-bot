"""Ko'p tilli matnlar"""

TEXTS = {
    # ===== Umumiy =====
    "choose_language": {
        "uz": "🌐 Tilni tanlang:",
        "ru": "🌐 Выберите язык:",
        "en": "🌐 Choose language:"
    },
    "language_set": {
        "uz": "✅ Til o'zbek tiliga o'zgartirildi!",
        "ru": "✅ Язык изменён на русский!",
        "en": "✅ Language changed to English!"
    },

    # ===== Kanal obuna =====
    "subscribe_channel": {
        "uz": "⚠️ Botni ishga tushirishdan oldin iltimos shu kanalga a'zo bo'ling:",
        "ru": "⚠️ Пожалуйста, подпишитесь на канал перед использованием бота:",
        "en": "⚠️ Please subscribe to the channel before using the bot:"
    },
    "subscribe_button": {
        "uz": "📢 Kanalga a'zo bo'lish",
        "ru": "📢 Подписаться на канал",
        "en": "📢 Subscribe to channel"
    },
    "check_subscription": {
        "uz": "✅ Tekshirish",
        "ru": "✅ Проверить",
        "en": "✅ Check"
    },
    "not_subscribed": {
        "uz": "❌ Siz hali kanalga a'zo bo'lmagansiz. Iltimos, avval kanalga a'zo bo'ling!",
        "ru": "❌ Вы ещё не подписаны на канал. Пожалуйста, подпишитесь!",
        "en": "❌ You haven't subscribed yet. Please subscribe first!"
    },

    # ===== Asosiy menyu =====
    "welcome": {
        "uz": "👋 Xush kelibsiz! Sizga {balance} so'm berildi.\n\nMen sizga quyidagi vazifalarda yordam bera olaman:\n\n📊 Taqdimot yaratish (PowerPoint)\n✍️ Matn yozish (esse, maqola, referat)\n\nQuyidagi tugmalardan birini tanlang:",
        "ru": "👋 Добро пожаловать! Вам начислено {balance} сум.\n\nЯ могу помочь вам с:\n\n📊 Создание презентаций (PowerPoint)\n✍️ Написание текстов (эссе, статьи, рефераты)\n\nВыберите одну из кнопок ниже:",
        "en": "👋 Welcome! You've been given {balance} sum.\n\nI can help you with:\n\n📊 Creating presentations (PowerPoint)\n✍️ Writing texts (essays, articles, reports)\n\nChoose one of the buttons below:"
    },
    "welcome_back": {
        "uz": "👋 Qaytganingizdan xursandmiz!\n\n💰 Balans: {balance} so'm\n\nQuyidagi tugmalardan birini tanlang:",
        "ru": "👋 Рады видеть вас снова!\n\n💰 Баланс: {balance} сум\n\nВыберите одну из кнопок ниже:",
        "en": "👋 Welcome back!\n\n💰 Balance: {balance} sum\n\nChoose one of the buttons below:"
    },
    "main_menu": {
        "uz": "📋 Asosiy menyu",
        "ru": "📋 Главное меню",
        "en": "📋 Main menu"
    },

    # ===== Menyu tugmalari =====
    "btn_presentation": {
        "uz": "📊 Taqdimot yaratish",
        "ru": "📊 Создать презентацию",
        "en": "📊 Create presentation"
    },
    "btn_text_writing": {
        "uz": "✍️ Matn yozish",
        "ru": "✍️ Написать текст",
        "en": "✍️ Write text"
    },
    "btn_balance": {
        "uz": "💰 Balans",
        "ru": "💰 Баланс",
        "en": "💰 Balance"
    },
    "btn_change_language": {
        "uz": "🌐 Tilni o'zgartirish",
        "ru": "🌐 Сменить язык",
        "en": "🌐 Change language"
    },
    "btn_help": {
        "uz": "❓ Yordam",
        "ru": "❓ Помощь",
        "en": "❓ Help"
    },
    "btn_back": {
        "uz": "⬅️ Orqaga",
        "ru": "⬅️ Назад",
        "en": "⬅️ Back"
    },

    # ===== Taqdimot =====
    "presentation_topic": {
        "uz": "📊 Taqdimot mavzusini yozing:\n\n(Masalan: \"Suniy intellekt va uning kelajagi\")",
        "ru": "📊 Напишите тему презентации:\n\n(Например: \"Искусственный интеллект и его будущее\")",
        "en": "📊 Write the presentation topic:\n\n(Example: \"Artificial Intelligence and its future\")"
    },
    "presentation_slides_count": {
        "uz": "📊 Nechta slayd bo'lsin? (5-20 oralig'ida raqam yozing)",
        "ru": "📊 Сколько слайдов? (Напишите число от 5 до 20)",
        "en": "📊 How many slides? (Write a number between 5-20)"
    },
    "presentation_generating": {
        "uz": "⏳ Taqdimot tayyorlanmoqda... Bu 1-3 daqiqa vaqt olishi mumkin.",
        "ru": "⏳ Презентация готовится... Это может занять 1-3 минуты.",
        "en": "⏳ Generating presentation... This may take 1-3 minutes."
    },
    "presentation_ready": {
        "uz": "✅ Taqdimot tayyor! Yuklab oling:",
        "ru": "✅ Презентация готова! Скачайте:",
        "en": "✅ Presentation is ready! Download:"
    },
    "invalid_slides_count": {
        "uz": "❌ Iltimos, 5 dan 20 gacha raqam kiriting.",
        "ru": "❌ Пожалуйста, введите число от 5 до 20.",
        "en": "❌ Please enter a number between 5 and 20."
    },

    # ===== Matn yozish =====
    "text_type_select": {
        "uz": "✍️ Qanday turdagi matn yozilsin?",
        "ru": "✍️ Какой тип текста написать?",
        "en": "✍️ What type of text to write?"
    },
    "btn_essay": {
        "uz": "📝 Esse",
        "ru": "📝 Эссе",
        "en": "📝 Essay"
    },
    "btn_article": {
        "uz": "📰 Maqola",
        "ru": "📰 Статья",
        "en": "📰 Article"
    },
    "btn_report": {
        "uz": "📄 Referat",
        "ru": "📄 Реферат",
        "en": "📄 Report"
    },
    "text_topic": {
        "uz": "✍️ {text_type} mavzusini yozing:",
        "ru": "✍️ Напишите тему {text_type}:",
        "en": "✍️ Write the {text_type} topic:"
    },
    "text_generating": {
        "uz": "⏳ Matn yozilmoqda... Bu 1-2 daqiqa vaqt olishi mumkin.",
        "ru": "⏳ Текст пишется... Это может занять 1-2 минуты.",
        "en": "⏳ Writing text... This may take 1-2 minutes."
    },
    "text_ready": {
        "uz": "✅ Matn tayyor!",
        "ru": "✅ Текст готов!",
        "en": "✅ Text is ready!"
    },

    # ===== Balans =====
    "balance_info": {
        "uz": "💰 Sizning balansingiz: {balance} so'm\n\n📊 Taqdimot yaratish: {pres_price} so'm\n✍️ Matn yozish: {text_price} so'm\n\n➖➖➖➖➖➖➖➖➖➖\nBalansni to'ldirish uchun: /buy",
        "ru": "💰 Ваш баланс: {balance} сум\n\n📊 Создание презентации: {pres_price} сум\n✍️ Написание текста: {text_price} сум\n\n➖➖➖➖➖➖➖➖➖➖\nПополнить баланс: /buy",
        "en": "💰 Your balance: {balance} sum\n\n📊 Create presentation: {pres_price} sum\n✍️ Write text: {text_price} sum\n\n➖➖➖➖➖➖➖➖➖➖\nTop up balance: /buy"
    },
    "not_enough_balance": {
        "uz": "❌ Balansingiz yetarli emas!\n\n💰 Sizda: {balance} so'm\n💳 Kerak: {needed} so'm\n\nBalansni to'ldirish uchun: /buy",
        "ru": "❌ Недостаточно средств!\n\n💰 У вас: {balance} сум\n💳 Нужно: {needed} сум\n\nПополнить баланс: /buy",
        "en": "❌ Insufficient balance!\n\n💰 You have: {balance} sum\n💳 Need: {needed} sum\n\nTop up balance: /buy"
    },
    "buy_balance_info": {
        "uz": "🛒 Balansni to'ldirish\n\nQuyidagi paketlardan birini tanlang:",
        "ru": "🛒 Пополнение баланса\n\nВыберите один из пакетов:",
        "en": "🛒 Top up balance\n\nChoose one of the packages:"
    },
    "payment_instructions": {
        "uz": "💳 To'lov qilish uchun:\n\n1️⃣ Quyidagi karta raqamiga {amount} so'm o'tkazing:\n\n<code>{card_number}</code>\n👤 {card_holder}\n\n2️⃣ To'lov chekini (screenshot) shu yerga yuboring.",
        "ru": "💳 Для оплаты:\n\n1️⃣ Переведите {amount} сум на карту:\n\n<code>{card_number}</code>\n👤 {card_holder}\n\n2️⃣ Отправьте чек (скриншот) сюда.",
        "en": "💳 To make payment:\n\n1️⃣ Transfer {amount} sum to the card:\n\n<code>{card_number}</code>\n👤 {card_holder}\n\n2️⃣ Send the receipt (screenshot) here."
    },
    "payment_received": {
        "uz": "✅ Chek qabul qilindi! Admin tekshirgandan so'ng balansingiz to'ldiriladi.",
        "ru": "✅ Чек получен! Баланс будет пополнен после проверки администратором.",
        "en": "✅ Receipt received! Balance will be topped up after admin verification."
    },

    # ===== Yordam =====
    "help_text": {
        "uz": "❓ Yordam\n\nBu bot sizga quyidagi vazifalarda yordam beradi:\n\n📊 **Taqdimot yaratish** - mavzu yozing, bot PowerPoint taqdimot yaratib beradi\n✍️ **Matn yozish** - esse, maqola yoki referat yozdiring\n\n💰 **Narxlar:**\n- Taqdimot: 6,000 so'm\n- Matn yozish: 3,000 so'm\n\n🛒 Balansni to'ldirish: /buy\n\nSavollar bo'lsa: @admin_username",
        "ru": "❓ Помощь\n\nЭтот бот поможет вам с:\n\n📊 **Создание презентаций** - напишите тему, бот создаст PowerPoint\n✍️ **Написание текстов** - эссе, статьи или рефераты\n\n💰 **Цены:**\n- Презентация: 6,000 сум\n- Написание текста: 3,000 сум\n\n🛒 Пополнить баланс: /buy\n\nВопросы: @admin_username",
        "en": "❓ Help\n\nThis bot helps you with:\n\n📊 **Create presentations** - write a topic, bot creates PowerPoint\n✍️ **Write texts** - essays, articles or reports\n\n💰 **Prices:**\n- Presentation: 6,000 sum\n- Text writing: 3,000 sum\n\n🛒 Top up balance: /buy\n\nQuestions: @admin_username"
    },

    # ===== Xatoliklar =====
    "error_general": {
        "uz": "❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.",
        "ru": "❌ Произошла ошибка. Пожалуйста, попробуйте снова.",
        "en": "❌ An error occurred. Please try again."
    },
    "error_ai": {
        "uz": "❌ AI xizmati bilan bog'lanishda xatolik. Iltimos, keyinroq urinib ko'ring.",
        "ru": "❌ Ошибка связи с AI сервисом. Попробуйте позже.",
        "en": "❌ Error connecting to AI service. Please try later."
    },

    # ===== Admin =====
    "admin_panel": {
        "uz": "🔧 Admin panel\n\n👥 Foydalanuvchilar: {users}\n📋 Bajarilgan vazifalar: {tasks}\n💳 Tasdiqlangan to'lovlar: {payments}\n💰 Jami daromad: {revenue} so'm",
        "ru": "🔧 Админ панель\n\n👥 Пользователи: {users}\n📋 Выполненные задачи: {tasks}\n💳 Одобренные платежи: {payments}\n💰 Общий доход: {revenue} сум",
        "en": "🔧 Admin panel\n\n👥 Users: {users}\n📋 Completed tasks: {tasks}\n💳 Approved payments: {payments}\n💰 Total revenue: {revenue} sum"
    },
    "btn_admin_stats": {
        "uz": "📊 Statistika",
        "ru": "📊 Статистика",
        "en": "📊 Statistics"
    },
    "btn_admin_payments": {
        "uz": "💳 Kutilayotgan to'lovlar",
        "ru": "💳 Ожидающие платежи",
        "en": "💳 Pending payments"
    },
    "btn_admin_broadcast": {
        "uz": "📢 Xabar yuborish",
        "ru": "📢 Рассылка",
        "en": "📢 Broadcast"
    },
    "btn_approve": {
        "uz": "✅ Tasdiqlash",
        "ru": "✅ Одобрить",
        "en": "✅ Approve"
    },
    "btn_reject": {
        "uz": "❌ Rad etish",
        "ru": "❌ Отклонить",
        "en": "❌ Reject"
    },
    "payment_approved_user": {
        "uz": "✅ To'lovingiz tasdiqlandi! {amount} so'm balansingizga qo'shildi.\n\n💰 Joriy balans: {balance} so'm",
        "ru": "✅ Оплата одобрена! {amount} сум добавлено на баланс.\n\n💰 Текущий баланс: {balance} сум",
        "en": "✅ Payment approved! {amount} sum added to balance.\n\n💰 Current balance: {balance} sum"
    },
    "payment_rejected_user": {
        "uz": "❌ To'lovingiz rad etildi. Iltimos, to'g'ri chek yuboring yoki admin bilan bog'laning.",
        "ru": "❌ Оплата отклонена. Пожалуйста, отправьте правильный чек или свяжитесь с админом.",
        "en": "❌ Payment rejected. Please send a correct receipt or contact admin."
    },
    "no_pending_payments": {
        "uz": "✅ Kutilayotgan to'lovlar yo'q.",
        "ru": "✅ Нет ожидающих платежей.",
        "en": "✅ No pending payments."
    },
    "broadcast_prompt": {
        "uz": "📢 Barcha foydalanuvchilarga yuboriladigan xabarni yozing:",
        "ru": "📢 Напишите сообщение для рассылки всем пользователям:",
        "en": "📢 Write a message to broadcast to all users:"
    },
    "broadcast_sent": {
        "uz": "✅ Xabar {count} foydalanuvchiga yuborildi.",
        "ru": "✅ Сообщение отправлено {count} пользователям.",
        "en": "✅ Message sent to {count} users."
    },
}


def t(key: str, lang: str = "uz", **kwargs) -> str:
    """Matnni olish"""
    text_dict = TEXTS.get(key, {})
    text = text_dict.get(lang, text_dict.get("uz", f"[{key}]"))
    if kwargs:
        text = text.format(**kwargs)
    return text
