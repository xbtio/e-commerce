from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

'''
class OrderRequest(Base):  
    __tablename__ = 'order_requests'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_email: Mapped[str] = mapped_column(String(250), nullable=False)   
    name_of_recipient: Mapped[str] = mapped_column(String(150), nullable=False)
    phone_of_recipient: Mapped[str] = mapped_column(String(150), nullable=False)
    additional_num: Mapped[str] = mapped_column(String(150), nullable=False)
    address_id: Mapped[int] = mapped_column(Integer, ForeignKey('address.id'), nullable=False)
    order_weigth: Mapped[int] = mapped_column(Integer, nullable=False)
    order_status: Mapped[str] = mapped_column(String(150), default='pending', nullable=False)
    passport_series: Mapped[str] = mapped_column(String(4), nullable=True)
    passport_number: Mapped[str] = mapped_column(String(30), nullable=True)
    passport_date_of_issue: Mapped[Date] = mapped_column(Date, nullable=True)
    passport_organization: Mapped[str] = mapped_column(String(255), nullable=True)
    tin: Mapped[str] = mapped_column(String(12), nullable=True)


'''

class OrderRequestCreate(BaseModel):
    name: str
    phone: str
    additional_num: str
    passport_series: Optional[str] = None
    passport_number: Optional[str] = None
    passport_date_of_issue: Optional[datetime.date] = None
    passport_organization: Optional[str] = None
    tin: Optional[str] = None