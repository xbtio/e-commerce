from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from model.data.product import Product
from sqlalchemy import update, delete, select, insert


class ProductRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    async def insert_product(self, product: Dict):
        try:
            await self.db.execute(insert(Product).values(**product))  
            await self.db.commit()
        except Exception as e:
            print(f"Exception during product insertion: {e}")
            return False 
        return True
    
    async def update_product(self, id: int, details: Dict[str, Any]):
        try:
            await self.db.execute(update(Product).where(Product.id == id).values(**details))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True

    async def delete_product(self, id: int):
        try:
            await self.db.execute(delete(Product).where(Product.id == id))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True
    
    async def get_all_products(self):
        result = await self.db.execute(select(Product))
        return result.scalars().all()
    
    async def get_product_by_id(self, id: int):
        result =  await self.db.execute(select(Product).where(Product.id == id))
        return result.scalars().one_or_none()