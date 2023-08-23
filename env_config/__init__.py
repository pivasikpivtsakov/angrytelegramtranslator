import os


def _env_get(varname: str) -> str | None:
    return os.environ.get(varname)


HOSTNAME = _env_get("HOSTNAME")
TG_API_TOKEN = _env_get("TG_API_TOKEN")
OPENAI_API_KEY = _env_get("OPENAI_API_KEY")
BOT_NAME = _env_get("BOT_NAME")
