import logging

import httpx
from httpx import HTTPError

from . import FormDataModel
from .method import Method
from .urls import TGBOTAPIURL


logger = logging.getLogger(__name__)


async def make_tg_request(method: Method, formdata: FormDataModel):
    methodval = method.value
    data = formdata.as_form_data_dict()
    logger.info(f"making request to method={methodval}")
    logger.debug(f"with data={data}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{TGBOTAPIURL}/{methodval}",
                data=data
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
