import logging

from .event_names import EventNames
from .private_message import PrivateMessagePayload
from handlers.handle_generic_update import handle_update
from vk_api.models import Notification

logger = logging.getLogger(__name__)


def handle_private_message(body: Notification):
    logger.info("received vk private message")
    payload = PrivateMessagePayload(
        user_id_from=body.object.message.peer_id,
        text=body.object.message.text
    )
    event_name = EventNames.PRIVATE_MESSAGE
    handle_update(event_name, payload)
