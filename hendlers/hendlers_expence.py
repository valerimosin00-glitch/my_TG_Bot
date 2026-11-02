import aiogram as ai
from aiogram.filters import Command

from aiogram.fsm.state import State, StatesGroup   
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta

from buttons import keyboard_expence, keyboard_choose_add_expence, keyboard_category, keyboard_show_expence,  keyboard_cancel
from database_zapros import add_expence, show_expence_two_date, show_expence_one_date

router = ai.Router()

# Хендлер для обработки кнопки расходы
@router.message(ai.F.text == "Расходы")
async def expenses(message: ai.types.Message):
    await message.answer("Что нужно сделать?", reply_markup= keyboard_expence) 

# FSM для добавления расходов
class Add_Expence(StatesGroup):
    waiting_date = State()
    obtaining_date = State()
    waiting_category = State()
    waiting_amount = State()
    waiting_description = State()

# Хендлер для обработки добавления расходов
@router.callback_query(ai.F.data =="add_expence" )
async def add_expense(callback: ai.types.CallbackQuery, state:FSMContext):
    await callback.answer()

    await state.set_state(Add_Expence.waiting_date)
    await callback.message.answer("Выберите дату", reply_markup=keyboard_choose_add_expence)

#Обработываем дату
@router.callback_query(Add_Expence.waiting_date)
async def date(callback: ai.types.CallbackQuery, state:FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    if callback.data == "today_add" or callback.data == "yesterday_add":
        dat = datetime.today()
        today = dat.date()
        if callback.data == "yesterday_add":
            today = today + timedelta(days=-1) 
        await state.update_data(date = str(today))
        await state.set_state(Add_Expence.waiting_category)
        await callback.message.answer("Выберите категорию", reply_markup=keyboard_category )
    else:
        await state.set_state(Add_Expence.obtaining_date)
        await callback.message.answer("Введите дату в формате год-месяц-день, например 2026-11-15")

#Хендлер для обработки произволной даты
@router.message(Add_Expence.obtaining_date)
async def cust_date(message: ai.types.Message, state:FSMContext):
    await message.edit_reply_markup(reply_markup=None)
    try:
        datetime.strptime(message.text, "%Y-%m-%d")
        await state.update_data(date = str(message.text))
        await state.set_state(Add_Expence.waiting_category)
        await message.answer("Выберите категорию", reply_markup=keyboard_category )
    except ValueError:
        await message.answer("Неверная дата или формат, попробуйте ещё раз", reply_markup=keyboard_cancel)

# словарь для определения категорий
key_value_category = {"food":"Еда", "tasty_treats":"Вкусняшки","health":"Здоровье","housing":"Коммуналка и жильё",
                      "body_care":"Уход за телом", "bus_and_car":"Транспорт", "entertainment":"Развлечения", 
                      "other":"Другое"}

# Хендлер выбора категорий
@router.callback_query(Add_Expence.waiting_category)
async def category(callback: ai.types.CallbackQuery, state:FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    await state.update_data(category = key_value_category[callback.data])
    await state.set_state(Add_Expence.waiting_amount)
    await callback.message.answer("Введите сумму", reply_markup= keyboard_cancel)

# Хендлер для получения суммы
@router.message(Add_Expence.waiting_amount)
async def amount(message:ai.types.Message, state:FSMContext):
    try:
        amount_float = float(message.text)
        if amount_float > 0 and amount_float < 500000:
            await state.update_data(amounts = amount_float)
            await state.set_state(Add_Expence.waiting_description)
            await message.answer("Добавьте комментарий", reply_markup= keyboard_cancel)
        else:
            raise ValueError
    except ValueError:
        await message.answer("Сумма введена не правильно, попробуйте ещё раз ввести число", reply_markup= keyboard_cancel)

# Финальный хендлер для добавления расходов
@router.message(Add_Expence.waiting_description)
async def add_expence_in_table(message:ai.types.Message, state:FSMContext):
    description = message.text
    user_id =message.from_user.id
    data = await state.get_data()
    expense_date = data["date"]
    category = data["category"]
    amount = data["amounts"]

    add_expence(user_id, amount, category, expense_date,description )

    await state.clear()
    await message.answer("Запись добавлена!", reply_markup= keyboard_expence)


# Хендлер обработки кнопки расходы
@router.callback_query(ai.F.data == "show_expence")
async def show_expence(callback:ai.types.CallbackQuery):
    await callback.answer()

    await callback.message.answer("Выберите за какой период показать рассходы", reply_markup= keyboard_show_expence)

# FSM для получения произвольной даты
class Shoose_Date_For_Custom_Date(StatesGroup):
    waiting_date = State()

# Хендлер для обработки произвольной даты
@router.callback_query(ai.F.data == "show_custom_date")
async def shoose_date_for_custom_date(callback: ai.types.CallbackQuery, state:FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)

    await state.set_state(Shoose_Date_For_Custom_Date.waiting_date)
    await callback.message.answer("Введите дату через : ,\n например 2014-10-24:2015-11-09", reply_markup= keyboard_cancel)

#Хендлер для обработки произвольной даты
@router.message(Shoose_Date_For_Custom_Date.waiting_date)
async def get_custom_date(message:ai.types.Message, state:FSMContext):
    date = message.text
    try:
        date = date.split(":")
        date_start = date[0]
        date_stop = date[-1]

        datetime.strptime(date_start, "%Y-%m-%d")
        datetime.strptime(date_stop, "%Y-%m-%d")
        if date_start > date_stop:
            date_stop,date_start = date_start,date_stop

        user_id = message.from_user.id
        result_finall = show_expence_two_date(user_id, str(date_start), str(date_stop))
        await state.clear()
        await message.answer(f"Ваши расходы: \n {result_finall}")
    except ValueError:
        await message.answer("Неверная дата или формат, попробуйте ещё раз", reply_markup= keyboard_cancel)

# Хендлер для обработки кнопок выбора периода расчетё
@router.callback_query(ai.F.data.startswith("expence_show"))
async def show_expence_date_buttons(callback: ai.types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    user_id = callback.from_user.id
    today = datetime.today().date()
    data = callback.data

    if data == "expence_show_today":
        result_finall = show_expence_one_date(user_id, today)
        await callback.message.answer(f"Ваши расходы: \n {result_finall}")

    else:
        date_stop = today
        week_day = today.weekday()
        if data == "expence_show_this_week":
            date_start = today - timedelta(days=week_day)
        elif data == "expence_show_week":
            date_start = today - timedelta(days=6)
        elif data == "expence_show_this_month":
            date_start = today.replace(day=1)
        elif data == "expence_show_month":
            date_start =  today - timedelta(days=29)
        result_finall = show_expence_two_date(user_id, str(date_start), str(date_stop))
        await callback.message.answer(f"Ваши расходы: \n {result_finall}")