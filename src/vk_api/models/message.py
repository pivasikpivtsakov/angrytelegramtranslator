from pydantic import BaseModel


class Message(BaseModel):
    id: int
    date: int
    peer_id: int
    from_id: int
    text: str
    random_id: int
    ref: str | None = None
    ref_source: str | None = None
    attachments: list[dict]
