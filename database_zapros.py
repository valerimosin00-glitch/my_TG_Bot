from datetime import datetime, time, timedelta
import sqlite3




# функция по выдаче данных 
def show_task_date(user_id, date):
    conn = sqlite3.connect(r"C:\Users\LENOVO\Desktop\програмирование\Telegrem_Bot\Bot_Finish\bot.db") 
    cur = conn.cursor()

    date_now = datetime.today()
    date_now = date_now.date()

    if date == "date_today":
        date_start = datetime.combine(date_now, time(0,0,0))
        date_stop = datetime.combine((date_now + timedelta(days=1)), time(0,0,0))
    elif date == "date_tomorrow":
        date_start = datetime.combine((date_now + timedelta(days=1)), time(0,0,0))
        date_stop = datetime.combine((date_now + timedelta(days=2)), time(0,0,0))
    elif date == "date_to_finish_week":
        date_start = datetime.combine(date_now, time(0,0,0))
        day = 8 - date_now.isoweekday()
        date_stop = datetime.combine((date_now + timedelta(days=day)), time(0,0,0))

    result = cur.execute("""
        SELECT task_id, task, due_datetime
        FROM tasks
        WHERE user_id=? and status=0 and due_datetime >= ? and due_datetime < ?
        ORDER BY due_datetime""", ((user_id, date_start, date_stop)))

    result = result.fetchall()

    conn.close()
    return result

