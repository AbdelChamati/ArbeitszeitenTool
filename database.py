import sqlite3
import os

os.makedirs("data", exist_ok=True)
DB_PATH = "data/app.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS work_entries(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        start TEXT,
        end TEXT,
        worked REAL,
        overtime REAL,
        income REAL
    )
    """)

    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_PATH)