from pydantic import BaseModel


class Confirmation(BaseModel):
    type: str
    group_id: int
