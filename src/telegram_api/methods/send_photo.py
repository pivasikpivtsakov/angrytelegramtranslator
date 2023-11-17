from ..models import InputFile
from ..utils import make_tg_request, Method, FormDataModel


class Body(FormDataModel):
    chat_id: str | int
    photo: InputFile | str
    caption: str | None


async def send_photo(body: Body):
    if isinstance(body.photo, InputFile):
        inputfile = body.photo
        body.photo = None
    else:
        inputfile = None
    return await make_tg_request(Method.SEND_PHOTO, body, inputfile)
