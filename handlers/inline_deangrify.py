import logging
from typing import Callable, Coroutine
from uuid import uuid4

from fastapi_events.typing import Event
from fastapi_events.handlers.local import local_handler
from fastapi_events.registry.payload_schema import registry as payload_schema
from pydantic import BaseModel
from openai import error as openai_error

from angry_api import deangrify
from env_config import DEBOUNCE_SECS, BOT_NAME
from services import debounce
from telegram_api.methods import answer_inline_query, AnswerInlineQueryBody
from telegram_api.models import InlineQueryResultArticle, InputTextMessageContent
from .event_names import EventNames

logger = logging.getLogger(__name__)


@payload_schema.register(event_name=EventNames.INLINE_DEANGRIFY)
class InlineDeangrifyPayload(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    user_id: int
    query: str
    query_id: str


users_to_angrifiers: dict[int, Callable[..., Coroutine[..., ..., Coroutine[..., ..., str]]]] = {}


def get_deangrifier_for_user(user_id: int):
    debouncer = debounce(float(DEBOUNCE_SECS))

    async def deangrify_for_user(text: str):
        logger.info(f"angrifier for user={user_id} called!")
        return await deangrify(text)

    if not (angrifier := users_to_angrifiers.get(user_id)):
        users_to_angrifiers[user_id] = debouncer(deangrify_for_user)
        angrifier = users_to_angrifiers[user_id]

    return angrifier


def preprocess_query(query: str) -> str:
    return query.strip("\r\n ")[:200]


@local_handler.register(event_name=EventNames.INLINE_DEANGRIFY)
async def deangrify_inline(event: Event):
    event_name, payload = event
    payload_model = InlineDeangrifyPayload(**payload)

    user_query = preprocess_query(payload_model.query)
    deangrify_for_user = get_deangrifier_for_user(payload_model.user_id)
    if user_query:
        try:
            debounce_for_user = await deangrify_for_user(user_query)
            calm_text = await debounce_for_user
            logger.debug(f"calm text output is: {calm_text}")

            await answer_inline_query(
                AnswerInlineQueryBody(
                    inline_query_id=payload_model.query_id,
                    results=[
                        InlineQueryResultArticle(
                            id=str(uuid4()),
                            title="Calm Text",
                            description=calm_text,
                            input_message_content=InputTextMessageContent(message_text=calm_text)
                        )
                    ],
                )
            )
        except openai_error.RateLimitError:
            please_donate = (
                "Oops, I’m really sorry about that. "
                "My OpenAI account ran out of money and I need to top it up. "
                "You may help with this by making a small donation. "
                "Every dollar makes a difference! "
                f"Please see @{BOT_NAME} for the available options."
            )
            await answer_inline_query(
                AnswerInlineQueryBody(
                    inline_query_id=payload_model.query_id,
                    results=[
                        InlineQueryResultArticle(
                            id=str(uuid4()),
                            title="OpenAI account has run out of money 😵",
                            description="Your financial help is HIGHLY appreciated!",
                            input_message_content=InputTextMessageContent(message_text=please_donate)
                        )
                    ],
                )
            )
        except openai_error.OpenAIError:
            await answer_inline_query(
                AnswerInlineQueryBody(
                    inline_query_id=payload_model.query_id,
                    results=[
                        InlineQueryResultArticle(
                            id=str(uuid4()),
                            title="Some error with OpenAI API 😵",
                            description="Already working on the fix",
                            input_message_content=InputTextMessageContent(message_text="")
                        )
                    ],
                )
            )
