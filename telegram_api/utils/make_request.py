import logging
from typing import Any, Tuple

import httpx
from httpx import HTTPError

from . import FormDataModel
from .method import Method
from .urls import TGBOTAPIURL
from ..models import InputFile

logger = logging.getLogger(__name__)


async def make_tg_request(
        method: Method, formdata: FormDataModel | None = None, inputfile: InputFile | None = None
) -> Any:
    methodval = method.value
    data = formdata.as_form_data_dict()
    logger.info(f"making request to tg method={methodval}")
    logger.debug(f"with data={data}")
    try:
        async with httpx.AsyncClient() as client:
            if inputfile is not None:
                file_data = open(inputfile.path_to_file, "rb")
                files_param = {"files": {inputfile.type: file_data}}
            else:
                files_param = {}
            response = await client.post(
                f"{TGBOTAPIURL}/{methodval}",
                data=data,
                **files_param
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
