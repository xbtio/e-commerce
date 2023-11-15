from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from model.data.sdek_order import OrderRequest
from sqlalchemy import update, delete, select, insert


class OrderRequestRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def insert_order_request(self, order_request: Dict):
        try:
            order_request_insert_stmt = insert(OrderRequest).values(**order_request).returning(OrderRequest.id)
            result = await self.db.execute(order_request_insert_stmt)
            await self.db.flush()
            order_id = result.fetchone()
            await self.db.commit()
            return order_id[0] if order_id else None
            
        except Exception as e:
            print(f"Exception during order request insertion: {type(e).__name__}, {str(e)}")
            # Consider rolling back the transaction if there's an error
            await self.db.rollback()
            return False
       
    
    async def update_order_request(self, id: int, details: Dict[str, Any]):
        try:
            await self.db.execute(update(OrderRequest).where(OrderRequest.id == id).values(**details))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True
    
    async def delete_order_request(self, id: int):
        try:
            await self.db.execute(delete(OrderRequest).where(OrderRequest.id == id))
            await self.db.commit()

        except Exception as e:
            print(e)
            return False
        return True
    
    async def get_order_request_by_id(self, id: int):
        result = await self.db.execute(select(OrderRequest).where(OrderRequest.id == id))
        return result.scalars().one_or_none()
    
    async def get_all_order_requests(self):
        result = await self.db.execute(select(OrderRequest))
        return result.scalars().all()