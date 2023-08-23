from typing import Any

from pydantic import BaseModel


class InlineQueryResultsButton(BaseModel):
    text: str
    start_parameter: str | None = None
    web_app: Any = None
