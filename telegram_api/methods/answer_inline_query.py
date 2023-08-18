import logging
from typing import Optional

from pydantic import BaseModel

from telegram_api.models import InlineQueryResultArticle
from ..utils import make_tg_request, Method

logger = logging.getLogger(__name__)


class Body(BaseModel):
    inline_query_id: str
    results: Optional[list[InlineQueryResultArticle]] = None


async def answer_inline_query(body: Body):
    return await make_tg_request(Method.ANSWERINLINEQUERY, body)
