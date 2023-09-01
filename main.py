import logging
from contextlib import asynccontextmanager
from typing import Callable

import openai
from fastapi import FastAPI, Response, Request
from fastapi.routing import APIRoute, APIRouter
from fastapi_events.dispatcher import dispatch
from fastapi_events.handlers.local import local_handler
from fastapi_events.middleware import EventHandlerASGIMiddleware
from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse

from env_config import TG_API_TOKEN, OPENAI_API_KEY
from handlers import EventNames, InlineDeangrifyPayload
from telegram_api.methods import set_webhook
from telegram_api.models import Update


def log_info(req_body, res_body):
    logging.info(req_body)
    logging.info(res_body)


class LoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            req_body = await request.body()
            response = await original_route_handler(request)

            if isinstance(response, StreamingResponse):
                res_body = b''
                async for item in response.body_iterator:
                    res_body += item

                task = BackgroundTask(log_info, req_body, res_body)
                return Response(content=res_body, status_code=response.status_code,
                                headers=dict(response.headers), media_type=response.media_type, background=task)
            else:
                res_body = response.body
                response.background = BackgroundTask(log_info, req_body, res_body)
                return response

        return custom_route_handler


app = FastAPI()
app.add_middleware(
    EventHandlerASGIMiddleware,
    handlers=[local_handler],
)
router = APIRouter(route_class=LoggingRoute)
logging.basicConfig(level=logging.DEBUG)
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.debug("setting webhook...")
    webhook_result = await set_webhook()
    logger.info(f"setwebhook result: \n {webhook_result}")
    logger.debug("setting openai api key...")
    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
        logger.info("openai api key is set")
    else:
        logger.error("openai api key unset!")
    yield


@router.get("/")
async def root():
    return "healthy"


@router.post(f"/{TG_API_TOKEN}")
async def api_root(request: Request):
    body = await request.body()
    logger.debug(body)
    return None
    # logger.info(f"received update from tg: {body.json()}")
    payload = InlineDeangrifyPayload(
        user_id=body.inline_query.from_.id,
        query=body.inline_query.query.strip("\r\n "),
        query_id=body.inline_query.id,
    )
    dispatch(
        EventNames.INLINE_DEANGRIFY,
        payload.dict()
    )
    return None


app.include_router(router)
