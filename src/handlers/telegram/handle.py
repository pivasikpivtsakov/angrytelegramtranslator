import logging

from motor.motor_asyncio import AsyncIOMotorDatabase

from telegram_api.models import Update
from .event_names import EventNames
from .private_message import PrivateMessagePayload
from .inline_deangrify import InlineDeangrifyPayload
from handlers.handle_generic_update import handle_update

logger = logging.getLogger(__name__)


def handle_inline_deangrify(body: Update):
    logger.info("received inline query")
    payload = InlineDeangrifyPayload(
        user_id=body.inline_query.from_.id,
        query=body.inline_query.query,
        query_id=body.inline_query.id,
    )
    event_name = EventNames.INLINE_DEANGRIFY
    handle_update(event_name, payload)


def handle_private_message(body: Update, db: AsyncIOMotorDatabase):
    logger.info("received private message")
    payload = PrivateMessagePayload(
        user_id_from=body.message.from_.id,
        text=body.message.text,
        user_lang=body.message.from_.language_code,
        db=db,
    )
    event_name = EventNames.PRIVATE_MESSAGE
    handle_update(event_name, payload)
