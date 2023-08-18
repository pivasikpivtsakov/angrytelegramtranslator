import logging

from ..utils import make_tg_request, Method, API_ROOT, FormDataModel

logger = logging.getLogger(__name__)


class Body(FormDataModel):
    url: str


async def set_webhook():
    return await make_tg_request(Method.SETWEBHOOK, Body(url=API_ROOT))
