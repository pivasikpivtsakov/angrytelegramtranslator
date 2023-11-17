import logging

from ..models import InlineQueryResultArticle, InlineQueryResultsButton
from ..utils import make_tg_request, Method, FormDataModel

logger = logging.getLogger(__name__)


class Body(FormDataModel):
    inline_query_id: str
    results: list[InlineQueryResultArticle]
    button: InlineQueryResultsButton | None = None


async def answer_inline_query(body: Body):
    return await make_tg_request(Method.ANSWERINLINEQUERY, body)
