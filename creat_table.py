import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "bot.db"

conn = sqlite3.connect(DB_PATH) 

cur = conn.cursor()


cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
    task_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    task TEXT,
    due_datetime TEXT,
    status INTEGER DEFAULT 0,
    postponed_count INTEGER DEFAULT 0,
    created_at TEXT,
    completed_at TEXT)""")


cur.execute("""
    CREATE TABLE IF NOT EXISTS plans(
    plan_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    task TEXT,
    status INTEGER DEFAULT 0,
    created_at TEXT,
    completed_at TEXT)""")

conn.commit()
conn.close()