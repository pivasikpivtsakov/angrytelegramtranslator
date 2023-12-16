from fastapi_events.typing import Event
from fastapi_events.handlers.local import local_handler
from fastapi_events.registry.payload_schema import registry as payload_schema
from motor.motor_asyncio import AsyncIOMotorDatabase

from database.models import LangResourceQueries
from env_config import BOT_NAME
from handlers.base_payload import BasePayload
from .event_names import EventNames
from telegram_api.methods import send_photo, SendPhotoBody, send_message, SendMessageBody
from pydantic import ConfigDict


@payload_schema.register(event_name=EventNames.PRIVATE_MESSAGE)
class PrivateMessagePayload(BasePayload):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    user_id_from: int
    text: str
    user_lang: str
    db: AsyncIOMotorDatabase


@local_handler.register(event_name=EventNames.PRIVATE_MESSAGE)
async def respond_to_private_message(event: Event):
    event_name, payload = event
    payload_model = PrivateMessagePayload(**payload)
    in_text = payload_model.text
    from_id = payload_model.user_id_from
    db = payload_model.db
    user_lang = payload_model.user_lang
    if in_text == "/start":
        out_text = (
            f"Напишите @{BOT_NAME} в поле для ввода сообщения. "
            f"Затем мощно выругайтесь и подождите. Сверху появится переведенная фраза. "
        )
        await send_photo(
            SendPhotoBody(
                chat_id=from_id,
                photo="AgACAgIAAxkDAAMvZQsvhzrDYpvGO31yxQABEb2uQXURAAJX0jEbM39YSEG-o7ZSjuCxAQADAgADeAADMAQ",
                caption=out_text
            )
        )
    elif in_text == "/lang":
        pass

        # send_message()
    elif in_text == "/donate":
        queries = LangResourceQueries(db)
        donate_options = await queries.get_value_for_lang(user_lang, "donateTo")
        if donate_options is not None:
            response_text = donate_options.value
            await send_message(SendMessageBody(chat_id=from_id, text=response_text))
