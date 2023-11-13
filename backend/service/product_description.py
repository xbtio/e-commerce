from model.data.product import Category
from sqlalchemy.ext.asyncio import AsyncSession
from repository.product_description import ProductDescriptionRepo
from typing import Dict, Any, List

class ProductDescriptionService:
    def __init__(self, db: AsyncSession):
        self.repo = ProductDescriptionRepo(db)

    
    async def update_product_description(self, list: List[Dict[str, Any]]):
        try:
            for i in list:
                await self.repo.update_product_description(i['id'], i)
        except Exception as e:
            print(e)
            return False
        return True
