from pydantic import BaseModel


class InputInvoiceMessageContent(BaseModel):
    message_text: str
