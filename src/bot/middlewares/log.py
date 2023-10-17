import logging
import time
from datetime import datetime

import chalk
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from logger import get_default_logger


class LoggingMiddleware(BaseMiddleware):
    def __init__(self, logger="mv"):
        if not isinstance(logger, logging.Logger):
            logger = get_default_logger(logger)
        self.logger = logger
        super(LoggingMiddleware, self).__init__()

    def check_timeout(self, obj):
        start = obj.conf.get("_start", None)
        if start:
            del obj.conf["_start"]
            return round((time.time() - start) * 1000)
        return -1

    async def on_pre_process_message(self, message: types.Message, data: dict):
        self.logger.info(
            f"{chalk.bold(chalk.yellow(str(datetime.utcnow())))} "
            f"user: {chalk.blue(f'[{message.from_user.id} {message.from_user.full_name} @{message.from_user.username}]')} "
            f"message: {chalk.green(f'[{message.message_id} {message.text}]')} "
            f"photo: {chalk.cyan(str(bool(message.photo)))}"
        )

    async def on_pre_process_inline_query(
        self, inline_query: types.InlineQuery, data: dict
    ):
        self.logger.info(
            f"{chalk.bold(chalk.yellow(str(datetime.utcnow())))} "
            f"user: {chalk.blue(f'[{inline_query.from_user.id} {inline_query.from_user.full_name} @{inline_query.from_user.username}]')} "
            f"inline query: {chalk.green(f'[{inline_query.query}]')}"
        )

    async def on_pre_process_error(self, update, error, data: dict):
        timeout = self.check_timeout(update)
        if timeout > 0:
            self.logger.info(
                f"Process update [ID:{update.update_id}]: [failed] (in {timeout} ms)"
            )
