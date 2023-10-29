from pydantic import BaseModel
import datetime
from typing import Union

def get_date_now():
    return datetime.datetime.now()

class ReviewSchema(BaseModel):
    name_of_user: str
    comment: str
    user_id: int
    product_id: int
    created_at: Union[datetime.datetime, str] = get_date_now()
    rating: int

class ReviewCreate(BaseModel):
    rating: int
    comment: str