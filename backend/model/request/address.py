from pydantic import BaseModel
from typing import Optional, Union
import datetime

'''
    __tablename__ = 'address'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    address: Mapped[str] = mapped_column(String(300), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)

'''
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