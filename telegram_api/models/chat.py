from pydantic import BaseModel


class Chat(BaseModel):
    id: int
    type: str
