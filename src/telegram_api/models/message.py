from pydantic import BaseModel, Field

from .chat import Chat
from .user import User


class Message(BaseModel):
    message_id: int
    message_thread_id: int | None = None
    from_: User | None = Field(None, alias="from")
    sender_chat: Chat | None = None
    date: int
    chat: Chat
    text: str | None = None
