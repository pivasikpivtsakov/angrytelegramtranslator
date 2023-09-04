import logging
from typing import Callable, Coroutine
from uuid import uuid4

from fastapi_events.typing import Event
from fastapi_events.handlers.local import local_handler
from fastapi_events.registry.payload_schema import registry as payload_schema
from pydantic import BaseModel

from angry_api import deangrify
from env_config import DEBOUNCE_SECS
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


async def get_deangrifier_for_user(user_id: int):
    debouncer = debounce(float(DEBOUNCE_SECS))

    async def deangrify_for_user(text: str):
        logger.info(f"angrifier for user={user_id} called!")
        return await deangrify(text)

    if not (angrifier := users_to_angrifiers.get(user_id)):
        users_to_angrifiers[user_id] = debouncer(deangrify_for_user)
        angrifier = users_to_angrifiers[user_id]

    return angrifier


@local_handler.register(event_name=EventNames.INLINE_DEANGRIFY)
async def deangrify_inline(event: Event):
    event_name, payload = event
    payload_model = InlineDeangrifyPayload(**payload)
    user_query = payload_model.query
    deangrify_for_user = await get_deangrifier_for_user(payload_model.user_id)
    if user_query:
        angrify_for_user_deb = await deangrify_for_user(user_query)
        calm_text = await angrify_for_user_deb
        logger.debug(f"calm text output is: {calm_text}")

        await answer_inline_query(
            AnswerInlineQueryBody(
                inline_query_id=payload_model.query_id,
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
