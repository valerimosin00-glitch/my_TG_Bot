import aiogram as ai
from aiogram.filters import Command

from aiogram.fsm.state import State, StatesGroup   
from aiogram.fsm.context import FSMContext

from database_zapros import show_task_date, show_task_custom_date, show_tasks_complit
from datetime import datetime

router = ai.Router()

from buttons import keyboard_start, keyboard_task, keyboard_task_to_time, keyboard_show_task_to_time, keyboard_cancel, keyboard_task_actions


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

# Обработчик показа выполненных задач
@router.callback_query(ai.F.data == "show_task_compl")
async def show_task_complit(callback: ai.types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    result = show_tasks_complit(user_id)
    result_finall = ""
    if result == []:
        await callback.message.answer("Выполненых задач пока нет")
    else:
        for i in result:
            task_id, task, due_datetime, completed_at = i
            result_finall = result_finall + f"\n {task_id} {task} - {due_datetime}, задача выполнена {completed_at}"
        await callback.message.answer(f"Ваши задачи:\n {result_finall}", reply_markup=keyboard_task_to_time)


# Словарь для списка ID и словарь для списка с параметрами запроса
tasks_for_user= {}
option_user_show_task = {}

# вынес в отдельную функцию
async def shows_task_variant1(user_id,date, message_obj):
    result = show_task_date(user_id, date)
    result_finall = ""
    if result == []:
        await message_obj.answer("Задач пока нет")
    else:
        tasks_id = []
        for i in result:
            task_id, task, due_datetime = i
            tasks_id.append(str(task_id))
            result_finall = result_finall + f"\n {task_id} {task} - {due_datetime}"
        tasks_for_user[user_id]=tasks_id
        option_user_show_task[user_id] = [user_id,date]
        await message_obj.answer(f"Ваши задачи:\n {result_finall}", reply_markup=keyboard_task_actions)

# Обработчик просмотра задач за конкретную дату(первые 3 кнопки)
@router.callback_query(ai.F.data.startswith("date"))
async def show_task_with_deadlines(callback: ai.types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    date = callback.data
    await shows_task_variant1(user_id,date, callback.message)

# Хендлер для обработки кнопки отмена
@router.message(ai.F.text == "отменить")
async def cancel(message: ai.types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Отменено", reply_markup=keyboard_start)

# Хендлер для обработки инлайн кнопки отмена
@router.callback_query(ai.F.data == "отменить")
async def cancel(callback: ai.types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.answer("Отменено", reply_markup=keyboard_start)


# FSM для получения дат для просмотра задач за произволный период
class Show_Task_To_Custom_Period(StatesGroup):
    waiting_date_start = State()
    waiting_date_stop = State()

# Обработчик просмотра задач на произвольную дату
@router.callback_query(ai.F.data == "custom_period")
async def show_task_custom(callback: ai.types.CallbackQuery, state: FSMContext):
    
    await callback.answer()
    await state.set_state(Show_Task_To_Custom_Period.waiting_date_start)
    await callback.message.answer("Введите дату начала, например 2026-12-12 или 2026.12.12")

# Обработчик введённой даты начала
@router.message(Show_Task_To_Custom_Period.waiting_date_start)
async def start_date(message: ai.types.Message, state: FSMContext):
    date_format="%Y-%m-%d"
    date_format2 = "%Y.%m.%d"
    try:
        if "-" in message.text:
            date_start = datetime.strptime(message.text, date_format)
        else:
            date_start = datetime.strptime(message.text, date_format2)

        await state.update_data(date_start = str(date_start))
        await state.set_state(Show_Task_To_Custom_Period.waiting_date_stop)
        await message.answer("Введите дату конца, например 2026-12-12 или 2026.12.12", reply_markup=keyboard_cancel)
    except ValueError:
        await message.answer("Неправильная дата или неверный формат, попробуйте ещё раз)", reply_markup=keyboard_cancel)

# вынес в отдельную функцию 
async def shows_task_variant2(user_id,date_start, date_stop, message_obj):
    result = show_task_custom_date(user_id, date_start, date_stop)
    if result == []:
        await message_obj.answer("Задач пока нет", reply_markup=keyboard_start)
    else:
        result_finall = ""
        tasks_id = []

        for i in result:
            task_id, task, due_datetime = i
            tasks_id.append(str(task_id))
            result_finall = result_finall + f"\n {task_id} {task} - {due_datetime}"
        tasks_for_user[user_id]=tasks_id
        option_user_show_task[user_id] = [user_id,date_start,date_stop]
        await message_obj.answer(f"Ваши задачи:\n {result_finall}", reply_markup= keyboard_task_actions)


# Обработчик введённой даты завершения
@router.message(Show_Task_To_Custom_Period.waiting_date_stop)
async def date_stop(message: ai.types.Message, state: FSMContext):
    date_format="%Y-%m-%d"
    date_format2 = "%Y.%m.%d"
    try:
        if "-" in message.text:
            date_stop = datetime.strptime(message.text, date_format)
        else:
            date_stop = datetime.strptime(message.text, date_format2)

        data = await state.get_data()

        if data["date_start"] < str(date_stop):
            date_start = data["date_start"]
            date_stop = str(date_stop) 
        else:
            date_start = str(date_stop)
            date_stop = data["date_start"]
        await shows_task_variant2(message.from_user.id,date_start, date_stop, message)

        await state.clear()
    except ValueError:
        await message.answer("Неправильная дата или неверный формат, попробуйте ещё раз)", reply_markup=keyboard_cancel)

