import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "fim.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS files (
        filepath TEXT PRIMARY KEY,
        filehash TEXT,
        last_scan TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_type TEXT,
        filepath TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()
