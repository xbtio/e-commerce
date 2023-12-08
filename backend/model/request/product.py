from pydantic import BaseModel
from typing import Optional, List
from .product_description import ProductDescriptionCreateSchema


class ProductSchema(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
    category_id: int
    image: Optional[str] = None
    rating: Optional[int] = None
    number_of_ratings: Optional[int] = None

class ProductCreateSchema(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
    category_id: int
    image: Optional[str] = None
    weigth: int
    length: int
    width: int
    height: int
 
class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    category_id: Optional[int] = None
    image: Optional[str] = None
    weigth: Optional[int] = None
    length: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
   