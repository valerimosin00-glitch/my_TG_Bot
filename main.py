import os
from dotenv import load_dotenv
import aiogram as ai
import asyncio
from hendlers.hendlers_task_to_time import router as tasks_router
from hendlers.hendlers_add_task import router as add_tasks_router
from hendlers.hendlers_task_actions import router as task_actions_router
from hendlers.hendlers_task_no_time import router as task_no_time_router
from hendlers.hendlers_expence import router as expence_router
from creat_table import creat_table
from sending_notifications import send_notifications
from apscheduler.schedulers.asyncio import AsyncIOScheduler 


load_dotenv()

TOKEN = os.getenv("TOKEN")



dp = ai.Dispatcher()

dp.include_router(tasks_router)
dp.include_router(add_tasks_router)
dp.include_router(task_actions_router)
dp.include_router(task_no_time_router)
dp.include_router(expence_router)

async def main():
    creat_table()
    bot = ai.Bot(token=TOKEN)

    scheduler = AsyncIOScheduler(timezone="Asia/Yerevan")

    scheduler.add_job(
    func=send_notifications,
    trigger='interval',
    minutes=1,
    args=[bot],
    id="check_tasks",
    max_instances=1)
    scheduler.start()
    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown(wait=False)
        await bot.session.close()



if __name__ == "__main__":
    asyncio.run(main())