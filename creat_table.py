import sqlite3

conn = sqlite3.connect(r"C:\Users\LENOVO\Desktop\програмирование\Telegrem_Bot\Bot_Finish\bot.db") 

cur = conn.cursor()


cur.execute("""
    CREATE TABLE tasks(
    task_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    task TEXT,
    due_datetime TEXT,
    status TEXT DEFAULT 0,
    postponed_count INTEGER DEFAULT 0,
    created_at TEXT)""")


cur.execute("""
    CREATE TABLE plans(
    plan_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    task TEXT,
    status TEXT,
    created_at TEXT)""")

conn.commit()
conn.close()