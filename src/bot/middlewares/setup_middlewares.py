from aiogram import Dispatcher

from bot.middlewares.log import LoggingMiddleware
from bot.middlewares.user import UserMiddleware


def setup_middlewares(dp: Dispatcher):
    dp.setup_middleware(LoggingMiddleware())
    dp.setup_middleware(UserMiddleware())
