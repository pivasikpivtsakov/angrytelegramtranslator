import logging
import sys
from contextlib import asynccontextmanager

import openai
from fastapi import FastAPI, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi.routing import APIRouter
from fastapi_events.dispatcher import dispatch
from fastapi_events.handlers.local import local_handler
from fastapi_events.middleware import EventHandlerASGIMiddleware

import env_config
from angry_api import deangrify
from handlers import EventNames, InlineDeangrifyPayload, BasePayload, TgPrivateMessagePayload, VkPrivateMessagePayload, VkEventNames
from services import AppEnvironments
from telegram_api.methods import set_webhook
from telegram_api.models import Update
from vk_api.methods import messages_send
from vk_api.models import Notification, NotificationType


@asynccontextmanager
async def lifespan(_app: FastAPI):
    if env_config.ENVIRONMENT == AppEnvironments.PRODUCTION:
        logger.debug("setting webhook...")
        webhook_result = await set_webhook()
        logger.info(f"setwebhook result: \n {webhook_result}")
    logger.debug("setting openai api key...")
    if env_config.OPENAI_API_KEY:
        openai.api_key = env_config.OPENAI_API_KEY
        logger.info("openai api key is set")
    else:
        logger.error("openai api key unset!")
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


def _handle_update(event_name: EventNames, payload: BasePayload):
    dispatch(
        event_name,
        payload.dict()
    )


def handle_inline_deangrify(body: Update):
    logger.info("received inline query")
    payload = InlineDeangrifyPayload(
        user_id=body.inline_query.from_.id,
        query=body.inline_query.query,
        query_id=body.inline_query.id,
    )
    event_name = EventNames.INLINE_DEANGRIFY
    _handle_update(event_name, payload)


def handle_private_message(body: Update):
    logger.info("received private message")
    payload = TgPrivateMessagePayload(
        user_id_from=body.message.from_.id,
        text=body.message.text,
    )
    event_name = EventNames.PRIVATE_MESSAGE
    _handle_update(event_name, payload)


async def handle_vk_message(body: Notification):
    logger.info("received vk private message")
    payload = VkPrivateMessagePayload(
        user_id_from=body.object.message.peer_id,
        text=body.object.message.text
    )
    event_name = VkEventNames.PRIVATE_MESSAGE
    _handle_update(event_name, payload)


@router.post(f"/{env_config.TG_API_TOKEN}")
async def tg_api_root(body: Update):
    logger.debug(f"deserialized tg update: {body}")
    if body.inline_query is not None:
        handle_inline_deangrify(body)
    elif body.message is not None:
        handle_private_message(body)
    return None


@router.post(f"/{env_config.VK_API_SECRET}")
async def vk_api_root(body: Notification, response_class: PlainTextResponse):
    logger.debug(f"deserialized vk update: {body}")
    if body.type == NotificationType.CONFIRMATION:
        return PlainTextResponse(content=env_config.VK_API_CONFIRMATION_RESPONSE)
    elif body.type == NotificationType.MESSAGE_NEW:
        await handle_vk_message(body)
    return PlainTextResponse(content="ok")


app.include_router(router)
