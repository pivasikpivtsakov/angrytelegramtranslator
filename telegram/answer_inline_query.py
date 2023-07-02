import httpx as http

from telegram.urls import TGURL_ANSWERINLINEQUERY


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
        return response.json()
