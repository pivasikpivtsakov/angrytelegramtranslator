from ..utils import make_tg_request, Method, FormDataModel


class Body(FormDataModel):
    chat_id: str | int
    text: str


async def send_message(body: Body):
    return await make_tg_request(Method.SEND_MESSAGE, body)
