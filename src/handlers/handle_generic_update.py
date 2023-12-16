from typing import TYPE_CHECKING, Union

from fastapi_events.dispatcher import dispatch

if TYPE_CHECKING:
    from .base_payload import BasePayload
    from .telegram import TgEventNames
    from .vk import VkEventNames


def handle_update(event_name: Union["TgEventNames", "VkEventNames"], payload: "BasePayload"):
    dispatch(
        event_name,
        payload.model_dump(),
    )
