from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from model.data.product import Product
from sqlalchemy import update, delete, select, insert
from model.data.blog import Blog, ReviewBlog

class BlogRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    async def insert_blog(self, blog: Dict):
        try:
            await self.db.execute(insert(Blog).values(**blog))  
            await self.db.commit()
        except Exception as e:
            print(f"Exception during blog insertion: {e}")
            return False 
        return True

    async def update_blog(self, id: int, details: Dict[str, Any]):
        try:
            await self.db.execute(update(Blog).where(Blog.id == id).values(**details))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True

    async def delete_blog(self, id: int):
        try:
            await self.db.execute(delete(Blog).where(Blog.id == id))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True

    async def get_all_blogs(self):
        result = await self.db.execute(select(Blog))
        return result.scalars().all()
    
    async def get_blog_by_id(self, id: int):
        result =  await self.db.execute(select(Blog).where(Blog.id == id))
        return result.scalars().one_or_none()
    
class ReviewBlogRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    async def insert_review(self, review: Dict):
        try:
            await self.db.execute(insert(ReviewBlog).values(**review))  
            await self.db.commit()
        except Exception as e:
            print(f"Exception during review insertion: {e}")
            return False 
        return True

    async def update_review(self, id: int, details: Dict[str, Any]):
        try:
            await self.db.execute(update(ReviewBlog).where(ReviewBlog.id == id).values(**details))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True

    async def delete_review(self, id: int):
        try:
            await self.db.execute(delete(ReviewBlog).where(ReviewBlog.id == id))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True

    async def get_review_by_id(self, id: int):
        result =  await self.db.execute(select(ReviewBlog).where(ReviewBlog.id == id))
        return result.scalars().one_or_none()

    async def get_reviews_by_blog_id(self, blog_id: int):
        result = await self.db.execute(select(ReviewBlog).where(ReviewBlog.blog_id == blog_id))
        return result.scalars().all()