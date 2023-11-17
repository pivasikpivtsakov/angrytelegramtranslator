import random

from ...utils import make_vk_request, Method


async def messages_send(user_id: int, message: str):
    random_id = random.randint(1, 2147483647)
    return await make_vk_request(
        Method.messages_send,
        {
            "random_id": random_id,
            "user_id": user_id,
            "message": message,
        }
    )
