import aiogram as ai
from datetime import datetime, time, timedelta



keyboard_start = ai.types.ReplyKeyboardMarkup(
    keyboard=[[ai.types.KeyboardButton(text="Задачи")],
    [ai.types.KeyboardButton(text="Расходы")]],
    resize_keyboard=True
)

# Инлайн клавиатура для главного обработчика задач
keyboard_task = ai.types.InlineKeyboardMarkup(
    inline_keyboard=[[ai.types.InlineKeyboardButton(text="Задачи ко времени", callback_data="task")],
              [ai.types.InlineKeyboardButton(text="Задачи без сроков", callback_data="plan")]]
)

# Инлайн клавиатура для задач ко времени
keyboard_task_to_time = ai.types.InlineKeyboardMarkup(
    inline_keyboard= [[ai.types.InlineKeyboardButton(text="Просмотр задач", callback_data="show_task")],
                [ai.types.InlineKeyboardButton(text="Добавить новую задачу", callback_data="add_task")],
                [ai.types.InlineKeyboardButton(text="Просмотр выполненных задач", callback_data="show_task_compl")]]
)

# Кнопки для просмотра задач ко времени
keyboard_show_task_to_time = ai.types.InlineKeyboardMarkup(
    inline_keyboard=[[ai.types.InlineKeyboardButton(text= "сегодня", callback_data="date_today"),
                      ai.types.InlineKeyboardButton(text="завтра", callback_data="date_tomorrow")],
                      [ai.types.InlineKeyboardButton(text="до конца недели", callback_data="date_to_finish_week")],
                      [ai.types.InlineKeyboardButton(text="за другой период", callback_data="custom_period")]]
)

# Кнопка отмены FSM
keyboard_cancel = ai.types.ReplyKeyboardMarkup(
    keyboard=[[ai.types.KeyboardButton(text="отменить")]],
    resize_keyboard=True
)

# словаро с датами для кнопок
date={}

def creat_date():
    date={}
    date_call = {}
    today = datetime.today()
    today_date = today.date()


    for i in range(1,16):
        date_add_now = f"{today_date.day}-{today_date.month}"
        key = "date" + str(i)
        date[key] = date_add_now
        date_call[key] = str(today_date)
        today_date = today_date + timedelta(days=1)

    return date, date_call

# функция каждый раз обновляет кнопки с данными
def creat_keyboard_date():
    date, date_call = creat_date()
    # кнопки с датами для добавления задачи
    keyboard_date = ai.types.InlineKeyboardMarkup(
        inline_keyboard=[[ai.types.InlineKeyboardButton(text = date["date1"], callback_data=date_call["date1"]),ai.types.InlineKeyboardButton(text = date["date2"], callback_data=date_call["date2"]),
               ai.types.InlineKeyboardButton(text = date["date3"], callback_data=date_call["date3"]),ai.types.InlineKeyboardButton(text = date["date4"], callback_data=date_call["date4"])],
               [ai.types.InlineKeyboardButton(text = date["date5"], callback_data=date_call["date5"]),ai.types.InlineKeyboardButton(text = date["date6"], callback_data=date_call["date6"]),
               ai.types.InlineKeyboardButton(text = date["date7"], callback_data=date_call["date7"]),ai.types.InlineKeyboardButton(text = date["date8"], callback_data=date_call["date8"])],
               [ai.types.InlineKeyboardButton(text = date["date9"], callback_data=date_call["date9"]),ai.types.InlineKeyboardButton(text = date["date10"], callback_data=date_call["date10"]),
               ai.types.InlineKeyboardButton(text = date["date11"], callback_data=date_call["date11"]),ai.types.InlineKeyboardButton(text = date["date12"], callback_data=date_call["date12"])],
               [ai.types.InlineKeyboardButton(text = date["date13"], callback_data=date_call["date13"]),ai.types.InlineKeyboardButton(text = date["date14"], callback_data=date_call["date14"]),
               ai.types.InlineKeyboardButton(text = date["date15"], callback_data=date_call["date15"]),ai.types.InlineKeyboardButton(text = "Другая дата", callback_data="custom_date")]]
        )

    return keyboard_date

# Выбор времени
keyboard_time = ai.types.InlineKeyboardMarkup(
    inline_keyboard=[[ai.types.InlineKeyboardButton(text="6:00", callback_data="06:00"),ai.types.InlineKeyboardButton(text="7:00", callback_data="07:00"),ai.types.InlineKeyboardButton(text="8:00", callback_data="08:00")],
                     [ai.types.InlineKeyboardButton(text="9:00", callback_data="09:00"),ai.types.InlineKeyboardButton(text="10:00", callback_data="10:00"),ai.types.InlineKeyboardButton(text="11:00", callback_data="11:00")],
                     [ai.types.InlineKeyboardButton(text="12:00", callback_data="12:00"),ai.types.InlineKeyboardButton(text="13:00", callback_data="13:00"),ai.types.InlineKeyboardButton(text="14:00", callback_data="14:00")],
                     [ai.types.InlineKeyboardButton(text="15:00", callback_data="15:00"),ai.types.InlineKeyboardButton(text="16:00", callback_data="16:00"),ai.types.InlineKeyboardButton(text="17:00", callback_data="17:00")],
                     [ai.types.InlineKeyboardButton(text="18:00", callback_data="18:00"),ai.types.InlineKeyboardButton(text="19:00", callback_data="19:00"),ai.types.InlineKeyboardButton(text="20:00", callback_data="20:00")],
                     [ai.types.InlineKeyboardButton(text="21:00", callback_data="21:00"),ai.types.InlineKeyboardButton(text="22:00", callback_data="22:00"),ai.types.InlineKeyboardButton(text="23:00", callback_data="23:00")]
                     ]
)

# Кнопки с действиями над задачами
keyboard_task_actions = ai.types.InlineKeyboardMarkup(
    inline_keyboard=[[ai.types.InlineKeyboardButton(text="Редактировать задачу", callback_data="update_task"),
                      ai.types.InlineKeyboardButton(text="Редактировать дату", callback_data="update_date")],
                      [ai.types.InlineKeyboardButton(text="Выполнено!", callback_data="task_complit"),
                       ai.types.InlineKeyboardButton(text="Удалить", callback_data="delete_task")],
                       [ai.types.InlineKeyboardButton(text="Отменить", callback_data="отменить")]]
)