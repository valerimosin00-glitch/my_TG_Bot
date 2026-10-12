import aiogram as ai
from aiogram.filters import Command

from aiogram.fsm.state import State, StatesGroup   
from aiogram.fsm.context import FSMContext

from buttons import keyboard_task_no_time, keyboard_task_actions_no_time, keyboard_cancel
from database_zapros import show_task_no_time, no_time_add_tasks, show_task_complit_no_time, update_status_task_no_time, delete_task_no_time, update_text_task_no_time

router = ai.Router()

# Основной обработчик задач без даты
@router.callback_query(ai.F.data == "plan")
async def task_no_time(callback: ai.types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Выберите действие", reply_markup=keyboard_task_no_time)

# Словарь для списка ID и словарь для списка с параметрами запроса
plans_for_user= {}

# вынес в отдельную функцию
async def shows_task_no_time(user_id, message_obj):
    result = show_task_no_time(user_id)
    result_finall = ""
    if result == []:
        await message_obj.answer("Задач пока нет")
    else:
        plans_id = []
        for i in result:
            plan_id, task = i
            plans_id.append(str(plan_id))
            result_finall = result_finall + f"\n {plan_id} {task}"
        plans_for_user[user_id]=plans_id
        await message_obj.answer(f"Ваши задачи:\n {result_finall}", reply_markup=keyboard_task_actions_no_time)


# Хендлер для просмотра задач без даты
@router.callback_query(ai.F.data == "no_time_show_task")
async def Show_Task_No_Time(callback:ai.types.CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id
    await shows_task_no_time(user_id,callback.message)

# FSM для добавления задачи
class Add_Task_no_Time(StatesGroup):
    wait_task = State()

# Хендлер для добавления задач без даты
@router.callback_query(ai.F.data == "no_time_add_task")
async def add_task_no_time(callback: ai.types.CallbackQuery, state:FSMContext):
    await callback.answer()
    await state.set_state(Add_Task_no_Time.wait_task)
    await callback.message.answer("Введите задачу которую хотите добавить")

# Хендлер для добавления задачи
@router.message(Add_Task_no_Time.wait_task)
async def add_task(message: ai.types.Message, state: FSMContext):

    user_id = message.from_user.id
    task = message.text
    no_time_add_tasks(user_id,task)

    await state.clear()
    await message.answer("Задача добавлена", reply_markup=keyboard_task_no_time)

# Хендлер для просмотра выполненных задач
@router.callback_query(ai.F.data == "no_time_show_task_compl")
async def show_task_no_time_complit(callback: ai.types.CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id
    result = show_task_complit_no_time(user_id)
    result_finall = ""
    if result == []:
        await callback.message.answer("Задач пока нет")
    else:
        for i in result:
            plan_id, task = i
            result_finall = result_finall + f"\n {plan_id} {task}"
        await callback.message.answer(f"Ваши задачи:\n {result_finall}", reply_markup=keyboard_task_no_time)

# FSM для обработки действий с задачами без даты
class Actions_Tasks(StatesGroup):
    wait_task_id = State()
    wait_new_task = State()

# Хендлер для обработки действий с задачами без даты
@router.callback_query(ai.F.data.startswith("no_time_"))
async def tasks_actions(callback: ai.types.CallbackQuery, state:FSMContext):
    await callback.answer()

    await state.set_state(Actions_Tasks.wait_task_id)
    await state.update_data(action = callback.data)
    await callback.message.answer("Введите ID задачи")

# Хендлер для обработки ID
@router.message(Actions_Tasks.wait_task_id)
async def receive_id(message: ai.types.Message, state: FSMContext):
    plan_id = message.text
    data = await state.get_data()
    action = data["action"]
    user_id = message.from_user.id

    if message.text in plans_for_user.get(user_id):
        if action == "no_time_task_complit":
            update_status_task_no_time(plan_id)
            await message.answer("Статус изменён")
            await state.clear()
            await shows_task_no_time(user_id, message)
        elif action == "no_time_delete_task":
            delete_task_no_time(plan_id)
            await message.answer("Задача удалена")
            await state.clear()
            await shows_task_no_time(user_id, message)
        elif action == "no_time_update_task":
            await state.update_data(plan_id = plan_id)
            await state.set_state(Actions_Tasks.wait_new_task)
            await message.answer("Введите новый текст задачи")
    else:
        await message.answer("Неверный ID, попробуйте ещё раз", reply_markup=keyboard_cancel)

# Обработчик изменения задачи
@router.message(Actions_Tasks.wait_new_task)
async def update_task_no_time(message: ai.types.Message, state: FSMContext):
    data = await state.get_data()
    plan_id = data["plan_id"]
    task = message.text
    user_id = message.from_user.id

    update_text_task_no_time(task, plan_id)
    await message.answer("Задача обновлена")
    await state.clear()
    await shows_task_no_time(user_id, message)




