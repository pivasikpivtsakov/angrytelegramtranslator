import logging

from pydantic import BaseModel

from ..utils import make_tg_request, Method, API_ROOT

logger = logging.getLogger(__name__)


class Body(BaseModel):
    url: str


async def set_webhook():
    return await make_tg_request(Method.SETWEBHOOK, Body(url=API_ROOT))
