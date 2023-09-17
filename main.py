import logging
import sys
from contextlib import asynccontextmanager

import openai
from fastapi import FastAPI, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRouter
from fastapi_events.dispatcher import dispatch
from fastapi_events.handlers.local import local_handler
from fastapi_events.middleware import EventHandlerASGIMiddleware

from services import AppEnvironments
import env_config
from handlers import EventNames, InlineDeangrifyPayload
from telegram_api.methods import set_webhook
from telegram_api.models import Update


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
logging.basicConfig(level=logging.INFO)
# reconfigure actually exists on sys.stderr object
sys.stderr.reconfigure(encoding="utf-8")
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.DEBUG)
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
async def api_root(body: Update):
    if body.inline_query is not None:
        payload = InlineDeangrifyPayload(
            user_id=body.inline_query.from_.id,
            query=body.inline_query.query,
            query_id=body.inline_query.id,
        )
        dispatch(
            EventNames.INLINE_DEANGRIFY,
            payload.dict()
        )
    return None


app.include_router(router)
