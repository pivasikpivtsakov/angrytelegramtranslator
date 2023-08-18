import logging
from uuid import uuid4

from fastapi import FastAPI

from env_config import TG_API_TOKEN
from telegram_api.methods import set_webhook, answer_inline_query, AnswerInlineQueryBody
from telegram_api.models import Update, InlineQueryResultArticle, InputTextMessageContent

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup():
    logger.info("setting webhook...")
    webhook_result = await set_webhook()
    logger.info(f"setwebhook result: \n {webhook_result}")


@app.get("/")
async def root():
    return "healthy"


@app.post(f"/{TG_API_TOKEN}")
async def api_root(body: Update):
    logger.info(body.json())

    await answer_inline_query(
        AnswerInlineQueryBody(
            inline_query_id=body.inline_query.id,
            results=[
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title="sample_title",
                    input_message_content=InputTextMessageContent(message_text="msg")
                )
            ]
        )
    )

    return None
