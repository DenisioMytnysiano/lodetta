import logging

from api.database.utils import get_collection


class MongoLogger(logging.Handler):

    def __init__(self, level=logging.NOTSET, collection_name: str = "logs"):
        logging.Handler.__init__(self, level)
        self.collection = get_collection(collection_name)

    def emit(self, record):
        self.collection.insert_one(record.__dict__)
