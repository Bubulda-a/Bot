import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command

from dotenv import load_dotenv

from dispatcher import get_dispatcher
import os

load_dotenv()
API_TOKEN = os.getenv("TG_TOKEN")

bot = Bot(token=API_TOKEN)


async def main():
    dp = get_dispatcher()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
