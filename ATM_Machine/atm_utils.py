import random
import sqlite3
import os

ADMIN_ACCOUNT = "Admin"
ADMIN_PIN = "0000"

DATABASE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "atm-machine-api", "atm.db")

def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        raise

def create_tables():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                account_number TEXT PRIMARY KEY,
                pin INTEGER NOT NULL,
                balance REAL NOT NULL,
                full_name TEXT NOT NULL,
                address TEXT NOT NULL,
                blood_group TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_number) REFERENCES users (account_number)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                username TEXT PRIMARY KEY,
                pin INTEGER NOT NULL
            )
        """)

        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def create_admin(username, pin):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO admin (username, pin) VALUES (?, ?)", (username, pin))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating admin: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

create_tables()
create_admin(ADMIN_ACCOUNT, ADMIN_PIN)

def get_admin(username):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username = ?", (username,))
        admin = cursor.fetchone()
        return admin
    except sqlite3.Error as e:
        print(f"Error getting admin: {e}")
        raise
    finally:
        if conn:
            conn.close()

def reset_admin_pin(username, new_pin):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE admin SET pin = ? WHERE username = ?", (new_pin, username))
        conn.commit()
        print(f"PIN for Admin {username} reset successfully.")
    except sqlite3.Error as e:
        print(f"Error resetting admin PIN: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def create_user(account_number, pin, balance, full_name, address, blood_group):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (account_number, pin, balance, full_name, address, blood_group) VALUES (?, ?, ?, ?, ?, ?)",
                   (account_number, pin, balance, full_name, address, blood_group))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating user: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def get_user(account_number):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE account_number = ?", (account_number,))
        user = cursor.fetchone()
        return user
    except sqlite3.Error as e:
        print(f"Error getting user: {e}")
        raise
    finally:
        if conn:
            conn.close()

def update_user_balance(account_number, new_balance):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance = ? WHERE account_number = ?", (new_balance, account_number))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating user balance: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def get_user_balance(account_number):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE account_number = ?", (account_number,))
        balance = cursor.fetchone()
        return balance['balance'] if balance else None
    except sqlite3.Error as e:
        print(f"Error getting user balance: {e}")
        raise
    finally:
        if conn:
            conn.close()

def record_transaction(account_number, transaction_type, amount):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (account_number, transaction_type, amount) VALUES (?, ?, ?)",
                   (account_number, transaction_type, amount))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error recording transaction: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def get_transaction_history(account_number):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE account_number = ? ORDER BY timestamp DESC", (account_number,))
        transactions = cursor.fetchall()
        return transactions
    except sqlite3.Error as e:
        print(f"Error getting transaction history: {e}")
        raise
    finally:
        if conn:
            conn.close()

def my_decorator(function):
    def wrapper(*args, **kwargs):
        print(f"\n--- {function.__name__.replace('_', ' ')} ---")
        result = function(*args, **kwargs)
        return result
    return wrapper

def generate_otp():
    """Generate a random 6-digit OTP code."""
    return str(random.randint(100000, 999999))
