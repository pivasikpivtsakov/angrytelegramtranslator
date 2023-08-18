import json
import logging
from typing import Iterable, Optional

import httpx as http
from pydantic import BaseModel

from .models import InlineQueryResultArticle
from .urls import TGURL_ANSWERINLINEQUERY


logger = logging.getLogger(__name__)


class Body(BaseModel):
    inline_query_id: str
    results: Optional[list[InlineQueryResultArticle]] = None


async def answer_inline_query(body: Body):
    async with http.AsyncClient() as client:
        logger.info(body.dict())
        dto = {
            "inline_query_id": body.inline_query_id,
            "results": json.dumps(body.dict(include={"results"})["results"])
        }
        response = await client.post(
            TGURL_ANSWERINLINEQUERY, data=dto
        )
        response_json = response.json()
        if response.status_code == 200:
            return response_json
        else:
            logger.error("answering inline query failed")
            logger.error(response_json)
            return response_json
