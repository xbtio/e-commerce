from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from model.data.product import Category
from sqlalchemy import update, delete, select, insert


class CategoryRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    async def insert_category(self, category):
        try:
            await self.db.execute(insert(Category).values(**category))
            await self.db.commit()
        except Exception as e:
            print(f"Exception during category insertion: {e}")
            return False 
        return True
    
    async def update_category(self, id: int, details: Dict[str, Any]):
        try:
            await self.db.execute(update(Category).where(Category.id == id).values(**details))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True
    
    async def delete_category(self, id: int):
        try:
            await self.db.execute(delete(Category).where(Category.id == id))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True
    
    async def get_all_categories(self):
        result = await self.db.execute(select(Category))
        return result.scalars().all()
    
    async def get_category_by_id(self, id: int):
        result =  await self.db.execute(select(Category).where(Category.id == id))
        return result.scalars().one_or_none()
