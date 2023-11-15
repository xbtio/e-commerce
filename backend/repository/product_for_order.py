from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from model.data.sdek_order import ProductForOrder
from sqlalchemy import update, delete, select, insert

class ProductForOrderRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def insert_product_for_order(self, product_for_order: Dict):
        try:
            await self.db.execute(insert(ProductForOrder).values(**product_for_order))  
            await self.db.commit()
        except Exception as e:
            print(f"Exception during product for order insertion: {e}")
            return False 
        return True
    
    async def update_product_for_order(self, id: int, details: Dict[str, Any]):
        try:
            await self.db.execute(update(ProductForOrder).where(ProductForOrder.id == id).values(**details))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True
    
    async def delete_product_for_order(self, id: int):
        try:
            await self.db.execute(delete(ProductForOrder).where(ProductForOrder.id == id))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True
    
    async def get_product_for_order_by_order_id(self, id: int):
        result =  await self.db.execute(select(ProductForOrder).where(ProductForOrder.order_request_id == id))
        return result.scalars().all()