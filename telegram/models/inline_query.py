from pydantic import BaseModel

from .user import User


class InlineQuery(BaseModel):
    id: str
    _from: User
    chat_type: str
    query: str
    offset: str
