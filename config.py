"""Bot konfiguratsiyasi"""

import os

# Telegram Bot Token
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# OpenAI API
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

# AI Model
AI_MODEL = os.environ.get("AI_MODEL", "gpt-4.1-mini")

# Pexels API (bepul stock fotolar)
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")

# Majburiy kanal obuna

MANDATORY_CHANNEL_ID = "-1003744833983"
MANDATORY_CHANNEL_LINK = "https://t.me/Ai_vazifachi"
# Admin ID (botni boshqaruvchi)
ADMIN_IDS = [int(x) for x in os.environ.get("ADMIN_IDS", "345375880").split(",")]

# Narxlar tizimi (so'mda)
NEW_USER_BALANCE = int(os.environ.get("NEW_USER_BALANCE", "15000"))

# Taqdimot paketlari (2 ta asosiy paket)
PRESENTATION_PACKAGES = {
    "standard": {
        "name_uz": "📋 Oddiy taqdimot",
        "name_ru": "📋 Обычная презентация",
        "name_en": "📋 Standard presentation",
        "has_ai_images": False,
        "has_diagrams": False,
        "description_uz": "Stock fotolar bilan professional taqdimot",
        "description_ru": "Профессиональная презентация со стоковыми фото",
        "description_en": "Professional presentation with stock photos",
    },
    "premium": {
        "name_uz": "⭐ Premium taqdimot (Rasm/Diagramma)",
        "name_ru": "⭐ Премиум презентация (Фото/Диаграммы)",
        "name_en": "⭐ Premium presentation (Images/Charts)",
        "has_ai_images": True,
        "has_diagrams": True,
        "description_uz": "AI rasmlar va diagrammalar bilan yuqori sifatli taqdimot",
        "description_ru": "Высококачественная презентация с AI изображениями и диаграммами",
        "description_en": "High-quality presentation with AI images and diagrams",
    },
}

# Sahifalar soni va narxlari (6-30 gacha)
SLIDE_COUNT_OPTIONS = {}
for i in range(6, 31):
    if i <= 10:
        std_price = 1500 + (i - 6) * 250
        prm_price = 3500 + (i - 6) * 250
    elif i <= 15:
        std_price = 2500 + (i - 10) * 100
        prm_price = 4500 + (i - 10) * 300
    elif i <= 20:
        std_price = 3000 + (i - 15) * 200
        prm_price = 6000 + (i - 15) * 200
    elif i <= 25:
        std_price = 4000 + (i - 20) * 200
        prm_price = 7000 + (i - 20) * 200
    else:
        std_price = 5000 + (i - 25) * 100
        prm_price = 8000 + (i - 25) * 100
    SLIDE_COUNT_OPTIONS[i] = {"standard": int(std_price), "premium": int(prm_price)}

# Matn yozish narxi
TEXT_WRITING_PRICE = int(os.environ.get("TEXT_WRITING_PRICE", "3000"))

# To'lov sozlamalari
PAYMENT_CARD_NUMBER = os.environ.get("PAYMENT_CARD_NUMBER", "6262 5700 3625 2213")
PAYMENT_CARD_HOLDER = os.environ.get("PAYMENT_CARD_HOLDER", "Karimov Nodir")

# Balans to'ldirish paketlari (so'mda)
BALANCE_PACKAGES = {
    "3000": {"amount": 3000, "label": "3,000 so'm"},
    "15000": {"amount": 15000, "label": "15,000 so'm"},
    "30000": {"amount": 30000, "label": "30,000 so'm"},
    "55000": {"amount": 55000, "label": "55,000 so'm"},
    "120000": {"amount": 120000, "label": "120,000 so'm"},
}

# Taqdimot dizayn shablonlari (@aislidebot uslubida)
PRESENTATION_TEMPLATES = {
    "business": {
        "name_uz": "💼 Biznes va Tadbirkorlik",
        "name_ru": "💼 Бизнес и Предпринимательство",
        "name_en": "💼 Business & Entrepreneurship",
        "color_primary": "1a365d",
        "color_secondary": "2a4365",
        "color_accent": "bee3f8",
        "color_text": "ffffff",
        "color_body": "2d3748",
    },
    "education": {
        "name_uz": "🎓 Ta'lim va Kasbiy Rivojlanish",
        "name_ru": "🎓 Образование и Развитие",
        "name_en": "🎓 Education & Development",
        "color_primary": "1a4731",
        "color_secondary": "276749",
        "color_accent": "c6f6d5",
        "color_text": "ffffff",
        "color_body": "2d3748",
    },
    "technology": {
        "name_uz": "💻 Texnologiya va IT",
        "name_ru": "💻 Технологии и IT",
        "name_en": "💻 Technology & IT",
        "color_primary": "1a202c",
        "color_secondary": "2d3748",
        "color_accent": "63b3ed",
        "color_text": "63b3ed",
        "color_body": "e2e8f0",
    },
    "medical": {
        "name_uz": "🏥 Sport, Salomatlik va Tibbiyot",
        "name_ru": "🏥 Спорт, Здоровье и Медицина",
        "name_en": "🏥 Sports, Health & Medicine",
        "color_primary": "00838F",
        "color_secondary": "00ACC1",
        "color_accent": "B2EBF2",
        "color_text": "ffffff",
        "color_body": "2d3748",
    },
    "creative": {
        "name_uz": "🎨 San'at va Madaniyat",
        "name_ru": "🎨 Искусство и Культура",
        "name_en": "🎨 Art & Culture",
        "color_primary": "553c9a",
        "color_secondary": "6b46c1",
        "color_accent": "e9d8fd",
        "color_text": "ffffff",
        "color_body": "2d3748",
    },
    "minimal": {
        "name_uz": "📋 Minimalist",
        "name_ru": "📋 Минималист",
        "name_en": "📋 Minimalist",
        "color_primary": "37474F",
        "color_secondary": "546E7A",
        "color_accent": "CFD8DC",
        "color_text": "ffffff",
        "color_body": "4a5568",
    },
    "history": {
        "name_uz": "📜 Tarix va Siyosat",
        "name_ru": "📜 История и Политика",
        "name_en": "📜 History & Politics",
        "color_primary": "7b341e",
        "color_secondary": "9c4221",
        "color_accent": "feebc8",
        "color_text": "ffffff",
        "color_body": "2d3748",
    },
    "nature": {
        "name_uz": "🌿 Atrof-muhit va Barqarorlik",
        "name_ru": "🌿 Экология и Устойчивость",
        "name_en": "🌿 Environment & Sustainability",
        "color_primary": "22543d",
        "color_secondary": "276749",
        "color_accent": "c6f6d5",
        "color_text": "ffffff",
        "color_body": "2d3748",
    },
    "entertainment": {
        "name_uz": "🎬 Ko'ngil-ochar va Media",
        "name_ru": "🎬 Развлечения и Медиа",
        "name_en": "🎬 Entertainment & Media",
        "color_primary": "702459",
        "color_secondary": "97266d",
        "color_accent": "fed7e2",
        "color_text": "ffffff",
        "color_body": "2d3748",
    },
    "personal": {
        "name_uz": "🧑‍💼 Shaxsiy Rivojlanish",
        "name_ru": "🧑‍💼 Личное Развитие",
        "name_en": "🧑‍💼 Personal Growth",
        "color_primary": "2a4365",
        "color_secondary": "2c5282",
        "color_accent": "bee3f8",
        "color_text": "ffffff",
        "color_body": "e2e8f0",
    },
}

# Ma'lumotlar bazasi
DB_PATH = os.environ.get("DB_PATH", "data/bot_database.db")
