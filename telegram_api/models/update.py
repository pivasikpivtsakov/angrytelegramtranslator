from pydantic import BaseModel

from . import InlineQuery


class Update(BaseModel):
    update_id: int
    inline_query: InlineQuery
