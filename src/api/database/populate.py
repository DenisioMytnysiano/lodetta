import os
import logging
from typing import List, Dict, NoReturn
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from dotenv import load_dotenv

from api.extensions.utils import get_logger

load_dotenv()
logger = get_logger(__name__)

FILENAME = os.environ.get("FILENAME")
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
MONGO_PORT = os.environ.get("MONGO_PORT")
HOSTNAME = os.environ.get("HOSTNAME")
MONGODB_CONNECTION_STRING = (
    f"mongodb://{HOSTNAME}:{MONGO_PORT}"
)


client: MongoClient = MongoClient(MONGODB_CONNECTION_STRING)
database: Database = client["lodetta"]
collection: Collection = database["logos"]


def extract_logos(filename: str) -> List[Dict]:
    logos = []
    with open(filename, "r") as source:
        for line in source:
            name, id = line.strip().split(",")
            logo = {"id": int(id), "name": name, "status": "Supported"}
            logos.append(logo)
    return logos


def setup_database(data: List[Dict]) -> NoReturn:
    database.drop_collection(collection.name)
    collection.insert_many(data)
    logger.info(f"Inserted total {len(data)} in {collection} collection")
    collection.create_index("id", unique=True)
    logger.info("Created unique index on 'id' field")
    collection.create_index("name", unique=True)
    logger.info("Created unique index on 'name' field")


def main():
    logos = extract_logos(FILENAME)
    setup_database(logos)


if __name__ == "__main__":
    main()
