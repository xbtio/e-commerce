from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from model.data.product import Product
from sqlalchemy import update, delete, select, insert
from model.data.review import Review
from sqlalchemy import func
from sqlalchemy.sql import text


class ReviewRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    async def insert_review(self, review: Dict):
        try:
            await self.db.execute(insert(Review).values(**review))
            await self.db.commit()
        except Exception as e:
            print(f"Exception during review insertion: {e}")
            return False 
        return True
    
    async def update_review(self, id: int, details: Dict[str, Any]):
        try:
            await self.db.execute(update(Review).where(Review.id == id).values(**details))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True

    async def delete_review(self, id: int):
        try:
            await self.db.execute(delete(Review).where(Review.id == id))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True
    
    async def get_all_reviews(self):
        result = await self.db.execute(select(Review))
        return result.scalars().all()
    
    async def get_review_by_id(self, id: int):
        result =  await self.db.execute(select(Review).where(Review.id == id))
        return result.scalars().first()
    
    async def get_review_by_product_id(self, product_id: int):
        result =  await self.db.execute(select(Review).where(Review.product_id == product_id))
        return result.scalars().all()
    
    async def get_total_rating(self, product_id: int):
        result = await self.db.execute(select(func.sum(Review.rating)).where(Review.product_id == product_id))
        return result.scalars().first()
    
    async def get_total_reviews(self, product_id: int):
        result = await self.db.execute(select(func.count(Review.id)).where(Review.product_id == product_id))
        return result.scalars().first()
        

    async def get_total_number_of_rating(self, product_id: int):
        result = await self.db.execute(select(func.count(Review.id)).where(Review.product_id == product_id))
        return result.scalars().first()