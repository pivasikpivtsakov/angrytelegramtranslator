import logging
from contextlib import asynccontextmanager
from uuid import uuid4
import base64

import openai
from fastapi import FastAPI

from angry_api import angrify
from env_config import TG_API_TOKEN, OPENAI_API_KEY, BOT_NAME
from telegram_api.methods import set_webhook, answer_inline_query, AnswerInlineQueryBody
from telegram_api.models import Update, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultsButton

app = FastAPI()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.debug("setting webhook...")
    webhook_result = await set_webhook()
    logger.info(f"setwebhook result: \n {webhook_result}")
    logger.debug("setting openai api key...")
    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
        logger.info("openai api key is set")
    else:
        logger.error("openai api key unset!")
    yield


@app.get("/")
async def root():
    return "healthy"


@app.post(f"/{TG_API_TOKEN}")
async def api_root(body: Update):
    logger.info(body.json())

    user_query = body.inline_query.query.strip("\n ")
    if user_query:
        calm_text = await angrify(user_query)

        await answer_inline_query(
            AnswerInlineQueryBody(
                inline_query_id=body.inline_query.id,
                results=[
                    InlineQueryResultArticle(
                        id=str(uuid4()),
                        title="calm text",
                        input_message_content=InputTextMessageContent(message_text=calm_text)
                    )
                ],
                button=InlineQueryResultsButton(
                    text="create in pm bot",
                    # start_parameter=f"https://t.me/{BOT_NAME}?userquery={base64.b64encode(user_query.encode()).decode()}"
                )
            )
        )

    return None
