import aiogram as ai
from datetime import datetime
from aiogram.fsm.state import State, StatesGroup   
from aiogram.fsm.context import FSMContext

from database_zapros import add_tasks

from buttons import keyboard_cancel, keyboard_start, creat_keyboard_date, keyboard_time

router = ai.Router()

class Add_tasks_to_time(StatesGroup):
    waiting_task = State()
    waiting_date = State()
    waiting_time = State()
    else_date = State()

# Хендлер для добавления задач ко времени
@router.callback_query(ai.F.data == "add_task")
async def add_task(callback: ai.types.CallbackQuery, state:FSMContext):

    await callback.answer()
    await state.set_state(Add_tasks_to_time.waiting_task)
    await callback.message.answer("Введите задачу", reply_markup=keyboard_cancel)

# Хендлер на получение даты
@router.message(Add_tasks_to_time.waiting_task)
async def add_task(message: ai.types.Message, state: FSMContext):

    await state.update_data(task=message.text)

    await state.set_state(Add_tasks_to_time.waiting_date)
    keyboard_date = creat_keyboard_date()
    await message.answer("Выберите дату", reply_markup= keyboard_date)

# Хендлер который получил дату 
@router.callback_query(Add_tasks_to_time.waiting_date)
async def add_date(callback: ai.types.CallbackQuery, state:FSMContext):
    await callback.answer()
    if callback.data == "custom_date":
        await state.set_state(Add_tasks_to_time.else_date)
        await callback.message.answer("Введите дату и время, например 2026-05-08 20:00")
    else:
        await state.update_data(date=callback.data)
        await state.set_state(Add_tasks_to_time.waiting_time)
        await callback.message.answer("Выберите время", reply_markup=keyboard_time)

# Обработка времени и добавление в бд
@router.callback_query(Add_tasks_to_time.waiting_time)
async def add_time(callback:ai.types.CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    date = data["date"]
    date_task = f"{date} {callback.data}"

    user_id = callback.from_user.id
    task = data["task"]
    date_creat = str(datetime.now().strftime("%Y-%m-%d %H:%M"))

    add_tasks(user_id, task, date_task, date_creat)

    await state.clear()
    await callback.message.answer("Задача добавлена", reply_markup=keyboard_start)


# Хендлер для обработки произвольной даты
@router.message(Add_tasks_to_time.else_date)
async def add_task_finall(message: ai.types.Message, state: FSMContext):
    
    date_format="%Y-%m-%d %H:%M"
    date_format2 = "%Y.%m.%d %H:%M"
    try:
        if "-" in message.text:
            date = datetime.strptime(message.text, date_format)
        else:
            date = datetime.strptime(message.text, date_format2)

        user_id = message.from_user.id

        data = await state.get_data()
        task = data["task"]

        date_task = str(date.strftime("%Y-%m-%d %H:%M"))

        date_creat = str(datetime.now().strftime("%Y-%m-%d %H:%M"))

        add_tasks(user_id, task, date_task, date_creat)

        await state.clear()
        await message.answer("Задача добавлена", reply_markup=keyboard_start)

    except ValueError:
        await message.answer("Неправильная дата или неверный формат, попробуйте ещё раз)", reply_markup=keyboard_cancel)