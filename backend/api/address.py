from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db_config.session import get_async_session
from model.request.address import AddressCreate, AddressUpdate
from fastapi_users import FastAPIUsers
from model.data.model import User
from auth.manager import get_user_manager
from auth.auth import auth_backend
from service.address import AddressService

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_user = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

router = APIRouter()

@router.post('/')
async def create_address(address: AddressCreate, user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    address_service = AddressService(db)
    model_json = address.model_dump()
    model_json['user_id'] = user.id
    result = await address_service.create_address(model_json)
    if result:
        return JSONResponse({"message": "address created successfully"})
    return JSONResponse({"message": "address creation failed"})

@router.put('/')
async def update_address(address: AddressUpdate, user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    address_service = AddressService(db)
    result = await address_service.update_address(user.id, address.model_dump())
    if result:
        return JSONResponse({"message": "address updated successfully"})
    return JSONResponse({"message": "address update failed"})

@router.delete('/')
async def delete_address(user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    address_service = AddressService(db)
    result = await address_service.delete_address(user.id)
    if result:
        return JSONResponse({"message": "address deleted successfully"})
    return JSONResponse({"message": "address delete failed"})

@router.get('/me')
async def get_by_user_id(user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    address_service = AddressService(db)
    result = await address_service.get_address_by_user_id(user.id)
    return result

@router.get('/', dependencies=[Depends(current_superuser)])
async def get_all_address(db: AsyncSession = Depends(get_async_session)):
    address_service = AddressService(db)
    result = await address_service.get_all_address()
    return result
