import logging

from api.extensions.mongo_logger import MongoLogger


def get_logger(name):
    logger = logging.getLogger(name)
    console_handler = logging.StreamHandler()
    mongo_handler = MongoLogger()
    logger.addHandler(console_handler)
    logger.addHandler(mongo_handler)
    return logger
