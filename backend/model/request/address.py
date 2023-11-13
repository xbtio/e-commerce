from pydantic import BaseModel
from typing import Optional, Union
import datetime


# create addresscreates 
class AddressCreate(BaseModel):
    address: str
    city: str
    country: str
    postal_code: str

class AddressUpdate(BaseModel):
    address: Optional[Union[str, None]] = None
    city: Optional[Union[str, None]] = None
    country: Optional[Union[str, None]] = None
    postal_code: Optional[Union[str, None]] = None