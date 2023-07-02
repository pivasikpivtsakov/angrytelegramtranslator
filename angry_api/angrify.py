import httpx as http

from env_config import ANGRY_API_ROOT


async def angrify(text: str):
    async with http.AsyncClient() as client:
        response = await client.post(ANGRY_API_ROOT, json={})
        return response.json()
