from pydantic import BaseModel

from telegram.models import InlineQuery


class Update(BaseModel):
    update_id: int
    inline_query: InlineQuery
