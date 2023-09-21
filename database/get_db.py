import logging
from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient

from env_config import DATABASE_URL

logger = logging.getLogger(__name__)


@lru_cache
def get_db():
    logger.debug("loading db...")
    client = AsyncIOMotorClient(DATABASE_URL)
    db = client.get_default_database()
    logger.info("db loaded")
    return db
