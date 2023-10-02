from enum import StrEnum

from pydantic import BaseModel


class NotificationType(StrEnum):
    CONFIRMATION = "confirmation"
    MESSAGE_NEW = "message_new"


class Notification(BaseModel):
    type: str
    group_id: int
