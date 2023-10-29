
from model.data.product import Category
from sqlalchemy.ext.asyncio import AsyncSession
from repository.category import CategoryRepo


from fastapi import HTTPException, status


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_category(self, category):
        try:
            category_repo = CategoryRepo(self.db)
            await category_repo.insert_category(category)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return True
    
    async def update_category(self, id: int, category):
        try:
            category_repo = CategoryRepo(self.db)
            category = await category_repo.update_category(id, category)
            if category is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return True
    
    async def delete_category(self, id: int):
        try:
            category_repo = CategoryRepo(self.db)
            category = await category_repo.delete_category(id)
            if category is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return True
    
    async def get_all_categories(self):
        try:
            category_repo = CategoryRepo(self.db)
            result = await category_repo.get_all_categories()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return result
