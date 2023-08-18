from pydantic import BaseModel


class User(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    username: str
    language_code: str
    is_premium: bool
