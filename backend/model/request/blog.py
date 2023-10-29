from email.mime import image
from pydantic import BaseModel
from typing import Optional, Union
import datetime

def get_date_now():
    return datetime.datetime.now()

class BlogSchema(BaseModel):
    title: str
    content: str
    image: Optional[str] = None
    published: Union[datetime.datetime, str] = get_date_now()

class BlogCreate(BaseModel):
    title: str
    content: str
    image: Optional[str] = None

class ReviewBlogCreate(BaseModel):
    comment: str
    blog_id: int

class ReviewBlogSchema(BaseModel):
    user_id: int
    comment: str
    blog_id: int
    date: Union[datetime.datetime, str] = get_date_now()