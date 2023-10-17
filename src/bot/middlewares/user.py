import datetime

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from db.schemes import User


def create_user(tg_user: types.User):
    user_list = User.objects(user_id=tg_user.id)

    params = {
        "user_id": tg_user.id,
        "first_name": tg_user.first_name,
        "last_name": tg_user.last_name,
        "username": tg_user.username,
        "language_code": tg_user.language_code,
    }
    if not user_list:
        User(**params).save()
    else:
        user = user_list[0]
        for field_name, field_value in params.items():
            setattr(user, field_name, field_value)
        user.save()


class UserMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        create_user(message.from_user)

    async def on_pre_process_inline_query(
        self, inline_query: types.InlineQuery, data: dict
    ):
        create_user(inline_query.from_user)
