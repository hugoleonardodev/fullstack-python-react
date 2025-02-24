import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

print(DB_NAME, "<database>DB_NAME")

client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]
