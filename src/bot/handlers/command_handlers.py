from aiogram.types import Message


async def start_handler(message: Message):
    await message.reply(
        text="Привет, этот бот умеет распознавать текст на картинке",
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )


async def about_handler(message: Message):
    await message.reply(
        text="Сделал @egorvoron", disable_web_page_preview=True
    )
