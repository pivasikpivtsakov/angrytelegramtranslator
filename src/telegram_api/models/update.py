from pydantic import BaseModel

from . import InlineQuery, Message


class Update(BaseModel):
    update_id: int
    inline_query: InlineQuery | None = None
    message: Message | None = None
