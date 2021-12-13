import os
from functools import lru_cache

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

load_dotenv()

MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
MONGO_PORT = os.environ.get("MONGO_PORT")
HOSTNAME = os.environ.get("HOSTNAME")
MONGODB_CONNECTION_STRING = (
    f"mongodb://{HOSTNAME}:{MONGO_PORT}"
)


@lru_cache
def get_collection(collection_name: str) -> Collection:
    client: MongoClient = MongoClient(MONGODB_CONNECTION_STRING)
    database: Database = client["lodetta"]
    collection: Collection = database[collection_name]
    return collection
