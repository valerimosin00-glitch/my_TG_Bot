import aiogram as ai
from aiogram.filters import Command

from aiogram.fsm.state import State, StatesGroup   
from aiogram.fsm.context import FSMContext

from database_zapros import show_task_date, show_task_custom_date
from datetime import datetime

router = ai.Router()

from buttons import keyboard_start, keyboard_task, keyboard_task_to_time, keyboard_show_task_to_time, keyboard_cancel


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

# Хендлер для обработки кнопки отмена
@router.message(ai.F.text == "отменить")
async def cancel(message: ai.types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Отменено", reply_markup=keyboard_start)


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

        result = show_task_custom_date(message.from_user.id, date_start, date_stop)
        if result == []:
            await message.answer("Задач пока нет", reply_markup=keyboard_start)
            await state.clear()
        else:
            result_finall = ""
            for i in result:
                task_id, task, due_datetime = i
                result_finall = result_finall + f"\n {task_id} {task} - {due_datetime}"
            await message.answer(f"Ваши задачи:\n {result_finall}")

            await state.clear()
    except ValueError:
        await message.answer("Неправильная дата или неверный формат, попробуйте ещё раз)", reply_markup=keyboard_cancel)

