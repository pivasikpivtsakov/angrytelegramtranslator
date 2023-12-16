import logging

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel

from database.get_db import get_db

logger = logging.getLogger(__name__)


class Resource(BaseModel):
    key: str
    value: str


class LangResources(BaseModel):
    lang: str
    resources: list[Resource]


class LangResourceQueries:
    def __init__(self, db: AsyncIOMotorDatabase = Depends(get_db)):
        self.collection_name = "lang-resources"
        self.db = db

    async def get_value_for_lang(self, lang: str, key: str) -> Resource | None:
        cursor = self.db[self.collection_name].aggregate([
            {"$unwind": "$resources"},
            {"$match": {"resources.key": key, "lang": lang}},
            {"$replaceWith": "$resources"},
        ])
        async for entity in cursor:
            entity: dict[str, ...]
            return Resource.model_validate(entity)
        logger.error(f"Resource not found: lang={lang} key={key}")
