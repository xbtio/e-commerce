from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from model.data.product import ProductDescription
from sqlalchemy import update, delete, select, insert

class ProductDescriptionRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    async def insert_product_description(self, product_description: Dict):
        try:
            await self.db.execute(insert(ProductDescription).values(**product_description))  
            await self.db.commit()
        except Exception as e:
            print(f"Exception during product description insertion: {e}")
            return False 
        return True

    async def update_product_description(self, id: int, details: Dict[str, Any]):
        try:
            await self.db.execute(update(ProductDescription).where(ProductDescription.id == id).values(**details))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True
    
    async def delete_product_description(self, id: int):
        try:
            await self.db.execute(delete(ProductDescription).where(ProductDescription.id == id))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True
    
    async def get_product_description_by_product_id(self, id: int):
        result =  await self.db.execute(select(ProductDescription).where(ProductDescription.product_id == id))
        return result.scalars().all()
    