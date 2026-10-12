import os
from dotenv import load_dotenv
import aiogram as ai
import asyncio
from hendlers.hendlers_task_to_time import router as tasks_router
from hendlers.hendlers_add_task import router as add_tasks_router
from hendlers.hendlers_task_actions import router as task_actions_router
from hendlers.hendlers_task_no_time import router as task_no_time_router

load_dotenv()

TOKEN = os.getenv("TOKEN")



dp = ai.Dispatcher()

dp.include_router(tasks_router)
dp.include_router(add_tasks_router)
dp.include_router(task_actions_router)
dp.include_router(task_no_time_router)

async def main():
    bot = ai.Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())