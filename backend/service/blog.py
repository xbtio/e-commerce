from sqlalchemy.ext.asyncio import AsyncSession
from model.data.blog import Blog, ReviewBlog
from repository.blog import BlogRepo, ReviewBlogRepo
from fastapi import HTTPException, status
import datetime


def get_date_now():
    return datetime.datetime.now()


class BlogService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_blog(self, blog):
        try:
            blog_repo = BlogRepo(self.db)
            blog['published'] = get_date_now()
            await blog_repo.insert_blog(blog)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return True
    
    async def update_blog(self, id: int, blog):
        try:
            blog_repo = BlogRepo(self.db)
            blog = await blog_repo.update_blog(id, blog)
            if blog is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return True
    
    async def delete_blog(self, id: int):
        try:
            blog_repo = BlogRepo(self.db)
            blog = await blog_repo.delete_blog(id)
            if blog is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return True
    
    async def get_all_blogs(self):
        try:
            blog_repo = BlogRepo(self.db)
            result = await blog_repo.get_all_blogs()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return result
    
    async def get_blog_by_id(self, id: int):
        try:
            blog_repo = BlogRepo(self.db)
            result = await blog_repo.get_blog_by_id(id)
            if result is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return result

class ReviewBlogService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_review(self, review):
        try:
            review_blog_repo = ReviewBlogRepo(self.db)
            review['date'] = get_date_now()
            await review_blog_repo.insert_review(review)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return True
    
    async def update_review(self, id: int, review):
        try:
            review_blog_repo = ReviewBlogRepo(self.db)
            review = await review_blog_repo.update_review(id, review)
            if review is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return True

    async def delete_review(self, id: int):
        try:
            review_blog_repo = ReviewBlogRepo(self.db)
            review = await review_blog_repo.delete_review(id)
            if review is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return True
    
    async def get_all_reviews_of_blog(self, blog_id: int):
        try:
            review_blog_repo = ReviewBlogRepo(self.db)
            result = await review_blog_repo.get_reviews_by_blog_id(blog_id)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return result