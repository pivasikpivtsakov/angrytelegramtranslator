from pydantic import BaseModel

from .input_message_content import InputMessageContent


class InlineQueryResultArticle(BaseModel):
    type: str = "article"
    id: str
    title: str
    input_message_content: InputMessageContent
    description: str | None = None
