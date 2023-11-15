from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from model.data.address import Address
from sqlalchemy import update, delete, select, insert


class AddressRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def insert_address(self, address: Dict):
        try:
            await self.db.execute(insert(Address).values(**address))
            await self.db.commit()
        except Exception as e:
            print(f"Exception during address insertion: {e}")
            return False
        return True
    
    async def update_address(self, user_id: int, details: Dict[str, Any]):
        try:
            await self.db.execute(update(Address).where(Address.user_id == user_id).values(**details))
            await self.db.commit()
        except Exception as e:
            print(e)
            return False
        return True
    
    async def delete_address(self, id: int):
        try:
            await self.db.execute(delete(Address).where(Address.user_id == id))
            await self.db.commit()
        except Exception as e:
            print(e)
            return False
        return True
    
    async def get_address_by_user_id(self, user_id: int):
        result = await self.db.execute(select(Address).where(Address.user_id == user_id))
        return result.scalars().one_or_none()
    
    async def get_all_address(self):
        result = await self.db.execute(select(Address))
        return result.scalars().all()

