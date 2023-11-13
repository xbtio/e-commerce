from pydantic import BaseModel
from typing import Optional

class ProductDescriptionCreateSchema(BaseModel):
    product_id: int
    title: str
    description: str

class ProductDescriptionUpdateSchema(BaseModel):
    id: int
    title: str
    description: str

