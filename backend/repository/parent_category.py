from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from model.data.product import ParentCategory
from sqlalchemy import update, delete, select, insert


class ParentCategoryRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    async def insert_parent_category(self, parent_category):
        try:
            await self.db.execute(insert(ParentCategory).values(**parent_category))
            await self.db.commit()
        except Exception as e:
            print(f"Exception during parent category insertion: {e}")
            return False 
        return True
    
    async def update_parent_category(self, id: int, details: Dict[str, Any]):
        try:
            await self.db.execute(update(ParentCategory).where(ParentCategory.id == id).values(**details))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True
    
    async def delete_parent_category(self, id: int):
        try:
            await self.db.execute(delete(ParentCategory).where(ParentCategory.id == id))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True
    
    async def get_all_parent_categories(self):
        result = await self.db.execute(select(ParentCategory))
        return result.scalars().all()
    
    async def get_parent_category_by_id(self, id: int):
        result =  await self.db.execute(select(ParentCategory).where(ParentCategory.id == id))
        return result.scalars().one_or_none()