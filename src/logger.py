import logging

from parameters import parameters


def get_default_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.addHandler(
        logging.FileHandler(filename=parameters["log_file"], encoding="utf-8")
    )
    return logger
