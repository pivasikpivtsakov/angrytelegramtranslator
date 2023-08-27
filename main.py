import logging
from contextlib import asynccontextmanager
from typing import Callable, Coroutine
from uuid import uuid4

import openai
from fastapi import FastAPI

from angry_api import angrify
from env_config import TG_API_TOKEN, OPENAI_API_KEY, DEBOUNCE_SECS
from services import debounce
from telegram_api.methods import set_webhook, answer_inline_query, AnswerInlineQueryBody
from telegram_api.models import Update, InlineQueryResultArticle, InputTextMessageContent

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


users_to_angrifiers: dict[int, Callable[..., Coroutine[..., ..., Coroutine[..., ..., str]]]] = {}


async def get_angrifier_for_user(user_id: int):
    debouncer = debounce(float(DEBOUNCE_SECS))

    async def angrify_for_user(text: str):
        logger.info(f"angrifier for user={user_id} called!")
        return await angrify(text)

    if not (angrifier := users_to_angrifiers.get(user_id)):
        users_to_angrifiers[user_id] = debouncer(angrify_for_user)
        angrifier = users_to_angrifiers[user_id]

    return angrifier


@app.post(f"/{TG_API_TOKEN}")
async def api_root(body: Update):
    logger.info(body.json())

    user_query = body.inline_query.query.strip("\r\n ")
    angrify_for_user = await get_angrifier_for_user(body.inline_query.from_.id)
    if user_query:
        angrify_for_user_deb = await angrify_for_user(user_query)
        calm_text = await angrify_for_user_deb

        await answer_inline_query(
            AnswerInlineQueryBody(
                inline_query_id=body.inline_query.id,
                results=[
                    InlineQueryResultArticle(
                        id=str(uuid4()),
                        title="calm text",
                        description=calm_text,
                        input_message_content=InputTextMessageContent(message_text=calm_text)
                    )
                ],
            )
        )

    return None
