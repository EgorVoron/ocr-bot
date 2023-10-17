import logging

import mongoengine as mongo
from aiogram import Dispatcher, types

from bot.bot import bot
from bot.handlers import register_handlers
from bot.middlewares import setup_middlewares
from mongo_connect import connect_to_mongo

logging.basicConfig(level=logging.INFO)
connect_to_mongo()

dp = Dispatcher(bot)  # future: storage
setup_middlewares(dp)
register_handlers(dp)


async def set_commands():
    commands = [
        types.BotCommand(command="/start", description="🦄 Начать"),
        types.BotCommand(command="/about", description="ℹ️ О боте"),
    ]

    await bot.set_my_commands(commands)


async def run_bot():
    await set_commands()
    await dp.start_polling()
