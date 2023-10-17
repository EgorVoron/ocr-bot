import io

from aiogram import types

from bot.ocr.basic_engine import scan_text


async def photo_handler(message: types.Message):
    photo = message.photo[-1]

    photo_bytes = io.BytesIO()
    await photo.download(destination_file=photo_bytes)
    text_lat, text_cyr = scan_text(photo_bytes.read())

    await message.reply(f"текст на кириллице: {text_cyr}\nна латинице: {text_lat}")

