'''
{
    "type": 2,
    "tariff_code": 119,
    "comment": "Новый заказ",
    "shipment_point": "MSK67",
    "sender": {
        "company": "Компания",
        "name": "Петров Петр",
        "email": "msk@cdek.ru",
        "phones": [
            {
                "number": "+79134000101"
            }
        ]
    },
    "recipient": {
        "company": "Иванов Иван",
        "name": "Иванов Иван",
        "passport_series": "5008",
        "passport_number": "345123",
        "passport_date_of_issue": "2019-03-12",
        "passport_organization": "ОВД Москвы",
        "tin": "123546789",
        "email": "email@gmail.com",
        "phones": [
            {
                "number": "+79134000404"
            }
        ]
    },
    "to_location": {
        "code": "44",
        "fias_guid": "0c5b2444-70a0-4932-980c-b4dc0d3f02b5",
        "postal_code": "109004",
        "longitude": 37.6204,
        "latitude": 55.754,
        "country_code": "RU",
        "region": "Москва",
        "sub_region": "Москва",
        "city": "Москва",
        "kladr_code": "7700000000000",
        "address": "ул. Блюхера, 32"
    },
    "services": [
        {
            "code": "INSURANCE",
            "parameter": "3000"
        }
    ],
    "packages": [
        {
            "number": "bar-001",
            "weight": "1000",
            "length": 10,
            "width": 140,
            "height": 140,
            "comment": "Комментарий к упаковке"
        }
    ]
}

'''
from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

class Phone(BaseModel):
    number: str
    additional: Optional[str] = None

class Sender(BaseModel):
    company: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phones: list[Phone]
    passport_series: Optional[str] = None
    passport_number: Optional[str] = None
    passport_date_of_issue: Optional[datetime.date] = None
    passport_organization: Optional[str] = None
    tin: Optional[str] = None
    passport_date_of_birth: Optional[datetime.date] = None

class Recipient(BaseModel):
    company: Optional[str] = None
    name: str
    passport_series: Optional[str] = None
    passport_number: Optional[str] = None
    passport_date_of_issue: Optional[datetime.date] = None
    passport_organization: Optional[str] = None
    tin: Optional[str] = None
    passport_date_of_birth: Optional[datetime.date] = None
    email: Optional[EmailStr] = None
    phones: list[Phone]

class ToLocation(BaseModel):
    code: Optional[str] = None
    fias_guid: Optional[str] = None
    postal_code: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    country_code: Optional[str] = None
    region: Optional[str] = None
    sub_region: Optional[str] = None
    city: Optional[str] = None
    kladr_code: Optional[str] = None
    address: str

class FromLocation(BaseModel):
    code: Optional[int] = None
    city: Optional[str] = None
    country_code: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    region_code: Optional[int] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    address: str


class Services(BaseModel):
    code: str
    parameter: Optional[str] = None

class Packages(BaseModel):
    number: str
    weight: int
    length: int
    width: int
    height: int
    comment: Optional[str] = None

class Order(BaseModel):
    type: Optional[int] = None
    tariff_code: int
    comment: Optional[str] = None
    # shipment_point: str
    sender: Sender
    recipient: Recipient
    from_location: FromLocation
    to_location: ToLocation
    services: Optional[list[Services]] = None
    packages: list[Packages]
