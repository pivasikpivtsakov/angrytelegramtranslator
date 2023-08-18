import logging

import httpx
from httpx import HTTPError
from pydantic import BaseModel

from .method import Method
from .urls import TGBOTAPIURL

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def make_tg_request(method: Method, data: BaseModel):
    logger.info(f"making request to method={method}")
    logger.debug(f"with data={data.dict()}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{TGBOTAPIURL}/{method}",
                data=data.dict()
            )
            response_json = response.json()
            if response.status_code == 200:
                return response_json
            else:
                logger.error(f"telegram api returned error status={response.status_code} body={response_json}")
                return response_json
    except HTTPError as e:
        logger.critical("failed to make request to telegram api")
        logger.exception(e)
        raise e
