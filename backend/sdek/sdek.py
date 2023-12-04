import re
import httpx
from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse
from config import SDEK_LOGIN, SDEK_PASS
from typing import Union
import asyncio
from .schema import Order, Sender, Phone, Recipient, ToLocation, FromLocation, Services, Packages
from model.data.address import Address
from model.data.model import User
from typing import Optional
import datetime

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
    
async def make_order_request(order: Order):
    token = await get_token()
    headers = {'Authorization': f'Bearer {token}'}
    if token:
        async with httpx.AsyncClient(headers=headers) as client:
            response = await client.post('https://api.cdek.ru/v2/orders', json=order.model_dump())
            return response.json()
    return None


class SdekService:
    async def get_status_about_order(self, cdek_number):
        token = await get_token()
        headers = {'Authorization': f'Bearer {token}'}
        if token:
            async with httpx.AsyncClient(headers=headers) as client:
                response = await client.get(f'https://api.cdek.ru/v2/orders?cdek_number={cdek_number}')
                return response.json()
        return None
    
    async def create_order(self, name_of_recepient: str, user_email: str, phone_of_recepient: str, additional_num: str, address_of_recepient: Address, length: int, width: int, heigth: int, weigth: int, passport_series: Optional[str], passport_number: Optional[str], passport_date_of_issue: Optional[datetime.date] = None, passport_organization: Optional[str] = None, tin: Optional[str] = None):
        phone = Phone(number="905073361421")
        sender = Sender(company="Invittal", name="Айгерим", phones=[phone])
        recipient = Recipient(name=name_of_recepient, email=user_email, phones=[Phone(number=phone_of_recepient, additional=additional_num)], passport_series=passport_series, passport_number=passport_number, passport_date_of_issue=passport_date_of_issue, passport_organization=passport_organization, tin=tin)
        
        from_location = FromLocation(code=11354, city="Стамбул", country_code="TR", country="Турция", region="Стамбул", region_code=788, longitude=0, latitude=0, address="Cumhuriyet, Kazım Orbay Cd. no3, 34381 Şişli/İstanbul, Турция")
        to_location = ToLocation(postal_code=address_of_recepient.postal_code, country_code=address_of_recepient.code, city=address_of_recepient.city, address=address_of_recepient.address)

        

        order = Order(type=2, tariff_code=293, sender=sender, recipient=recipient, from_location=from_location, to_location=to_location, packages=[Packages(number="1", weight=weigth, length=length, width=width, height=heigth, comment='Коробка')])
        
        response = await make_order_request(order)
        return response
    
    async def refuse_order(self, sdek_uuid: str):
        token = await get_token()
        headers = {'Authorization': f'Bearer {token}'}
        if token:
            async with httpx.AsyncClient(headers=headers) as client:
                response = await client.post(f'https://api.cdek.ru/v2/orders/{sdek_uuid}/refusal')
                return response.json()
        return None




