from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

from bot.handlers import admin_handlers, command_handlers
from bot.handlers.photo_handler import photo_handler


def register_handlers(dp: Dispatcher):
    # admin
    dp.register_message_handler(
        admin_handlers.get_user_handler, Text(startswith="user ")
    )
    dp.register_callback_query_handler(
        admin_handlers.promote_user_handler, lambda c: c.data.startswith("promote ")
    )

    # commands
    dp.register_message_handler(command_handlers.start_handler, commands="start")
    dp.register_message_handler(command_handlers.about_handler, commands="about")

    # reading
    dp.register_message_handler(photo_handler, content_types=[ContentType.PHOTO])
