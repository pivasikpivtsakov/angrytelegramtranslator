import logging
from typing import Any

import httpx
from httpx import HTTPError

from env_config import VK_API_VERSION, VK_ACCESS_TOKEN
from .method import Method
from .urls import VKBOTAPIURL

logger = logging.getLogger(__name__)


async def make_vk_request(
        method: Method, user_params: dict[str, str | int] | None = None,
) -> Any:
    methodval = method.value
    logger.info(f"making request to vk method={methodval}")
    logger.debug(f"with user_params={user_params}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{VKBOTAPIURL}/{methodval}",
                params={
                    "v": VK_API_VERSION,
                    "access_token": VK_ACCESS_TOKEN,
                    **user_params,
                },
            )
            response_json = response.json()
            if response.status_code == 200:
                return response_json
            else:
                logger.error(f"vk api returned error status={response.status_code} body={response_json}")
                return response_json
    except HTTPError as e:
        logger.critical("failed to make request to vk api")
        logger.exception(e)
        raise e
