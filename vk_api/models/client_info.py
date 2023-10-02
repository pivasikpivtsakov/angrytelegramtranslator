from pydantic import BaseModel


class ClientInfo(BaseModel):
    client: str
    version: str
    platform: str
    lang: str
    button_action: dict[str, str | int | bool | list[dict]]
