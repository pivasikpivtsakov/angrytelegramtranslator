from pydantic import BaseModel


class InputMessageContent(BaseModel):
    message_text: str
