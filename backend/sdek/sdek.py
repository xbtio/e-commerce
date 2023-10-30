import re
import httpx
from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse
from config import SDEK_LOGIN, SDEK_PASS
from typing import Union
import asyncio

URL = 'https://api.cdek.ru/v2/oauth/token'

params = {'client_id': SDEK_LOGIN, 'client_secret': SDEK_PASS, 'grant_type': 'client_credentials'}

async def get_token():
    async with httpx.AsyncClient() as client:
        response = await client.post(URL, params=params)
        # get access token
        content = await response.aread()
        result = re.search(r'"access_token":"(.*?)"', content.decode('utf-8'))
        if result is not None:
            return result.group(1)
        return None


class SdekService:
    async def get_status_about_order(self, sdeck_id: int):
        token = await get_token()
        headers = {'Authorization': f'Bearer {token}'}
        if token:
            async with httpx.AsyncClient(headers=headers) as client:
                response = await client.get(f'https://api.cdek.ru/v2/orders?cdek_number={sdeck_id}')
                return response.json()['entity']
        return None
    




