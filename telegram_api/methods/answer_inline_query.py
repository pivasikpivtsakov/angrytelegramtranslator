import logging
from typing import Optional

from ..models import InlineQueryResultArticle
from ..utils import make_tg_request, Method, FormDataModel

logger = logging.getLogger(__name__)


class Body(FormDataModel):
    inline_query_id: str
    results: Optional[list[InlineQueryResultArticle]] = None


async def answer_inline_query(body: Body):
    return await make_tg_request(Method.ANSWERINLINEQUERY, body)
