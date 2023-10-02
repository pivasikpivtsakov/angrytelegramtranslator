from enum import StrEnum

from pydantic import BaseModel

from .message_new_object import MessageNewObject


class NotificationType(StrEnum):
    CONFIRMATION = "confirmation"
    MESSAGE_NEW = "message_new"


class Notification(BaseModel):
    type: str
    event_id: int | None
    v: str | None
    object: MessageNewObject | None
    group_id: int
