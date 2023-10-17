import asyncio
import datetime
import logging
import time
import traceback

import mongoengine as mongo

from bot.bot import bot
from bot.texts import get_text
from db.logic import update_user
from db.schemes import User
from mongo_connect import connect_to_mongo

SLEEP_TIME = 8 * 60 * 60
connect_to_mongo()
logging.basicConfig(level=logging.INFO)


async def alert(user_id):
    await bot.send_message(user_id, text=get_text("promotion_alert_msg"))


while True:
    logging.info("promotion alert started")
    users_to_alert = User.objects(
        is_blocked=False,
        is_deactivated=False,
        is_promoted=True,
        alerted_on_promotion_end=False,
        promoted_until__lte=datetime.datetime.utcnow() + datetime.timedelta(days=1),
    )
    for user in users_to_alert:
        try:
            logging.info(f"alerting {user.user_id}(@{user.username})")
            asyncio.run(alert(user.user_id))
            user.alerted_on_promotion_end = True
            update_user(user, is_activity=False)
        except Exception:
            logging.error(traceback.format_exc())
        else:
            logging.info("alerted\n")
    time.sleep(SLEEP_TIME)
