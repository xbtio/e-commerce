from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db_config.session import get_async_session
from model.request.cart import ShoppingCartItemCreateSchema
from fastapi_users import FastAPIUsers
from model.data.model import User
from auth.manager import get_user_manager
from auth.auth import auth_backend
from service.cart import ShoppingCartItemService, ShoppingCartService

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_superuser = fastapi_users.current_user(active=True, superuser=True)
current_user = fastapi_users.current_user(active=True, verified=True)

router = APIRouter()

@router.post("/")
async def create_cart_item(cart_item: ShoppingCartItemCreateSchema, current_user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    cart_item_service = ShoppingCartItemService(db)
    content_dict = cart_item.model_dump()
    result = await cart_item_service.create_cart_item(content_dict, current_user.id)
    if result:
        return JSONResponse({"message": "cart item created successfully"})
    return JSONResponse({"message": "cart item creation failed"})


@router.delete("/{id}")
async def delete_cart_item(id: int, db: AsyncSession = Depends(get_async_session)):
    cart_item_service = ShoppingCartItemService(db)
    result = await cart_item_service.delete_cart_item(id)
    return result

@router.get("/")
async def get_cart_info_by_user_id(current_user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    cart_item_service = ShoppingCartService(db)
    result = await cart_item_service.get_cart_info_by_user_id(current_user.id)
    return result