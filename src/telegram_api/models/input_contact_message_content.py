from pydantic import BaseModel


class InputContactMessageContent(BaseModel):
    message_text: str
