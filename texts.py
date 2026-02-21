"""Ko'p tilli matnlar - TO'LIQ VERSIYA"""

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
    "cancel_message": {
        "uz": "❌ Jarayon bekor qilindi.",
        "ru": "❌ Процесс отменён.",
        "en": "❌ Process cancelled."
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

    # ===== YANGI: Taqdimot - yangi jarayon =====
    "presentation_topic_input": {
        "uz": "📝 <b>Taqdimot mavzusini kiriting:</b>\n\nMasalan: Sun'iy intellekt rivojlanishi",
        "ru": "📝 <b>Введите тему презентации:</b>\n\nНапример: Развитие искусственного интеллекта",
        "en": "📝 <b>Enter presentation topic:</b>\n\nExample: AI Development"
    },
    
    "presentation_author_input": {
        "uz": "👤 <b>Ism-familyangizni kiriting:</b>\n\nBu taqdimotning birinchi va oxirgi sahifasida ko'rsatiladi.\n\nMasalan: Nodirbek Karimov",
        "ru": "👤 <b>Введите ваше имя и фамилию:</b>\n\nОни будут показаны на первой и последней странице.\n\nНапример: Нодирбек Каримов",
        "en": "👤 <b>Enter your name:</b>\n\nIt will be shown on first and last slides.\n\nExample: Nodirbek Karimov"
    },
    
    "presentation_language_select": {
        "uz": "🌐 <b>Taqdimot tilini tanlang:</b>\n\nTaqdimotdagi barcha matn shu tilda bo'ladi.",
        "ru": "🌐 <b>Выберите язык презентации:</b>\n\nВесь текст будет на этом языке.",
        "en": "🌐 <b>Choose presentation language:</b>\n\nAll text will be in this language."
    },
    
    "presentation_summary_new": {
        "uz": """📋 <b>Taqdimot ma'lumotlari:</b>

━━━━━━━━━━━━━━━━━━━━━━
📝 Mavzu: {topic}
👤 Muallif: {author}
🌐 Til: {language_name}
📦 Paket: {package}
📄 Asosiy sahifalar: {slides} ta
📊 Jami sahifalar: {total_slides} ta
   (1 sarlavha + 1 reja + {slides} kontent + 1 rahmat)
💰 Narx: {price} so'm
━━━━━━━━━━━━━━━━━━━━━━

Taqdimot rejasini qanday tuzamiz?""",
        "ru": """📋 <b>Информация о презентации:</b>

━━━━━━━━━━━━━━━━━━━━━━
📝 Тема: {topic}
👤 Автор: {author}
🌐 Язык: {language_name}
📦 Пакет: {package}
📄 Основные слайды: {slides} шт.
📊 Всего слайдов: {total_slides} шт.
   (1 титул + 1 план + {slides} контент + 1 спасибо)
💰 Цена: {price} сум
━━━━━━━━━━━━━━━━━━━━━━

Как составим план презентации?""",
        "en": """📋 <b>Presentation details:</b>

━━━━━━━━━━━━━━━━━━━━━━
📝 Topic: {topic}
👤 Author: {author}
🌐 Language: {language_name}
📦 Package: {package}
📄 Main slides: {slides}
📊 Total slides: {total_slides}
   (1 title + 1 plan + {slides} content + 1 thanks)
💰 Price: {price} sum
━━━━━━━━━━━━━━━━━━━━━━

How to create presentation plan?"""
    },
    
    "btn_plan_manual": {
        "uz": "📝 Reja kiritish (3 ta)",
        "ru": "📝 Ввести план (3 пункта)",
        "en": "📝 Enter plan (3 points)"
    },
    
    "btn_plan_auto": {
        "uz": "🤖 Avtomatik tanlash",
        "ru": "🤖 Автоматически",
        "en": "🤖 Automatic"
    },
    
    "presentation_plan_1": {
        "uz": "📝 <b>1-rejani kiriting:</b>\n\nMasalan: Kirish - Sun'iy intellektning tarixi",
        "ru": "📝 <b>Введите 1-й пункт плана:</b>\n\nНапример: Введение - История ИИ",
        "en": "📝 <b>Enter plan point 1:</b>\n\nExample: Introduction - AI History"
    },
    
    "presentation_plan_2": {
        "uz": "📝 <b>2-rejani kiriting:</b>\n\nMasalan: Asosiy qism - AI turlari va qo'llanishi",
        "ru": "📝 <b>Введите 2-й пункт плана:</b>\n\nНапример: Основная часть - Виды и применение ИИ",
        "en": "📝 <b>Enter plan point 2:</b>\n\nExample: Main part - AI types and applications"
    },
    
    "presentation_plan_3": {
        "uz": "📝 <b>3-rejani kiriting:</b>\n\nMasalan: Xulosa - Kelajak istiqbollari",
        "ru": "📝 <b>Введите 3-й пункт плана:</b>\n\nНапример: Заключение - Перспективы",
        "en": "📝 <b>Enter plan point 3:</b>\n\nExample: Conclusion - Future perspectives"
    },
    
    "progress_content": {
        "uz": "AI kontent yaratmoqda...",
        "ru": "Создание контента...",
        "en": "Generating content..."
    },
    
    "progress_template": {
        "uz": "Shablon asosida yaratilmoqda...",
        "ru": "Создание на основе шаблона...",
        "en": "Creating from template..."
    },
    
    "progress_design": {
        "uz": "Dizayn qo'llanmoqda...",
        "ru": "Применение дизайна...",
        "en": "Applying design..."
    },
    
    "progress_done": {
        "uz": "Tayyor!",
        "ru": "Готово!",
        "en": "Done!"
    },
    
    "presentation_error": {
        "uz": "❌ Taqdimot yaratishda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.",
        "ru": "❌ Ошибка при создании презентации. Пожалуйста, попробуйте снова.",
        "en": "❌ Error creating presentation. Please try again."
    },
    
    "presentation_ready": {
        "uz": "✅ Taqdimot tayyor!",
        "ru": "✅ Презентация готова!",
        "en": "✅ Presentation ready!"
    },

    # ===== ESKI MATNLAR (paket, sahifalar va hokazo) =====
    "btn_package_standard": {
        "uz": "📦 Oddiy paket",
        "ru": "📦 Стандартный пакет",
        "en": "📦 Standard package"
    },
    "btn_package_premium": {
        "uz": "⭐ Premium paket",
        "ru": "⭐ Премиум пакет",
        "en": "⭐ Premium package"
    },
    "presentation_choose_package": {
        "uz": "📦 <b>Paketni tanlang:</b>\n\n<b>Oddiy:</b> Asosiy dizayn\n<b>Premium:</b> Professional dizayn + AI rasmlar",
        "ru": "📦 <b>Выберите пакет:</b>\n\n<b>Стандарт:</b> Базовый дизайн\n<b>Премиум:</b> Профессиональный дизайн + AI изображения",
        "en": "📦 <b>Choose package:</b>\n\n<b>Standard:</b> Basic design\n<b>Premium:</b> Professional design + AI images"
    },
    "presentation_choose_slides": {
        "uz": "📄 <b>Sahifalar sonini tanlang:</b>\n\n6 dan 30 gacha",
        "ru": "📄 <b>Выберите количество слайдов:</b>\n\nОт 6 до 30",
        "en": "📄 <b>Choose number of slides:</b>\n\nFrom 6 to 30"
    },
    "presentation_choose_template": {
        "uz": "🎨 <b>Dizayn shablonini tanlang:</b>",
        "ru": "🎨 <b>Выберите шаблон дизайна:</b>",
        "en": "🎨 <b>Choose design template:</b>"
    },
    "not_enough_balance": {
        "uz": "❌ Balans yetarli emas!\n\n💰 Sizning balansingiz: {balance} so'm\n📊 Kerak: {needed} so'm\n\nIltimos, balansni to'ldiring.",
        "ru": "❌ Недостаточно средств!\n\n💰 Ваш баланс: {balance} сум\n📊 Необходимо: {needed} сум\n\nПожалуйста, пополните баланс.",
        "en": "❌ Insufficient balance!\n\n💰 Your balance: {balance} sum\n📊 Required: {needed} sum\n\nPlease top up your balance."
    },
    "balance_info": {
        "uz": "💰 <b>Balans ma'lumotlari:</b>\n\nJoriy balans: {balance} so'm\n\n📊 Narxlar:\n• Taqdimot: 3,000 - 50,000 so'm\n• Matn yozish: {text_price} so'm",
        "ru": "💰 <b>Информация о балансе:</b>\n\nТекущий баланс: {balance} сум\n\n📊 Цены:\n• Презентация: 3,000 - 50,000 сум\n• Написание текста: {text_price} сум",
        "en": "💰 <b>Balance information:</b>\n\nCurrent balance: {balance} sum\n\n📊 Prices:\n• Presentation: 3,000 - 50,000 sum\n• Text writing: {text_price} sum"
    },
    "help_text": {
        "uz": "❓ <b>Yordam:</b>\n\nBot orqali siz:\n📊 Professional taqdimot yaratishingiz\n✍️ Matn yozdirishingiz mumkin\n\nSavollar bo'lsa: @support",
        "ru": "❓ <b>Помощь:</b>\n\nЧерез бота вы можете:\n📊 Создать профессиональную презентацию\n✍️ Написать текст\n\nВопросы: @support",
        "en": "❓ <b>Help:</b>\n\nYou can:\n📊 Create professional presentations\n✍️ Write texts\n\nQuestions: @support"
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
