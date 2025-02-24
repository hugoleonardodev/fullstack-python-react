import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
DB_NAME = os.getenv("DB_NAME", "testdb")


async def connect_with_retry():
    """Retry MongoDB connection until successful."""
    retries = 1
    delay = 5  # seconds
    for attempt in range(retries):
        try:
            client = AsyncIOMotorClient(MONGO_URI)
            await client.server_info()  # Check if MongoDB is reachable
            print("Connected to MongoDB!")
            return client
        except Exception as e:
            print(f"MongoDB connection failed ({attempt + 1}/{retries}): {e}")
            await asyncio.sleep(delay)
    raise Exception("MongoDB is not available after multiple retries.")


async def seed_database():
    """Seed the database with initial data if empty."""
    client = await connect_with_retry()
    db = client[DB_NAME]
    categories_collection = db["categories"]

    count = await categories_collection.count_documents({})
    if count == 0:
        print("Seeding database with default categories...")
        default_categories = [
            {"name": "Technology"},
            {"name": "Health"},
            {"name": "Finance"},
            {"name": "Education"},
        ]
        await categories_collection.insert_many(default_categories)
        print("Database seeding complete.")
    else:
        print("Database already populated. Skipping seeding.")

    client.close()
