from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from model.data.order import Order
from sqlalchemy import update, delete, select, insert


class OrderRepo:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    async def insert_order(self, order: Dict):
        try:
            await self.db.execute(insert(Order).values(**order))  
            await self.db.commit()
        except Exception as e:
            print(f"Exception during order insertion: {e}")
            return False 
        return True

    async def get_order_by_user_id(self, user_id: int):
        result = await self.db.execute(select(Order).where(Order.user_id == user_id))
        return result.scalars().one_or_none()