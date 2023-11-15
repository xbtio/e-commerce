from pydantic import BaseModel
from typing import Optional

class ProductDescriptionCreateSchema(BaseModel):
    title: str
    description: str

class ProductDescriptionUpdateSchema(BaseModel):
    id: int
    title: str
    description: str

