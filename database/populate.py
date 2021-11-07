import os
import logging
import asyncio
from typing import List, Dict, NoReturn
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)

logging.root.setLevel(logging.DEBUG)
logging.basicConfig()

FILENAME = os.environ.get("FILENAME")
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
MONGO_PORT = os.environ.get("MONGO_PORT")
HOSTNAME = os.environ.get("HOSTNAME")
MONGODB_CONNECTION_STRING = (
    f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}" + f"@{HOSTNAME}:{MONGO_PORT}"
)


client: AsyncIOMotorClient = AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
database: AsyncIOMotorDatabase = client["lodetta"]
collection: AsyncIOMotorCollection = database["logos"]


def extract_logos(filename: str) -> List[Dict]:
    logos = []
    with open(filename, "r") as source:
        for line in source:
            id, name = line.strip().split(",")
            logo = {"id": int(id), "name": name, "status": "Supported"}
            logos.append(logo)
    return logos


async def setup_database(data: List[Dict]) -> NoReturn:
    await collection.insert_many(data)
    logging.info(f"Inserted total {len(data)} in {collection} collection")
    collection.create_index("id", unique=True)
    logging.info("Created unique index on 'id' field")
    collection.create_index("name", unique=True)
    logging.info("Created unique index on 'name' field")


def main():
    loop = asyncio.get_event_loop()
    logos = extract_logos(FILENAME)
    loop.run_until_complete(setup_database(logos))


if __name__ == "__main__":
    main()
