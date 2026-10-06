import os
from dotenv import load_dotenv
import aiogram as ai
import asyncio
from hendlers.hendlers_task import router as tasks_router


load_dotenv()

TOKEN = os.getenv("TOKEN")



dp = ai.Dispatcher()

dp.include_router(tasks_router)



async def main():
    bot = ai.Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())