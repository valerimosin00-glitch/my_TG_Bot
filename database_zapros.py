from datetime import datetime, time, timedelta
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "bot.db"

# Функция для получения всех ID 
def get_tasks_for_notifications():
    conn = sqlite3.connect(DB_PATH) 
    cur = conn.cursor()
    today = datetime.today()
    dt_now = today.strftime("%Y-%m-%d %H:%M")
    dt_in_advance = (today + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")
    result = cur.execute("""
        SELECT user_id, task, due_datetime
        FROM tasks
        WHERE due_datetime = ? OR due_datetime = ? AND status = 0""", (dt_now, dt_in_advance))

    result = result.fetchall()
    start = []
    before = []
    for i in result:
        if dt_now == i[-1]:
            start.append(i)
        else:
            before.append(i)
    result_finall = {"start": start,"before":before }

    conn.close()
    return result_finall

# функция по выдаче данных 
def show_task_date(user_id, date):
    conn = sqlite3.connect(DB_PATH) 
    cur = conn.cursor()

    date_now = datetime.today()
    date_now = date_now.date()

    if date == "date_today":
        date_start = datetime.combine(date_now, time(0,0))
        date_stop = datetime.combine((date_now + timedelta(days=1)), time(0,0))
    elif date == "date_tomorrow":
        date_start = datetime.combine((date_now + timedelta(days=1)), time(0,0))
        date_stop = datetime.combine((date_now + timedelta(days=2)), time(0,0))
    elif date == "date_to_finish_week":
        date_start = datetime.combine(date_now, time(0,0))
        day = 8 - date_now.isoweekday()
        date_stop = datetime.combine((date_now + timedelta(days=day)), time(0,0))

    date_start = date_start.strftime("%Y-%m-%d %H:%M")
    date_stop = date_stop.strftime("%Y-%m-%d %H:%M")

    result = cur.execute("""
        SELECT task_id, task, due_datetime
        FROM tasks
        WHERE user_id=? and status=0 and due_datetime >= ? and due_datetime < ?
        ORDER BY due_datetime""", (user_id, date_start, date_stop))

    result = result.fetchall()

    conn.close()
    return result

def show_task_custom_date(user_id, date_start, date_stop):
    conn = sqlite3.connect(DB_PATH) 
    cur = conn.cursor()

    result = cur.execute("""
        SELECT task_id, task, due_datetime
        FROM tasks
        WHERE user_id=? and status=0 and due_datetime >= ? and due_datetime < ?
        ORDER BY due_datetime""", ((user_id, date_start, date_stop)))

    result = result.fetchall()

    conn.close()
    return result

"""
    CREATE TABLE tasks(
    task_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    task TEXT,
    due_datetime TEXT,
    status TEXT DEFAULT 0,
    postponed_count INTEGER DEFAULT 0,
    created_at TEXT
    completed_at TEXT)"""

def add_tasks(user_id, task, due_datetime, created_at):
    conn = sqlite3.connect(DB_PATH) 
    cur = conn.cursor()


    cur.execute("""
        INSERT INTO tasks (user_id, task, due_datetime, created_at)
        VALUES (?,?,?,?)
        """, (user_id, task, due_datetime, created_at))

    conn.commit()
    conn.close()

    return "Запись добавлена"


def update_text_task(task, task_id):
    conn = sqlite3.connect(DB_PATH) 
    cur = conn.cursor()    

    cur.execute("""
        UPDATE tasks
        SET task = ?
        WHERE task_id = ?""", (task, task_id))
    conn.commit()
    conn.close()
    
def update_date_task(task_id, date):
    conn = sqlite3.connect(DB_PATH) 
    cur = conn.cursor() 

    cur.execute("""
        UPDATE tasks
        SET due_datetime = ?
        WHERE task_id = ?""", (date, task_id))

    conn.commit()
    conn.close()    

def update_status_task(task_id):
    conn = sqlite3.connect(DB_PATH) 
    cur = conn.cursor() 

    date = datetime.today()
    date = str(date.date())

    cur.execute("""
        UPDATE tasks
        SET status = 1, completed_at = ?
        WHERE task_id = ?""", (date,task_id))

    conn.commit()
    conn.close()    


def delete_task(task_id):
    conn = sqlite3.connect(DB_PATH) 
    cur = conn.cursor() 

    cur.execute("""
        DELETE FROM tasks
        WHERE task_id = ?""", (task_id,))

    conn.commit()
    conn.close()  


def show_tasks_complit(user_id):
    conn = sqlite3.connect(DB_PATH) 
    cur = conn.cursor() 

    result = cur.execute("""
        SELECT task_id, task, due_datetime, completed_at
        FROM tasks
        WHERE user_id = ? and status = 1
        ORDER BY completed_at DESC
        """, (user_id,))
    result = result.fetchall()
    conn.close()  
    return result


"""
    CREATE TABLE plans(
    plan_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    task TEXT,
    status TEXT DEFAUT 0,
    created_at TEXT,
    comleted_at TEXT)"""

def show_task_no_time(user_id):
    conn = sqlite3.connect(DB_PATH) 
    cur = conn.cursor() 

    result = cur.execute("""
        SELECT plan_id, task
        FROM plans
        WHERE user_id = ? and status = 0
        ORDER BY created_at DESC""", (user_id,))    

    result = result.fetchall()
    conn.close()
    return result

def no_time_add_tasks(user_id, task):
    conn = sqlite3.connect(DB_PATH) 
    cur = conn.cursor()
    date_creat = str(datetime.now().strftime("%Y-%m-%d %H:%M"))

    cur.execute("""
        INSERT INTO plans (user_id, task, created_at)
        VALUES (?,?,?)
        """, ((user_id, task, date_creat)))

    conn.commit()
    conn.close()

def show_task_complit_no_time(user_id):
    conn = sqlite3.connect(DB_PATH) 
    cur = conn.cursor()
    result = cur.execute("""
        SELECT plan_id, task
        FROM plans
        WHERE user_id = ? and status = 1
        ORDER BY created_at DESC""", (user_id,))    

    result = result.fetchall()
    conn.close()
    return result


def update_status_task_no_time(plan_id):
    conn = sqlite3.connect(DB_PATH) 
    cur = conn.cursor() 

    date = datetime.today()
    date = str(date.date())

    cur.execute("""
        UPDATE plans
        SET status = 1, completed_at = ?
        WHERE plan_id = ?""", (date,plan_id))

    conn.commit()
    conn.close()    

def delete_task_no_time(plan_id):
    conn = sqlite3.connect(DB_PATH) 
    cur = conn.cursor() 

    cur.execute("""
        DELETE FROM plans
        WHERE plan_id = ?""", (plan_id,))

    conn.commit()
    conn.close()  

def update_text_task_no_time(task, plan_id):
    conn = sqlite3.connect(DB_PATH) 
    cur = conn.cursor()    

    cur.execute("""
        UPDATE plans
        SET task = ?
        WHERE plan_id = ?""", (task, plan_id))
    conn.commit()
    conn.close()


"""
    CREATE TABLE IF NOT EXISTS expense(
    expense_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    amount REAL,
    category TEXT ,
    expense_date TEXT,
    description TEXT)"""

# Функция для добавления расхода
def add_expence(user_id, amount, category, expense_date,description ):
    conn = sqlite3.connect(DB_PATH) 
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO expense (user_id, amount, category, expense_date,description)
        VALUES (?,?,?,?,?)
        """, (user_id, amount, category, expense_date,description))

    conn.commit()
    conn.close()

# Функция для просмотра расходов за период времени
def show_expence_two_date(user_id, date_start, date_stop):
    conn = sqlite3.connect(DB_PATH) 
    cur = conn.cursor()

    result = cur.execute("""
        SELECT expense_id, amount, category, expense_date, description
        FROM expense
        WHERE user_id=? and expense_date >= ? and expense_date <= ?
        ORDER BY expense_date""", (user_id, date_start, date_stop))

    result = result.fetchall()
    result_finall = ""
    for i in result:
        result_finall = result_finall + f" ID:{i[0]}, {i[1]} {i[2]} {i[3]} {i[4]} \n" 

    conn.close()
    return result_finall    

# Функция просмотра расходов зв 1 день
def show_expence_one_date(user_id, date):
    conn = sqlite3.connect(DB_PATH) 
    cur = conn.cursor()

    result = cur.execute("""
        SELECT expense_id, amount, category, expense_date, description
        FROM expense
        WHERE user_id=? and expense_date = ?
        ORDER BY expense_date""", (user_id, date))

    result = result.fetchall()
    result_finall = ""
    for i in result:
        result_finall = result_finall + f" ID:{i[0]}, {i[1]} {i[2]} {i[3]} {i[4]} \n" 

    conn.close()
    return result_finall 