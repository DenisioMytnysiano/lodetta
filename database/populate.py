import os
import asyncio
from typing import List, Dict, NoReturn
import motor.motor_asyncio

FILENAME = os.environ.get("FILENAME")
MONGO_USER = os.environ.get("MONGO_USER")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
MONGO_PORT = os.environ.get("MONGO_PORT")
HOSTNAME = os.environ.get("HOSTNAME")
print(MONGO_PORT)
MONGODB_CONNECTION_STRING = (
    f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}" + f"@{HOSTNAME}:{MONGO_PORT}"
)


client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_CONNECTION_STRING)
database = client["lodetta"]
collection = database["logos"]


def extract_logos(filename: str) -> List[Dict]:
    logos = []
    with open(filename, "r") as source:
        for line in source:
            logo = {"name": line.strip()}
            logos.append(logo)
    return logos


async def insert_logos(logos: List[Dict]) -> NoReturn:
    await collection.insert_many(logos)


def main():
    loop = asyncio.get_event_loop()
    logos = extract_logos(FILENAME)
    loop.run_until_complete(insert_logos(logos))


if __name__ == "__main__":
    main()
