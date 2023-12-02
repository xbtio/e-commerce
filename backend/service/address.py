from sqlalchemy.ext.asyncio import AsyncSession
from country.country import get_country_info
from fastapi import HTTPException, status
from repository.address import AddressRepo
from model.data.address import Address



class AddressService:
    def __init__(self, db: AsyncSession) -> None:
        self.repo = AddressRepo(db)
    
    async def create_address(self, blog):
        code = await get_country_info(blog['country'])
        blog['code'] = code
        return await self.repo.insert_address(blog)

    async def update_address(self, id: int, blog):
        return await self.repo.update_address(id, blog)
    
    async def delete_address(self, id: int):
        return await self.repo.delete_address(id)
    
    async def get_address_by_user_id(self, id: int) -> Address:
        result = await self.repo.get_address_by_user_id(id)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
        return result

    async def get_address_by_id(self, id: int) -> Address:
        result = await self.repo.get_address_by_id(id)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
        return result
    
    async def get_all_address(self):
        return await self.repo.get_all_address()