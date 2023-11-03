from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sdek.sdek import SdekService
from repository.order import OrderRepo

from auth.manager import get_user_manager
from auth.auth import auth_backend
from model.data.model import User
from fastapi_users import FastAPIUsers

from db_config.session import get_async_session
from service.address import AddressService

from sdek.schema import Phone

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_user = fastapi_users.current_user(active=True, verified=True)

router = APIRouter()

@router.get("/callback")
async def callback(sdek_id: int):
    sdek_service = SdekService()
    result = await sdek_service.get_status_about_order(sdek_id)
    if result is not None:
        return JSONResponse({"message": "order info received successfully", "data": result})
    return JSONResponse({"message": "order info receiving failed"})


@router.post("/order")
async def create_order(name_of_recepient: str, phone_of_recepient: Phone, comment: str,user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    sdek_service = SdekService()
    address_service = AddressService(db)
    order_repo = OrderRepo(db)
    address_of_user = await address_service.get_address_by_user_id(user.id)
    result = await sdek_service.create_order(name_of_recepient=name_of_recepient, email=user.email, phone_of_recepient=phone_of_recepient, address_of_recepient=address_of_user, comment=comment)
    if result is not None:
        await order_repo.insert_order({'user_id': user.id, 'sdek_order_uuid': result['entity']['uuid']})
        return JSONResponse({"message": "order created successfully", "data": result})
    return JSONResponse({"message": "order creation failed"})

@router.post("/order/refusal")
async def create_order_refusal(user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    sdek_service = SdekService()
    order_repo = OrderRepo(db)
    order_of_user = await order_repo.get_order_by_user_id(user.id)
    if order_of_user is not None:
        result = await sdek_service.refuse_order(order_of_user.sdek_order_uuid)
        if result is not None:
            return JSONResponse({"message": "order refused successfully", "data": result})
        return JSONResponse({"message": "order refusing failed"})
    return JSONResponse({"message": "order refusing failed"})
    