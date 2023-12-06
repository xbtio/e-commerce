from pydantic import BaseModel
from typing import Optional

class ProductImageCreateSchema(BaseModel):
    image: str

class ProductImageUpdateSchema(BaseModel):
    image: str