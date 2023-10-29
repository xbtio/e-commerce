import re
import httpx
import asyncio

async def get_country_info(name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://restcountries.com/v3.1/name/{name}')
        content = await response.aread()
        result = re.search(r'"cca2":"(.*?)"', content.decode('utf-8'))
        if result is not None:
            return result.group(1)
        return None

