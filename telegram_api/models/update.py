from pydantic import BaseModel

from . import InlineQuery, Message


class Update(BaseModel):
    update_id: int
    inline_query: InlineQuery | None
    message: Message | None
