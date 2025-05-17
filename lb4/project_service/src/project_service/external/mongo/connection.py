import sys

import pymongo
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from ...settings import settings
from .mongo_db import db


async def connect_to_mongo():
    logger.info("Initializing mongo connection")
    try:
        db.client = AsyncIOMotorClient(settings.mongo_url)
        db.db = db.client[settings.mongo_db]
    except Exception as exc:
        logger.error("Failed to connect to Mongo")
        logger.error(str(exc))
        sys.exit(1)
    logger.info("Successfully connected to Mongo")


async def close_mongo_connection():
    logger.debug("closing mongo connection")
    db.client.close()


async def init_mongo():
    try:
        collections = await db.db.list_collection_names()
        if settings.mongo_collection in collections:
            logger.info(f'msg="Mongo already initialized"')
        else:
            logger.info(f'msg="Initializing mongo"')
            test_data = [
                {
                    "name": "Project1",
                    "description": "Description1",
                },
                {
                    "name": "Project2",
                    "description": "Description2",
                },
                {
                    "name": "Project3",
                    "description": "Description3",
                },
                {
                    "name": "Project4",
                    "description": "Description4",
                },
                {
                    "name": "Project5",
                    "description": "Description5",
                },
            ]
            await db.db[settings.mongo_collection].insert_many(test_data)
            await db.db[settings.mongo_collection].create_index(
                [("name", pymongo.TEXT)]
            )

    except Exception as exc:
        logger.error('msg="Failed init mongo."')
        logger.error(str(exc))
        sys.exit(1)
