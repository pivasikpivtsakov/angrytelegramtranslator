import logging
import os
from typing import Callable

import angry_api
import services
from services import enum_to_set_str

logger = logging.getLogger(__name__)


def _env_get(
        varname: str,
        validation_rule: Callable[[str], bool] | None = None,
        warning_message: str | None = None,
        raise_if_failed=True
) -> str | None:
    """
    :param varname: name of env var
    :param validation_rule: returns True if var passes validation
    :param warning_message: what to print in logs if validation fails
    :param raise_if_failed: raise if var is None or validation failed
    :return: env var value
    """
    varvalue = os.environ.get(varname)
    if not varvalue:
        logger.warning(f"{varname} is unset!")
        if raise_if_failed:
            raise Exception(f"{varname} is unset!")
    if validation_rule is not None:
        if not validation_rule(varvalue):
            logger.warning(warning_message)
            if raise_if_failed:
                raise Exception(f"validation failed for {varname}")
    return varvalue


HOSTNAME = _env_get("HOSTNAME", raise_if_failed=False)

TG_API_TOKEN = _env_get("TG_API_TOKEN")

OPENAI_API_KEY = _env_get("OPENAI_API_KEY")

BOT_NAME = _env_get("BOT_NAME")

DEBOUNCE_SECS = _env_get("DEBOUNCE_SECS", lambda x: x.replace(".", "").isdigit(),
                         "DEBOUNCE_SECS must be positive float")

_app_envs_set = enum_to_set_str(services.AppEnvironments)
ENVIRONMENT = _env_get("ENVIRONMENT", lambda x: x in _app_envs_set,
                       f"ENVIRONMENT must be one of: {_app_envs_set}")

_openai_models_set = enum_to_set_str(angry_api.GptModels)
OPENAI_MODEL = _env_get("OPENAI_MODEL", lambda x: x in _openai_models_set,
                        f"OPENAI_MODEL must be one of: {_openai_models_set}")

DATABASE_URL = _env_get("DATABASE_URL")

VK_API_SECRET = _env_get("VK_API_SECRET")

VK_API_CONFIRMATION_RESPONSE = _env_get("VK_API_CONFIRMATION_RESPONSE")

VK_API_VERSION = _env_get("VK_API_VERSION")

VK_ACCESS_TOKEN = _env_get("VK_ACCESS_TOKEN")
