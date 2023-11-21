from enum import StrEnum

from pydantic import BaseModel

from .message_new_object import MessageNewObject


class NotificationType(StrEnum):
    CONFIRMATION = "confirmation"
    MESSAGE_NEW = "message_new"


class Notification(BaseModel):
    type: str
    event_id: str | None = None
    v: str | None = None
    object: MessageNewObject | None = None
    group_id: int
