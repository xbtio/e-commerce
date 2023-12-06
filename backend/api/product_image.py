from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db_config.session import get_async_session
from model.request.product_image import ProductImageCreateSchema, ProductImageUpdateSchema
from fastapi_users import FastAPIUsers
from model.data.model import User
from auth.manager import get_user_manager
from auth.auth import auth_backend
from typing import List
from repository.product_image import ProductImageRepo

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_superuser = fastapi_users.current_user(active=True, superuser=True)


router = APIRouter()

@router.get('/', dependencies=[Depends(current_superuser)])
async def get_all_product_images(db: AsyncSession = Depends(get_async_session)):
    product_image_repo = ProductImageRepo(db)
    result = await product_image_repo.get_all_product_images()
    return result

@router.delete('/{id}', dependencies=[Depends(current_superuser)])
async def delete_product_image(id: int, db: AsyncSession = Depends(get_async_session)):
    product_image_repo = ProductImageRepo(db)
    result = await product_image_repo.delete_product_image(id)
    if result:
        return JSONResponse({"message": "product image deleted successfully"}, status_code=200)
    return JSONResponse({"message": "product image deletion failed"}, status_code=400)

@router.put('/{id}', dependencies=[Depends(current_superuser)])
async def update_product_image(id: int, product_image: ProductImageUpdateSchema, db: AsyncSession = Depends(get_async_session)):
    product_image_repo = ProductImageRepo(db)
    content = product_image.model_dump()
    result = await product_image_repo.update_product_image(id, content)
    if result:
        return JSONResponse({"message": "product image updated successfully"}, status_code=200)
    return JSONResponse({"message": "product image update failed"}, status_code=400)
