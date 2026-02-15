"""Ma'lumotlar bazasi boshqaruvi"""

import sqlite3
import os
from datetime import datetime
from config import DB_PATH, NEW_USER_BALANCE


def get_db():
    """Ma'lumotlar bazasiga ulanish"""
    db_dir = os.path.dirname(DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Ma'lumotlar bazasini yaratish"""
    conn = get_db()
    cursor = conn.cursor()

    # Foydalanuvchilar jadvali
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            language TEXT DEFAULT 'uz',
            balance INTEGER DEFAULT 0,
            total_tasks INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            last_active TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # To'lovlar jadvali
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

    # Vazifalar jadvali
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            task_type TEXT,
            topic TEXT,
            language TEXT,
            status TEXT DEFAULT 'pending',
            result_file TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            completed_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    conn.commit()
    conn.close()


def get_user(user_id: int):
    """Foydalanuvchini olish"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def create_user(user_id: int, username: str, full_name: str):
    """Yangi foydalanuvchi yaratish"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, username, full_name, balance) VALUES (?, ?, ?, ?)",
        (user_id, username, full_name, NEW_USER_BALANCE)
    )
    conn.commit()
    conn.close()


def update_user_language(user_id: int, language: str):
    """Foydalanuvchi tilini yangilash"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET language = ? WHERE user_id = ?", (language, user_id))
    conn.commit()
    conn.close()


def get_user_balance(user_id: int) -> int:
    """Foydalanuvchi balansini olish (so'mda)"""
    user = get_user(user_id)
    if user:
        return user["balance"]
    return 0


def update_balance(user_id: int, amount: int):
    """Balansni yangilash (+ yoki -)"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET balance = balance + ? WHERE user_id = ?",
        (amount, user_id)
    )
    conn.commit()
    conn.close()


def deduct_balance(user_id: int, amount: int) -> bool:
    """Balansdan yechish. Yetarli bo'lsa True qaytaradi."""
    current = get_user_balance(user_id)
    if current >= amount:
        update_balance(user_id, -amount)
        return True
    return False


def increment_tasks(user_id: int):
    """Bajarilgan vazifalar sonini oshirish"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET total_tasks = total_tasks + 1, last_active = ? WHERE user_id = ?",
        (datetime.now().isoformat(), user_id)
    )
    conn.commit()
    conn.close()


def create_payment(user_id: int, amount: int, receipt_photo: str) -> int:
    """To'lov yaratish"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO payments (user_id, amount, receipt_photo) VALUES (?, ?, ?)",
        (user_id, amount, receipt_photo)
    )
    payment_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return payment_id


def get_pending_payments():
    """Kutilayotgan to'lovlarni olish"""
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
    """To'lovni tasdiqlash"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE payments SET status = 'approved', reviewed_at = ?, reviewed_by = ? WHERE id = ?",
        (datetime.now().isoformat(), admin_id, payment_id)
    )
    # Balansga qo'shish
    cursor.execute("SELECT user_id, amount FROM payments WHERE id = ?", (payment_id,))
    payment = cursor.fetchone()
    if payment:
        cursor.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ?",
            (payment["amount"], payment["user_id"])
        )
    conn.commit()
    conn.close()
    return payment


def reject_payment(payment_id: int, admin_id: int):
    """To'lovni rad etish"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE payments SET status = 'rejected', reviewed_at = ?, reviewed_by = ? WHERE id = ?",
        (datetime.now().isoformat(), admin_id, payment_id)
    )
    cursor.execute("SELECT user_id FROM payments WHERE id = ?", (payment_id,))
    payment = cursor.fetchone()
    conn.commit()
    conn.close()
    return payment


def create_task(user_id: int, task_type: str, topic: str, language: str) -> int:
    """Vazifa yaratish"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (user_id, task_type, topic, language) VALUES (?, ?, ?, ?)",
        (user_id, task_type, topic, language)
    )
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id


def complete_task(task_id: int, result_file: str):
    """Vazifani yakunlash"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET status = 'completed', result_file = ?, completed_at = ? WHERE id = ?",
        (result_file, datetime.now().isoformat(), task_id)
    )
    conn.commit()
    conn.close()


def get_all_users_count() -> int:
    """Barcha foydalanuvchilar sonini olish"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_all_users():
    """Barcha foydalanuvchilarni olish"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
    users = cursor.fetchall()
    conn.close()
    return users


def get_stats():
    """Statistikani olish"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'completed'")
    total_tasks = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM payments WHERE status = 'approved'")
    total_payments = cursor.fetchone()[0]
    
    cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM payments WHERE status = 'approved'")
    total_revenue = cursor.fetchone()[0]
    
    conn.close()
    return {
        "total_users": total_users,
        "total_tasks": total_tasks,
        "total_payments": total_payments,
        "total_revenue": total_revenue
    }
