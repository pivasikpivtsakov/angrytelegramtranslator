import logging
from typing import Iterable

import httpx as http
from pydantic import BaseModel

from .models import InlineQueryResultArticle
from .urls import TGURL_ANSWERINLINEQUERY


logger = logging.Logger(__name__)


class Body(BaseModel):
    inline_query_id: str
    results: list[InlineQueryResultArticle]


async def answer_inline_query(body: Body):
    async with http.AsyncClient() as client:
        response = await client.post(
            TGURL_ANSWERINLINEQUERY, json=body.json()
        )
        response_json = response.json()
        if response.status_code == 200:
            return response_json
        else:
            logger.error("answering inline query failed")
            logger.error(response_json)
            return response_json
