from pydantic import BaseModel


class InputTextMessageContent(BaseModel):
    message_text: str
