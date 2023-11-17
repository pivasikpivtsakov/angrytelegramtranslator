from pydantic import BaseModel


class InputFile(BaseModel):
    path_to_file: str
    type: str
