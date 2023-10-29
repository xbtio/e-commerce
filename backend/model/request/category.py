from pydantic import BaseModel
from typing import Optional

class CategorySchema(BaseModel):
    name: str
    description: str
