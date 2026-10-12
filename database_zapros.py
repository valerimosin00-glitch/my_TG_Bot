from datetime import datetime, time, timedelta
import sqlite3




# функция по выдаче данных 
def show_task_date(user_id, date):
    conn = sqlite3.connect(r"C:\Users\LENOVO\Desktop\програмирование\Telegrem_Bot\Bot_Finish\bot.db") 
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

    result = cur.execute("""
        SELECT task_id, task, due_datetime
        FROM tasks
        WHERE user_id=? and status=0 and due_datetime >= ? and due_datetime < ?
        ORDER BY due_datetime""", ((user_id, date_start, date_stop)))

    result = result.fetchall()

    conn.close()
    return result

def show_task_custom_date(user_id, date_start, date_stop):
    conn = sqlite3.connect(r"C:\Users\LENOVO\Desktop\програмирование\Telegrem_Bot\Bot_Finish\bot.db") 
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
    conn = sqlite3.connect(r"C:\Users\LENOVO\Desktop\програмирование\Telegrem_Bot\Bot_Finish\bot.db") 
    cur = conn.cursor()


    cur.execute("""
        INSERT INTO tasks (user_id, task, due_datetime, created_at)
        VALUES (?,?,?,?)
        """, ((user_id, task, due_datetime, created_at)))

    conn.commit()
    conn.close()

    return "Запись добавлена"


def update_text_task(task, task_id):
    conn = sqlite3.connect(r"C:\Users\LENOVO\Desktop\програмирование\Telegrem_Bot\Bot_Finish\bot.db") 
    cur = conn.cursor()    

    cur.execute("""
        UPDATE tasks
        SET task = ?
        WHERE task_id = ?""", (task, task_id))
    conn.commit()
    conn.close()
    
def update_date_task(task_id, date):
    conn = sqlite3.connect(r"C:\Users\LENOVO\Desktop\програмирование\Telegrem_Bot\Bot_Finish\bot.db") 
    cur = conn.cursor() 

    cur.execute("""
        UPDATE tasks
        SET due_datetime = ?
        WHERE task_id = ?""", (date, task_id))

    conn.commit()
    conn.close()    

def update_status_task(task_id):
    conn = sqlite3.connect(r"C:\Users\LENOVO\Desktop\програмирование\Telegrem_Bot\Bot_Finish\bot.db") 
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
    conn = sqlite3.connect(r"C:\Users\LENOVO\Desktop\програмирование\Telegrem_Bot\Bot_Finish\bot.db") 
    cur = conn.cursor() 

    cur.execute("""
        DELETE FROM tasks
        WHERE task_id = ?""", (task_id,))

    conn.commit()
    conn.close()  


def show_tasks_complit(user_id):
    conn = sqlite3.connect(r"C:\Users\LENOVO\Desktop\програмирование\Telegrem_Bot\Bot_Finish\bot.db") 
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
    conn = sqlite3.connect(r"C:\Users\LENOVO\Desktop\програмирование\Telegrem_Bot\Bot_Finish\bot.db") 
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
    conn = sqlite3.connect(r"C:\Users\LENOVO\Desktop\програмирование\Telegrem_Bot\Bot_Finish\bot.db") 
    cur = conn.cursor()
    date_creat = str(datetime.now().strftime("%Y-%m-%d %H:%M"))

    cur.execute("""
        INSERT INTO plans (user_id, task, created_at)
        VALUES (?,?,?)
        """, ((user_id, task, date_creat)))

    conn.commit()
    conn.close()

def show_task_complit_no_time(user_id):
    conn = sqlite3.connect(r"C:\Users\LENOVO\Desktop\програмирование\Telegrem_Bot\Bot_Finish\bot.db") 
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
    conn = sqlite3.connect(r"C:\Users\LENOVO\Desktop\програмирование\Telegrem_Bot\Bot_Finish\bot.db") 
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
    conn = sqlite3.connect(r"C:\Users\LENOVO\Desktop\програмирование\Telegrem_Bot\Bot_Finish\bot.db") 
    cur = conn.cursor() 

    cur.execute("""
        DELETE FROM plans
        WHERE plan_id = ?""", (plan_id,))

    conn.commit()
    conn.close()  

def update_text_task_no_time(task, plan_id):
    conn = sqlite3.connect(r"C:\Users\LENOVO\Desktop\програмирование\Telegrem_Bot\Bot_Finish\bot.db") 
    cur = conn.cursor()    

    cur.execute("""
        UPDATE plans
        SET task = ?
        WHERE plan_id = ?""", (task, plan_id))
    conn.commit()
    conn.close()