import logging
import random
import string

from fastapi import FastAPI
import httpx as http

from env_config import TG_API_TOKEN
from telegram import answer_inline_query, AnswerInlineQueryBody, TGURL_SETWEBHOOK, API_ROOT
from telegram.models import Update, InlineQueryResultArticle, InputMessageContent

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup():
    async with http.AsyncClient() as client:
        logger.info("setting webhook...")
        response = await client.post(TGURL_SETWEBHOOK, data={"url": API_ROOT})
        logger.info(f"setwebhook result: \n {response.json()}")


@app.get("/")
async def root():
    return "healthy"


@app.post(f"/{TG_API_TOKEN}")
async def api_root(body: Update):
    logger.info(body.json())

    def random_str(length: int):
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

    return await answer_inline_query(
        AnswerInlineQueryBody(
            inline_query_id=body.inline_query.id,
            results=[
                InlineQueryResultArticle(
                    id=random_str(length=10),
                    title="sample_title",
                    input_message_content=InputMessageContent(message_text="msg")
                )
            ]
        )
    )
