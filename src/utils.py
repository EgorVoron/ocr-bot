import datetime
import logging
from time import time

logger = logging.getLogger("utils")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


def timeit(func):
    def wrapper(*args, **kwargs):
        t = time()
        res = func(*args, **kwargs)
        tt = time() - t
        logger.info(f"{func.__name__}:", tt)
        return res

    return wrapper


def format_text(text: str) -> str:
    return text.replace("\n", " ").lower()


def text_is_correct(text: str) -> bool:
    if not text:
        return False
    letters_and_digits_num = sum(map(lambda x: x.isalpha() or x.isdigit(), text))
    return letters_and_digits_num >= 0.6 * len(text)


def string_after(string: str, substring: str):
    return string.partition(substring)[2]


def readable_date(date: datetime.date) -> str:
    year = date.year
    month = date.month
    day = date.day
    return f"{day}.{month}.{year}"


def today_min_datetime() -> datetime.datetime:
    return datetime.datetime.combine(
        datetime.datetime.utcnow().date(), datetime.datetime.min.time()
    )
