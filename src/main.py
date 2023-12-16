import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi.routing import APIRouter
from fastapi_events.handlers.local import local_handler
from fastapi_events.middleware import EventHandlerASGIMiddleware
from motor.motor_asyncio import AsyncIOMotorDatabase

import env_config
from database import get_db
from services import AppEnvironments
from telegram_api.methods import set_webhook
from telegram_api.models import Update
from vk_api.models import Notification, NotificationType
from handlers import tg_handle_inline_deangrify, tg_handle_private_message, vk_handle_private_message


@asynccontextmanager
async def lifespan(_app: FastAPI):
    if env_config.ENVIRONMENT == AppEnvironments.PRODUCTION:
        # on every app launch, tell telegram that it should send requests to our url defined in env var
        logger.debug("setting webhook...")
        webhook_result = await set_webhook()
        logger.info(f"setwebhook result: \n {webhook_result}")
    yield

app_kwargs = {}
if env_config.ENVIRONMENT == AppEnvironments.PRODUCTION:
    app_kwargs["openapi_url"] = None
app = FastAPI(
    lifespan=lifespan,
    **app_kwargs
)
app.add_middleware(
    EventHandlerASGIMiddleware,
    handlers=[local_handler],
)
router = APIRouter()
logging.basicConfig(level=logging.DEBUG)
# reconfigure actually exists on sys.stderr object
# noinspection PyUnresolvedReferences
sys.stderr.reconfigure(encoding="utf-8")
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    reqbody = exc.body
    logger.error(
        f"received invalid data in webhook. Maybe telegram api changed? Body={reqbody}. Validation error below"
    )
    logger.exception(exc)
    return await request_validation_exception_handler(request, exc)


@router.get("/")
async def root():
    return "healthy"


@router.post(f"/{env_config.TG_API_TOKEN}")
async def tg_api_root(body: Update, db: AsyncIOMotorDatabase = Depends(get_db)):
    logger.debug(f"deserialized tg update: {body}")
    if body.inline_query is not None:
        tg_handle_inline_deangrify(body)
    elif body.message is not None:
        tg_handle_private_message(body, db)
    return None


@router.post(f"/{env_config.VK_API_SECRET}")
async def vk_api_root(body: Notification, db: AsyncIOMotorDatabase = Depends(get_db)):
    logger.debug(f"deserialized vk update: {body}")
    if body.type == NotificationType.CONFIRMATION:
        return PlainTextResponse(content=env_config.VK_API_CONFIRMATION_RESPONSE)
    elif body.type == NotificationType.MESSAGE_NEW:
        vk_handle_private_message(body)
    return PlainTextResponse(content="ok")


app.include_router(router)
