import datetime

from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from bot.bot import bot
from bot.texts import get_text
from db.logic import update_user
from db.schemes import User
from parameters import parameters
from utils import readable_date, string_after

admin_ids = parameters["admins"]


def require_admin(handler):
    async def wrapper(obj: Message | CallbackQuery):
        if obj.from_user.id not in admin_ids:
            return
        return await handler(obj)

    return wrapper


@require_admin
async def get_user_handler(message: Message):
    user_id_str = string_after(message.text, "user ")
    if not user_id_str.isdigit():
        await message.reply("Invalid user id")
        return
    user_id = int(user_id_str)
    user = User.objects(user_id=user_id).first()
    if not user:
        await message.reply("User not found")
        return
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(f"promote", callback_data=f"promote {user_id}"))
    await message.reply(
        f"user {user_id} @{user.username}\n{user.first_name} {user.last_name}",
        reply_markup=kb,
    )


def promote_user(user: User) -> datetime.datetime:
    remainder = None
    if user.still_promoted():
        remainder = user.promoted_until - datetime.datetime.utcnow()
    user.is_promoted = True
    user.promoted_at = datetime.datetime.utcnow()
    user.promoted_until = user.promoted_at + datetime.timedelta(days=31)
    if remainder:
        user.promoted_until += remainder
    user.alerted_on_promotion_end = False
    update_user(user, is_activity=False)
    return user.promoted_until


@require_admin
async def promote_user_handler(callback_query: CallbackQuery):
    user_id = int(string_after(callback_query.data, "promote "))
    user = User.objects(user_id=user_id).first()
    if not user:
        await callback_query.answer("User not found")  # deleted probably
        return
    promoted_until = promote_user(user)
    await callback_query.answer(f"Promoted until {promoted_until}")
    await bot.send_message(
        user_id,
        text="Ты получил премиум, спасибо за поддержку",
    )
