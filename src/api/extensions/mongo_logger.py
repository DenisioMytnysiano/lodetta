import datetime
import logging

from api.database.utils import get_collection

collection = get_collection("logs")


class MongoLogger(logging.Handler):

    def __init__(self, level=logging.NOTSET, collection_name: str = "logs", *args, **kwargs):
        logging.Handler.__init__(self, level, *args, **kwargs)
        self.collection = get_collection(collection_name)

    def emit(self, record):
        self.collection.insert_one({
            'when': datetime.datetime.now(),
            'levelno': record.levelno,
            'levelname': record.levelname,
            'message': record.msg
        })
