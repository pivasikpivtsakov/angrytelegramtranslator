import logging

from fastapi import FastAPI
import httpx as http

from env_config import TG_API_TOKEN
from telegram import answer_inline_query, TGURL_SETWEBHOOK, API_ROOT

app = FastAPI()
logger = logging.Logger(__name__)


@app.on_event("startup")
async def startup():
    async with http.AsyncClient() as client:
        logger.info("setting webhook...")
        response = await client.post(TGURL_SETWEBHOOK, data={"url": API_ROOT})
        logger.info(f"setwebhook result: \n {response.json()}")


@app.get("/")
async def root():
    return "healthy"


@app.post(f"/{TG_API_TOKEN}")
async def api_root():
    return await answer_inline_query()
