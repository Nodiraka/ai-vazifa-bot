"""Ma'lumotlar bazasi boshqaruvi — PostgreSQL (Railway) + SQLite (local) """

import os
import logging
from datetime import datetime
from config import NEW_USER_BALANCE

logger = logging.getLogger(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL", "")
USE_POSTGRES = bool(DATABASE_URL)

if USE_POSTGRES:
    import psycopg2
    import psycopg2.extras
    logger.info("✅ PostgreSQL ishlatilmoqda")
else:
    import sqlite3
    DB_PATH = os.environ.get("DB_PATH", "data/bot_database.db")
    logger.info("✅ SQLite ishlatilmoqda (local)")


def get_db():
    if USE_POSTGRES:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
        return conn
    else:
        db_dir = os.path.dirname(DB_PATH)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn


def ph():
    return "%s" if USE_POSTGRES else "?"


def placeholder(n=1):
    p = "%s" if USE_POSTGRES else "?"
    return ",".join([p] * n)


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    if USE_POSTGRES:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
                username TEXT DEFAULT '',
                full_name TEXT DEFAULT '',
                language TEXT DEFAULT 'uz',
                balance INTEGER DEFAULT 0,
                total_tasks INTEGER DEFAULT 0,
                referral_code TEXT UNIQUE,
                referred_by BIGINT DEFAULT NULL,
                referral_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT NOW(),
                last_active TIMESTAMP DEFAULT NOW()
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id SERIAL PRIMARY KEY,
                user_id BIGINT REFERENCES users(user_id),
                amount INTEGER,
                receipt_photo TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT NOW(),
                reviewed_at TIMESTAMP,
                reviewed_by BIGINT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                user_id BIGINT REFERENCES users(user_id),
                task_type TEXT,
                topic TEXT,
                language TEXT,
                status TEXT DEFAULT 'completed',
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT DEFAULT '',
                full_name TEXT DEFAULT '',
                language TEXT DEFAULT 'uz',
                balance INTEGER DEFAULT 0,
                total_tasks INTEGER DEFAULT 0,
                referral_code TEXT UNIQUE,
                referred_by INTEGER DEFAULT NULL,
                referral_count INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_active TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount INTEGER,
                receipt_photo TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                reviewed_at TEXT,
                reviewed_by INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                task_type TEXT,
                topic TEXT,
                language TEXT,
                status TEXT DEFAULT 'completed',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

    conn.commit()
    conn.close()
    logger.info("✅ Database jadvallar tayyor")


def _generate_referral_code(user_id: int) -> str:
    import hashlib
    return hashlib.md5(str(user_id).encode()).hexdigest()[:8].upper()


def get_user(user_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE user_id = {ph()}", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def create_user(user_id: int, username: str, full_name: str, referred_by: int = None):
    conn = get_db()
    cursor = conn.cursor()
    ref_code = _generate_referral_code(user_id)
    if USE_POSTGRES:
        cursor.execute("""
            INSERT INTO users (user_id, username, full_name, balance, referral_code, referred_by)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO NOTHING
        """, (user_id, username, full_name, NEW_USER_BALANCE, ref_code, referred_by))
    else:
        cursor.execute("""
            INSERT OR IGNORE INTO users (user_id, username, full_name, balance, referral_code, referred_by)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, username, full_name, NEW_USER_BALANCE, ref_code, referred_by))
    conn.commit()
    conn.close()


def update_user_language(user_id: int, language: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET language = {ph()} WHERE user_id = {ph()}", (language, user_id))
    conn.commit()
    conn.close()


def get_user_balance(user_id: int) -> int:
    user = get_user(user_id)
    return user["balance"] if user else 0


def update_balance(user_id: int, amount: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET balance = balance + {ph()} WHERE user_id = {ph()}", (amount, user_id))
    conn.commit()
    conn.close()


def deduct_balance(user_id: int, amount: int) -> bool:
    current = get_user_balance(user_id)
    if current >= amount:
        update_balance(user_id, -amount)
        return True
    return False


def increment_tasks(user_id: int):
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().isoformat() if not USE_POSTGRES else datetime.now()
    cursor.execute(
        f"UPDATE users SET total_tasks = total_tasks + 1, last_active = {ph()} WHERE user_id = {ph()}",
        (now, user_id)
    )
    conn.commit()
    conn.close()


def save_task(user_id: int, task_type: str, topic: str, language: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO tasks (user_id, task_type, topic, language) VALUES ({placeholder(4)})",
        (user_id, task_type, topic, language)
    )
    conn.commit()
    conn.close()


def get_user_tasks(user_id: int, limit: int = 10):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM tasks WHERE user_id = {ph()} ORDER BY created_at DESC LIMIT {ph()}",
        (user_id, limit)
    )
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def create_payment(user_id: int, amount: int, receipt_photo: str) -> int:
    conn = get_db()
    cursor = conn.cursor()
    if USE_POSTGRES:
        cursor.execute(
            "INSERT INTO payments (user_id, amount, receipt_photo) VALUES (%s, %s, %s) RETURNING id",
            (user_id, amount, receipt_photo)
        )
        payment_id = cursor.fetchone()["id"]
    else:
        cursor.execute(
            "INSERT INTO payments (user_id, amount, receipt_photo) VALUES (?, ?, ?)",
            (user_id, amount, receipt_photo)
        )
        payment_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return payment_id


def get_pending_payments():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.*, u.username, u.full_name 
        FROM payments p 
        JOIN users u ON p.user_id = u.user_id 
        WHERE p.status = 'pending' 
        ORDER BY p.created_at DESC
    """)
    payments = cursor.fetchall()
    conn.close()
    return payments


def approve_payment(payment_id: int, admin_id: int):
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().isoformat() if not USE_POSTGRES else datetime.now()
    cursor.execute(
        f"UPDATE payments SET status='approved', reviewed_at={ph()}, reviewed_by={ph()} WHERE id={ph()}",
        (now, admin_id, payment_id)
    )
    cursor.execute(f"SELECT user_id, amount FROM payments WHERE id = {ph()}", (payment_id,))
    payment = cursor.fetchone()
    if payment:
        cursor.execute(
            f"UPDATE users SET balance = balance + {ph()} WHERE user_id = {ph()}",
            (payment["amount"], payment["user_id"])
        )
    conn.commit()
    conn.close()
    return payment


def reject_payment(payment_id: int, admin_id: int):
    conn = get_db()
    cursor = conn.cursor()
    now = datetime.now().isoformat() if not USE_POSTGRES else datetime.now()
    cursor.execute(
        f"UPDATE payments SET status='rejected', reviewed_at={ph()}, reviewed_by={ph()} WHERE id={ph()}",
        (now, admin_id, payment_id)
    )
    cursor.execute(f"SELECT user_id FROM payments WHERE id = {ph()}", (payment_id,))
    payment = cursor.fetchone()
    conn.commit()
    conn.close()
    return payment


def get_all_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
    users = cursor.fetchall()
    conn.close()
    return users


def get_all_users_count() -> int:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as cnt FROM users")
    result = cursor.fetchone()
    conn.close()
    return result["cnt"] if result else 0


def get_stats() -> dict:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as cnt FROM users")
    total_users = cursor.fetchone()["cnt"]
    cursor.execute("SELECT COUNT(*) as cnt FROM tasks WHERE status = 'completed'")
    total_tasks = cursor.fetchone()["cnt"]
    cursor.execute("SELECT COUNT(*) as cnt FROM payments WHERE status = 'approved'")
    total_payments = cursor.fetchone()["cnt"]
    cursor.execute("SELECT COALESCE(SUM(amount), 0) as total FROM payments WHERE status = 'approved'")
    total_revenue = cursor.fetchone()["total"]
    cursor.execute("SELECT COUNT(*) as cnt FROM users WHERE referred_by IS NOT NULL")
    total_referrals = cursor.fetchone()["cnt"]
    conn.close()
    return {
        "total_users": total_users,
        "total_tasks": total_tasks,
        "total_payments": total_payments,
        "total_revenue": total_revenue,
        "total_referrals": total_referrals,
    }


def get_user_by_referral_code(code: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE referral_code = {ph()}", (code.upper(),))
    user = cursor.fetchone()
    conn.close()
    return user


def add_referral_bonus(referrer_id: int, bonus: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE users SET balance = balance + {ph()}, referral_count = referral_count + 1 WHERE user_id = {ph()}",
        (bonus, referrer_id)
    )
    conn.commit()
    conn.close()
