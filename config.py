"""Bot konfiguratsiyasi"""

import os

# Telegram Bot Token
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# OpenAI API
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", None)

# AI Model
AI_MODEL = os.environ.get("AI_MODEL", "gpt-4.1-mini")

# Majburiy kanal obuna
MANDATORY_CHANNEL_ID = int(os.environ.get("MANDATORY_CHANNEL_ID", "-1003627690761"))
MANDATORY_CHANNEL_LINK = os.environ.get("MANDATORY_CHANNEL_LINK", "https://t.me/Ai_vazifachi")

# Admin ID (botni boshqaruvchi)
ADMIN_IDS = [int(x) for x in os.environ.get("ADMIN_IDS", "345375880").split(",")]

# Narxlar tizimi (so'mda)
NEW_USER_BALANCE = int(os.environ.get("NEW_USER_BALANCE", "15000"))
PRESENTATION_PRICE = int(os.environ.get("PRESENTATION_PRICE", "6000"))
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

# Ma'lumotlar bazasi
DB_PATH = os.environ.get("DB_PATH", "data/bot_database.db")
