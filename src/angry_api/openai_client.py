from functools import lru_cache

import openai

import env_config


@lru_cache
def get_openai_client():
    return openai.AsyncClient(api_key=env_config.OPENAI_API_KEY)
