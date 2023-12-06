from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete, select, insert
from model.data.product import ProductImage
from sqlalchemy.orm import joinedload, contains_eager, selectinload, aliased

class ProductImageRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    async def insert_product_image(self, product_image: Dict):
        try:
            await self.db.execute(insert(ProductImage).values(**product_image))  
            await self.db.commit()
        except Exception as e:
            print(f"Exception during product image insertion: {e}")
            return False 
        return True

    async def update_product_image(self, id: int, details: Dict[str, Any]):
        try:
            await self.db.execute(update(ProductImage).where(ProductImage.id == id).values(**details))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True
    
    async def delete_product_image(self, id: int):
        try:
            await self.db.execute(delete(ProductImage).where(ProductImage.id == id))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True
    
    async def get_product_image_by_product_id(self, id: int):
        result =  await self.db.execute(select(ProductImage).where(ProductImage.product_id == id))
        return result.scalars().all()
    
    async def get_product_image_by_id(self, id: int):
        result =  await self.db.execute(select(ProductImage).where(ProductImage.id == id))
        return result.scalars().one_or_none()
    
    async def get_all_product_images(self):
        result = await self.db.execute(select(ProductImage))
        return result.scalars().all()