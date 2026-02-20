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
    "btn_cancel": {
        "uz": "❌ To'xtatish",
        "ru": "❌ Отмена",
        "en": "❌ Cancel"
    },
    "btn_create": {
        "uz": "✅ Yaratish",
        "ru": "✅ Создать",
        "en": "✅ Create"
    },
    "btn_choose_template": {
        "uz": "🎨 Shablon tanlash",
        "ru": "🎨 Выбрать шаблон",
        "en": "🎨 Choose template"
    },

    # ===== Taqdimot - 1-qadam: Paket tanlash =====
    "presentation_choose_package": {
        "uz": "📊 <b>Taqdimot turini tanlang:</b>\n\n"
              "📋 <b>Oddiy taqdimot</b>\n"
              "   Stock fotolar bilan professional taqdimot\n\n"
              "⭐ <b>Premium taqdimot</b>\n"
              "   AI rasmlar va diagrammalar bilan yuqori sifatli taqdimot",
        "ru": "📊 <b>Выберите тип презентации:</b>\n\n"
              "📋 <b>Обычная презентация</b>\n"
              "   Профессиональная презентация со стоковыми фото\n\n"
              "⭐ <b>Премиум презентация</b>\n"
              "   Высококачественная презентация с AI изображениями и диаграммами",
        "en": "📊 <b>Choose presentation type:</b>\n\n"
              "📋 <b>Standard presentation</b>\n"
              "   Professional presentation with stock photos\n\n"
              "⭐ <b>Premium presentation</b>\n"
              "   High-quality presentation with AI images and diagrams"
    },
    "btn_package_standard": {
        "uz": "📋 Oddiy taqdimot",
        "ru": "📋 Обычная презентация",
        "en": "📋 Standard presentation"
    },
    "btn_package_premium": {
        "uz": "⭐ Premium taqdimot",
        "ru": "⭐ Премиум презентация",
        "en": "⭐ Premium presentation"
    },

    # ===== Taqdimot - 2-qadam: Sahifalar soni =====
    "presentation_choose_slides": {
        "uz": "📄 <b>Sahifalar soni nechta bo'lsin?</b>\n\nQuyidagi tugmalardan birini tanlang (6 dan 30 gacha):",
        "ru": "📄 <b>Сколько страниц?</b>\n\nВыберите одну из кнопок ниже (от 6 до 30):",
        "en": "📄 <b>How many slides?</b>\n\nChoose one of the buttons below (6 to 30):"
    },

    # ===== Taqdimot - 3-qadam: Dizayn tanlash =====
    "presentation_choose_template": {
        "uz": "🎨 <b>Dizaynni tanlang:</b>",
        "ru": "🎨 <b>Выберите дизайн:</b>",
        "en": "🎨 <b>Choose design:</b>"
    },
    "btn_template_business": {
        "uz": "💼 Biznes",
        "ru": "💼 Бизнес",
        "en": "💼 Business"
    },
    "btn_template_education": {
        "uz": "🎓 Ta'lim",
        "ru": "🎓 Образование",
        "en": "🎓 Education"
    },
    "btn_template_technology": {
        "uz": "💻 Texnologiya",
        "ru": "💻 Технологии",
        "en": "💻 Technology"
    },
    "btn_template_medical": {
        "uz": "🏥 Tibbiyot",
        "ru": "🏥 Медицина",
        "en": "🏥 Medical"
    },
    "btn_template_creative": {
        "uz": "🎨 Ijodiy",
        "ru": "🎨 Креативный",
        "en": "🎨 Creative"
    },
    "btn_template_minimal": {
        "uz": "⬜ Minimalist",
        "ru": "⬜ Минималист",
        "en": "⬜ Minimal"
    },

    # ===== Taqdimot - 4-qadam: Mavzu =====
    "presentation_topic": {
        "uz": "📝 <b>Taqdimot mavzusini kiriting:</b>\n\n"
              "• Mavzuni batafsil yoritishga harakat qiling.\n"
              "• Qisqartma so'zlarga, imloviy xatoli so'zlarga tushunmay qolishim mumkin.\n\n"
              "💡 Masalan: <i>Suniy intellekt va uning kelajagi</i>",
        "ru": "📝 <b>Введите тему презентации:</b>\n\n"
              "• Постарайтесь подробно описать тему.\n"
              "• Сокращения и ошибки могут быть неправильно поняты.\n\n"
              "💡 Например: <i>Искусственный интеллект и его будущее</i>",
        "en": "📝 <b>Enter the presentation topic:</b>\n\n"
              "• Try to describe the topic in detail.\n"
              "• Abbreviations and typos may be misunderstood.\n\n"
              "💡 Example: <i>Artificial Intelligence and its future</i>"
    },
    "presentation_summary": {
        "uz": "📋 <b>Taqdimot Haqida</b>\n\n"
              "📌 <b>Mavzu:</b> {topic}\n"
              "📦 <b>Paket:</b> {package}\n"
              "🎨 <b>Dizayn:</b> {template}\n"
              "📄 <b>Sahifalar soni:</b> {slides} ta\n"
              "🌐 <b>Til:</b> {lang_name}\n"
              "💰 <b>Narx:</b> {price} so'm\n\n"
              "👉 Ushbu sozlamalar asosida slaydingiz yaratiladi.\n"
              "Davom etish uchun <b>✅ Yaratish</b> tugmasini bosing.",
        "ru": "📋 <b>О презентации</b>\n\n"
              "📌 <b>Тема:</b> {topic}\n"
              "📦 <b>Пакет:</b> {package}\n"
              "🎨 <b>Дизайн:</b> {template}\n"
              "📄 <b>Количество страниц:</b> {slides}\n"
              "🌐 <b>Язык:</b> {lang_name}\n"
              "💰 <b>Цена:</b> {price} сум\n\n"
              "👉 Презентация будет создана с этими настройками.\n"
              "Для продолжения нажмите <b>✅ Создать</b>.",
        "en": "📋 <b>Presentation Info</b>\n\n"
              "📌 <b>Topic:</b> {topic}\n"
              "📦 <b>Package:</b> {package}\n"
              "🎨 <b>Design:</b> {template}\n"
              "📄 <b>Number of slides:</b> {slides}\n"
              "🌐 <b>Language:</b> {lang_name}\n"
              "💰 <b>Price:</b> {price} sum\n\n"
              "👉 Your presentation will be created with these settings.\n"
              "Press <b>✅ Create</b> to continue."
    },
    "presentation_generating": {
        "uz": "⏳ Taqdimot tayyorlanmoqda...\n\n📊 Mavzu: {topic}\n🎨 Dizayn: {template}\n📄 Sahifalar: {slides}\n💰 Narx: {price} so'm\n\nBu 1-3 daqiqa vaqt olishi mumkin.",
        "ru": "⏳ Презентация готовится...\n\n📊 Тема: {topic}\n🎨 Дизайн: {template}\n📄 Страницы: {slides}\n💰 Цена: {price} сум\n\nЭто может занять 1-3 минуты.",
        "en": "⏳ Generating presentation...\n\n📊 Topic: {topic}\n🎨 Design: {template}\n📄 Slides: {slides}\n💰 Price: {price} sum\n\nThis may take 1-3 minutes."
    },
    "presentation_ready": {
        "uz": "✅ Taqdimot tayyor! Yuklab oling:",
        "ru": "✅ Презентация готова! Скачайте:",
        "en": "✅ Presentation is ready! Download:"
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
        "uz": "💰 Sizning balansingiz: <b>{balance} so'm</b>\n\n"
              "📊 <b>Taqdimot narxlari:</b>\n"
              "  📋 Oddiy:   2,000 - 5,000 so'm\n"
              "  ⭐ Premium: 4,000 - 8,000 so'm\n\n"
              "✍️ <b>Matn yozish:</b> {text_price} so'm\n\n"
              "➖➖➖➖➖➖➖➖➖➖\n"
              "Balansni to'ldirish uchun: /buy",
        "ru": "💰 Ваш баланс: <b>{balance} сум</b>\n\n"
              "📊 <b>Цены на презентации:</b>\n"
              "  📋 Обычная:  2,000 - 5,000 сум\n"
              "  ⭐ Премиум: 4,000 - 8,000 сум\n\n"
              "✍️ <b>Написание текста:</b> {text_price} сум\n\n"
              "➖➖➖➖➖➖➖➖➖➖\n"
              "Пополнить баланс: /buy",
        "en": "💰 Your balance: <b>{balance} sum</b>\n\n"
              "📊 <b>Presentation prices:</b>\n"
              "  📋 Standard: 2,000 - 5,000 sum\n"
              "  ⭐ Premium:  4,000 - 8,000 sum\n\n"
              "✍️ <b>Text writing:</b> {text_price} sum\n\n"
              "➖➖➖➖➖➖➖➖➖➖\n"
              "Top up balance: /buy"
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
        "uz": "❓ <b>Yordam</b>\n\nBu bot sizga quyidagi vazifalarda yordam beradi:\n\n"
              "📊 <b>Taqdimot yaratish</b> - mavzu yozing, bot PowerPoint taqdimot yaratib beradi\n"
              "✍️ <b>Matn yozish</b> - esse, maqola yoki referat yozdiring\n\n"
              "💰 <b>Narxlar:</b>\n"
              "📋 Oddiy taqdimot: 2,000 - 5,000 so'm\n"
              "⭐ Premium taqdimot: 4,000 - 8,000 so'm\n"
              "✍️ Matn yozish: 3,000 so'm\n\n"
              "🛒 Balansni to'ldirish: /buy",
        "ru": "❓ <b>Помощь</b>\n\nЭтот бот поможет вам с:\n\n"
              "📊 <b>Создание презентаций</b> - напишите тему, бот создаст PowerPoint\n"
              "✍️ <b>Написание текстов</b> - эссе, статьи или рефераты\n\n"
              "💰 <b>Цены:</b>\n"
              "📋 Обычная презентация: 2,000 - 5,000 сум\n"
              "⭐ Премиум презентация: 4,000 - 8,000 сум\n"
              "✍️ Написание текста: 3,000 сум\n\n"
              "🛒 Пополнить баланс: /buy",
        "en": "❓ <b>Help</b>\n\nThis bot helps you with:\n\n"
              "📊 <b>Create presentations</b> - write a topic, bot creates PowerPoint\n"
              "✍️ <b>Write texts</b> - essays, articles or reports\n\n"
              "💰 <b>Prices:</b>\n"
              "📋 Standard presentation: 2,000 - 5,000 sum\n"
              "⭐ Premium presentation: 4,000 - 8,000 sum\n"
              "✍️ Text writing: 3,000 sum\n\n"
              "🛒 Top up balance: /buy"
    },

    # ===== Progress =====
    "progress_step1": {
        "uz": "📝 Rejalar yaratilmoqda...",
        "ru": "📝 Создание плана...",
        "en": "📝 Creating outline..."
    },
    "progress_step2": {
        "uz": "✍️ Matnlar yozilmoqda...",
        "ru": "✍️ Написание текстов...",
        "en": "✍️ Writing content..."
    },
    "progress_step3": {
        "uz": "🎨 Dizayn qo'llanilmoqda...",
        "ru": "🎨 Применение дизайна...",
        "en": "🎨 Applying design..."
    },
    "progress_step4": {
        "uz": "✅ Taqdimot tayyor!",
        "ru": "✅ Презентация готова!",
        "en": "✅ Presentation is ready!"
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
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text
