from buttons import keyboard_show_task_to_time
from aiogram.exceptions import TelegramAPIError

from database_zapros import get_tasks_for_notifications 

async def send_notifications(bot):
    result = get_tasks_for_notifications()
    start = result["start"]
    before = result["before"]
#user_id, task, due_datetime
    if start != []:
        for i in start:
            try:
                await bot.send_message(
            chat_id=i[0],
            text=f"Время приступить к задаче: {i[1]}\n Для просмотра задач можете воспользоваться кнопками",
            reply_markup=keyboard_show_task_to_time)
            except TelegramAPIError as error:
                print(f"Ошибка отправки пользователю {i[0]}: {error}")
    if before != []:
        for i in before:
            try:
                await bot.send_message(
            chat_id=i[0],
            text=f"Через 30 минут нужно будет приступать к задаче: {i[1]} \n Для просмотра задач можете воспользоваться кнопками",
            reply_markup=keyboard_show_task_to_time)
            except TelegramAPIError as error:
                print(f"Ошибка отправки пользователю {i[0]}: {error}")

    