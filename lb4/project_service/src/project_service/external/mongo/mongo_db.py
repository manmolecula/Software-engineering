from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class DataBase:
    client: AsyncIOMotorClient = None  # type: ignore
    db: AsyncIOMotorDatabase = None  # type: ignore


db = DataBase()


async def get_mongo_database() -> AsyncIOMotorDatabase:
    return db.db
