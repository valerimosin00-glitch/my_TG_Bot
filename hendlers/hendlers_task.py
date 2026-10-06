import aiogram as ai
from aiogram.filters import Command

from aiogram.fsm.state import State, StatesGroup   
from aiogram.fsm.context import FSMContext

from database_zapros import show_task_date

router = ai.Router()

# Основная панель кнопок, потом перенести в отдельный файл
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
                [ai.types.InlineKeyboardButton(text="Добавить новую задачу", callback_data="add_task")]]
)

# Кнопки для просмотра задач ко времени
keyboard_show_task_to_time = ai.types.InlineKeyboardMarkup(
    inline_keyboard=[[ai.types.InlineKeyboardButton(text= "сегодня", callback_data="date_today"),
                      ai.types.InlineKeyboardButton(text="завтра", callback_data="date_tomorrow")],
                      [ai.types.InlineKeyboardButton(text="до конца недели", callback_data="date_to_finish_week")],
                      [ai.types.InlineKeyboardButton(text="за другой период", callback_data="custom_period")]]
)

# Первый хендлер
@router.message(Command("start"))
async def start(message: ai.types.Message):
    await message.answer("Привет! Выбери действие:", reply_markup=keyboard_start)


# Временная заглушка для ветки расходов, потом будет перенесена в отдельный файл и доработана
@router.message(ai.F.text == "Расходы")
async def expenses(message: ai.types.Message):
    await message.answer("Скоро появится") 


# главный обработчик задач
@router.message(ai.F.text == "Задачи")
async def tasks(message: ai.types.Message):
    await message.answer("Какие задачи вам нужны?", reply_markup=keyboard_task )


# обработчик задач ко времени
@router.callback_query(ai.F.data == "task")
async def tast_to_time(callback: ai.types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Выберите действие", reply_markup=keyboard_task_to_time)

# Обработчик просмотра задач ко времени
@router.callback_query(ai.F.data == "show_task")
async def show_task_to_time(callback: ai.types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("За какой период нужно показать задачи", reply_markup=keyboard_show_task_to_time)

# Обработчик просмотра задач за конкретную дату(первые 3 кнопки)
@router.callback_query(ai.F.data.startswith("date"))
async def show_task_with_deadlines(callback: ai.types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    date = callback.data
    result = show_task_date(user_id, date)
    result_finall = ""
    if result == []:
        await callback.message.answer("Задач пока нет")
    else:
        for i in result:
            task_id, task, due_datetime = i
            result_finall = result_finall + f"\n {task_id} {task} - {due_datetime}"
        await callback.message.answer(f"Ваши задачи:\n {result_finall}")