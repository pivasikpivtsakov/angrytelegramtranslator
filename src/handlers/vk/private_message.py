from fastapi_events.typing import Event
from fastapi_events.handlers.local import local_handler
from fastapi_events.registry.payload_schema import registry as payload_schema

from angry_api import deangrify
from vk_api.methods import messages_send
from .event_names import EventNames
from handlers.base_payload import BasePayload
from pydantic import ConfigDict


@payload_schema.register(event_name=EventNames.PRIVATE_MESSAGE)
class PrivateMessagePayload(BasePayload):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    user_id_from: int
    text: str


@local_handler.register(event_name=EventNames.PRIVATE_MESSAGE)
async def respond_to_private_message(event: Event):
    event_name, payload = event
    payload_model = PrivateMessagePayload(**payload)
    in_text = payload_model.text
    from_id = payload_model.user_id_from
    deangrified_text = await deangrify(in_text)
    await messages_send(from_id, deangrified_text)
