from fastapi_events.typing import Event
from fastapi_events.handlers.local import local_handler
from fastapi_events.registry.payload_schema import registry as payload_schema

from handlers import EventNames, BasePayload


@payload_schema.register(event_name=EventNames.PRIVATE_MESSAGE)
class PrivateMessagePayload(BasePayload):
    class Config:
        arbitrary_types_allowed = True

    user_id_from: int
    text: str


@local_handler.register(event_name=EventNames.PRIVATE_MESSAGE)
async def respond_to_private_message(event: Event):
    event_name, payload = event
    payload_model = PrivateMessagePayload(**payload)
