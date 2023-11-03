import re
import httpx
from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse
from config import SDEK_LOGIN, SDEK_PASS
from typing import Union
import asyncio
from .schema import Order, Sender, Phone, Recipient, ToLocation, FromLocation, Services, Packages
from model.data.address import Address

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
    
    async def create_order(self, name_of_recepient: str, email: str, phone_of_recepient: Phone, address_of_recepient: Address, comment: str):
        token = await get_token()
        headers = {'Authorization': f'Bearer {token}'}
        phone = Phone(number="905073361421")
        sender = Sender(company="NVİTAL SAĞLIK HİZMETLERİ SANAYİ VE TİCARET LİMİTED ŞİRKETİ", name="Айгерим", phones=[phone])
        recipient = Recipient(name=name_of_recepient, email=email, phones=[phone_of_recepient])
        
        from_location = FromLocation(code=11354, city="Стамбул", country_code="TR", country="Турция", region="Стамбул", region_code=788, longitude=0, latitude=0, address="Cumhuriyet, Kazım Orbay Cd. no3, 34381 Şişli/İstanbul, Турция")
        to_location = ToLocation(postal_code=address_of_recepient.postal_code, country_code=address_of_recepient.code, city=address_of_recepient.city, address=address_of_recepient.address)
        order = Order(type=2, tariff_code=293, sender=sender, recipient=recipient, from_location=from_location, to_location=to_location, packages=[Packages(number="1", weight=1, length=1, width=1, height=1, comment=comment)])
        if token:
            async with httpx.AsyncClient(headers=headers) as client:
                response = await client.post('https://api.cdek.ru/v2/orders', json=order.model_dump())
                return response.json()
        return None
    
    async def refuse_order(self, sdek_uuid: str):
        token = await get_token()
        headers = {'Authorization': f'Bearer {token}'}
        if token:
            async with httpx.AsyncClient(headers=headers) as client:
                response = await client.post(f'https://api.cdek.ru/v2/orders/{sdek_uuid}/refusal')
                return response.json()
        return None




