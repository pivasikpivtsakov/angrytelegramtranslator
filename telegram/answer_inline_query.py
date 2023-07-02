import logging

import httpx as http

from .urls import TGURL_ANSWERINLINEQUERY


logger = logging.Logger(__name__)


async def answer_inline_query():
    async with http.AsyncClient() as client:
        response = await client.post(
            TGURL_ANSWERINLINEQUERY, json={
                "results": [
                    {
                        "type": "article",
                        "id": "1",
                        "title": "Title",
                        "description": "Description",
                        "input_message_content": {"message_text": "hello I can respond to messages"}
                    }
                ]
            }
        )
        response_json = response.json()
        if response.status_code == 200:
            return response_json
        else:
            logger.error("answering inline query failed")
            logger.error(response_json)
            return response_json
