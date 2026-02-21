"""YANGI MATNLAR - texts.py ga qo'shish kerak"""

NEW_TEXTS = {
    # Taqdimot - yangi jarayon
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
    }
}

print("✅ Yangi matnlar tayyor - texts.py ga qo'shish kerak")
