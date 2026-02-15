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
MANDATORY_CHANNEL_ID = int(os.environ.get("MANDATORY_CHANNEL_ID", "-1003627690761"))
MANDATORY_CHANNEL_LINK = os.environ.get("MANDATORY_CHANNEL_LINK", "https://t.me/Ai_vazifachi")

# Admin ID (botni boshqaruvchi)
ADMIN_IDS = [int(x) for x in os.environ.get("ADMIN_IDS", "345375880").split(",")]

# Narxlar tizimi (so'mda)
NEW_USER_BALANCE = int(os.environ.get("NEW_USER_BALANCE", "15000"))

# Taqdimot narxlari
PRESENTATION_PRICES = {
    "standard_15": {"price": 3000, "max_slides": 15, "label": "Oddiy (15 gacha)", "has_ai_images": False},
    "standard_25": {"price": 5000, "max_slides": 25, "label": "Oddiy (25 gacha)", "has_ai_images": False},
    "premium_15": {"price": 6000, "max_slides": 15, "label": "Premium (15 gacha)", "has_ai_images": True},
    "premium_25": {"price": 8000, "max_slides": 25, "label": "Premium (25 gacha)", "has_ai_images": True},
}

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

# Taqdimot shablonlari
PRESENTATION_TEMPLATES = {
    "business": {"name_uz": "Biznes", "name_ru": "Бизнес", "name_en": "Business",
                 "color_primary": "1F4E79", "color_secondary": "2E75B6", "color_accent": "BDD7EE", "color_text": "FFFFFF"},
    "education": {"name_uz": "Ta'lim", "name_ru": "Образование", "name_en": "Education",
                  "color_primary": "2E7D32", "color_secondary": "43A047", "color_accent": "C8E6C9", "color_text": "FFFFFF"},
    "technology": {"name_uz": "Texnologiya", "name_ru": "Технологии", "name_en": "Technology",
                   "color_primary": "283593", "color_secondary": "3949AB", "color_accent": "C5CAE9", "color_text": "FFFFFF"},
    "medical": {"name_uz": "Tibbiyot", "name_ru": "Медицина", "name_en": "Medical",
                "color_primary": "00838F", "color_secondary": "00ACC1", "color_accent": "B2EBF2", "color_text": "FFFFFF"},
    "creative": {"name_uz": "Ijodiy", "name_ru": "Креативный", "name_en": "Creative",
                 "color_primary": "6A1B9A", "color_secondary": "8E24AA", "color_accent": "E1BEE7", "color_text": "FFFFFF"},
    "minimal": {"name_uz": "Minimalist", "name_ru": "Минималист", "name_en": "Minimal",
                "color_primary": "37474F", "color_secondary": "546E7A", "color_accent": "CFD8DC", "color_text": "FFFFFF"},
}

# Ma'lumotlar bazasi
DB_PATH = os.environ.get("DB_PATH", "data/bot_database.db")
