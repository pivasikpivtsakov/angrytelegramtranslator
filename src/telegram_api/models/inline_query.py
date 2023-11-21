from pydantic import BaseModel, Field

from .user import User


class InlineQuery(BaseModel):
    id: str
    from_: User = Field(alias="from")
    chat_type: str | None = None
    query: str
    offset: str
