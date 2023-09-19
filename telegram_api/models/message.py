from pydantic import BaseModel, Field

from .chat import Chat
from .user import User


class Message(BaseModel):
    message_id: int
    message_thread_id: int | None
    from_: User | None = Field(alias="from")
    sender_chat: Chat | None
    date: int
    chat: Chat
    text: str | None
