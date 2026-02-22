import sqlite3
import os
import sys


def get_base_path():
    # If running as PyInstaller .exe
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    # If running in development
    return os.path.dirname(os.path.abspath(__file__))


BASE_PATH = get_base_path()

DATA_FOLDER = os.path.join(BASE_PATH, "data")
os.makedirs(DATA_FOLDER, exist_ok=True)

DB_PATH = os.path.join(DATA_FOLDER, "app.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        """
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """
    )

    c.execute(
        """
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
    """
    )

    conn.commit()
    conn.close()


def get_connection():
    return sqlite3.connect(DB_PATH)
