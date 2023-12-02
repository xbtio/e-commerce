from pydantic import BaseModel
from typing import Optional

class CategorySchema(BaseModel):
    name: str
    parent_category_id: int
    description: str

class ParentCategorySchema(BaseModel):
    name: str