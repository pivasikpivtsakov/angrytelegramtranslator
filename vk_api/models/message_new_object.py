from pydantic import BaseModel

from .client_info import ClientInfo
from .message import Message


class MessageNewObject(BaseModel):
    message: Message
    client_info: ClientInfo
