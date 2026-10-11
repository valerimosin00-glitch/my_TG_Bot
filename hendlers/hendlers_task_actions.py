import aiogram as ai
from aiogram.filters import Command

from aiogram.fsm.state import State, StatesGroup   
from aiogram.fsm.context import FSMContext

from hendlers.hendlers_task_to_time import tasks_for_user, option_user_show_task, shows_task_variant1, shows_task_variant2
from buttons import keyboard_cancel, keyboard_start, creat_keyboard_date, keyboard_time
from database_zapros import update_text_task, update_date_task, update_status_task, delete_task

router = ai.Router()

# Общий FSM для получения ID задачи
class Wait_Id(StatesGroup):
    wait_id = State()
    shoose_action = State()

# FSM для редактирования текста задачи
class Update_Text_Task(StatesGroup):
    waiting_task_text = State()

# FSM для переноса задачи
class UpdateDate(StatesGroup):
    waiting_date = State()
    waiting_time = State()

# Хендлер для обработки кнопок с ддействиями
@router.callback_query( ai.F.data.in_({"update_task", "update_date", "task_complit", "delete_task"}))
async def wait_id(callback: ai.types.CallbackQuery, state:FSMContext):
    await callback.answer()

    await callback.message.edit_reply_markup(reply_markup=None)
    await state.set_state(Wait_Id.wait_id)
    await state.update_data(actions = callback.data)
    await callback.message.answer("Введите ID задачи(первое число) которую хотите редактировать", reply_markup=keyboard_cancel)

# Хендлер для получения ID и выбора дальнейшего дествия
@router.message(Wait_Id.wait_id)
async def choose_action(message:ai.types.Message, state:FSMContext):
    task_id = tasks_for_user.get(message.from_user.id)
    data = await state.get_data()
    action = data["actions"]

    if message.text in task_id:
        del tasks_for_user[message.from_user.id]
        await state.clear()
        if action == "update_task":
            await state.set_state(Update_Text_Task.waiting_task_text)
            await state.update_data(id= message.text)
            await message.answer("Введите новый текст задачи")
        elif action == "update_date":
            await state.set_state(UpdateDate.waiting_date)
            await state.update_data(id = message.text)
            await message.answer("Выберите дату", reply_markup= creat_keyboard_date())
        elif action == "task_complit":
            update_status_task(message.text)
            await message.answer("Статус задачи изменён")
            if len(option_user_show_task[message.from_user.id]) == 2:
                user_id,date = option_user_show_task[message.from_user.id]
                del option_user_show_task[user_id]
                await shows_task_variant1(user_id,date,message)
            else:
                user_id,date_start, date_stop = option_user_show_task[message.from_user.id]
                del option_user_show_task[user_id]
                await shows_task_variant2(user_id,date_start,date_stop,message)  
        elif action == "delete_task":
            delete_task(message.text)
            await message.answer("Задача удалена")
            if len(option_user_show_task[message.from_user.id]) == 2:
                user_id,date = option_user_show_task[message.from_user.id]
                del option_user_show_task[user_id]
                await shows_task_variant1(user_id,date,message)
            else:
                user_id,date_start, date_stop = option_user_show_task[message.from_user.id]
                del option_user_show_task[user_id]
                await shows_task_variant2(user_id,date_start,date_stop,message)            

    else:
        await message.answer("Неверный ID, попробуйте ещё раз", reply_markup=keyboard_cancel)   

# Финальный хендлер для изменения задачи
@router.message(Update_Text_Task.waiting_task_text)
async def update_task_text(message: ai.types.Message, state: FSMContext):

    text_task = message.text

    data = await state.get_data()
    task_id = data["id"]
    update_text_task(text_task, task_id)

    await state.clear()
    await message.answer("Задачи изменена" )
    if len(option_user_show_task[message.from_user.id]) == 2:
        user_id,date = option_user_show_task[message.from_user.id]
        del option_user_show_task[user_id]
        await shows_task_variant1(user_id,date,message)
    else:
        user_id,date_start, date_stop = option_user_show_task[message.from_user.id]
        del option_user_show_task[user_id]
        await shows_task_variant2(user_id,date_start,date_stop,message)          

# Хендлер обработки даты 
@router.callback_query(UpdateDate.waiting_date)
async def wait_new_time(callback: ai.types.CallbackQuery, state:FSMContext):
    await callback.answer()

    await state.update_data(date = callback.data)
    await callback.message.edit_reply_markup(reply_markup=None)
    await state.set_state(UpdateDate.waiting_time)
    await callback.message.answer("Теперь выберите время", reply_markup= keyboard_time)

# финальный хендлер получает время и выполняет запрос в бд
@router.callback_query(UpdateDate.waiting_time)
async def update_time(callback:ai.types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    data = await state.get_data()
    task_id, date = data["id"], data["date"]
    time = callback.data
    datetime = f"{date} {time}"

    update_date_task(task_id, datetime)

    await state.clear()
    await callback.message.answer("Задача перенесена")

    if len(option_user_show_task[callback.from_user.id]) == 2:
        user_id,date = option_user_show_task[callback.from_user.id]
        del option_user_show_task[user_id]
        await shows_task_variant1(user_id,date,callback.message)
    else:
        user_id,date_start, date_stop = option_user_show_task[callback.from_user.id]
        del option_user_show_task[user_id]
        await shows_task_variant2(user_id,date_start,date_stop,callback.message)      