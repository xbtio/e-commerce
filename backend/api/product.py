from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db_config.session import get_async_session
from repository.product import ProductRepo
from model.request.product import ProductUpdateSchema, ProductCreateSchema
from model.request.product_description import ProductDescriptionCreateSchema, ProductDescriptionUpdateSchema
from model.request.product_image import ProductImageCreateSchema, ProductImageUpdateSchema
from fastapi_users import FastAPIUsers
from model.data.model import User
from auth.manager import get_user_manager
from auth.auth import auth_backend
from typing import List

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_superuser = fastapi_users.current_user(active=True, superuser=True)


router = APIRouter()


@router.post("/", dependencies=[Depends(current_superuser)])
async def create_product(product: ProductCreateSchema, product_description: List[ProductDescriptionCreateSchema], product_image: List[ProductImageCreateSchema], db: AsyncSession = Depends(get_async_session)):
    product_repo = ProductRepo(db)
    content_dict = product.model_dump()
    product_description_content = [i.model_dump() for i in product_description]
    product_images = [i.model_dump() for i in product_image]
    result = await product_repo.insert_product(content_dict, product_description_content, product_images)
    if result:
        return JSONResponse({"message": "product created successfully"})
    return JSONResponse({"message": "product creation failed"})

@router.put("/{id}", dependencies=[Depends(current_superuser)])
async def update_product(id: int, product: ProductUpdateSchema,db: AsyncSession = Depends(get_async_session)):
    product_repo = ProductRepo(db)
    content = product.model_dump()
    result = await product_repo.update_product(id, content)
    if result:  
        return JSONResponse({"message": "product updated successfully"})
    return JSONResponse({"message": "product update failed"})

@router.delete("/{id}", dependencies=[Depends(current_superuser)])
async def delete_product(id: int, db: AsyncSession = Depends(get_async_session)):
    product_repo = ProductRepo(db)
    result = await product_repo.delete_product(id)
    return result

@router.get("/")
async def get_all_products(db: AsyncSession = Depends(get_async_session)):
    product_repo = ProductRepo(db)
    result = await product_repo.get_all_products()
    return result

@router.get("/{id}")
async def get_product_by_id(id: int, db: AsyncSession = Depends(get_async_session)):
    product_repo = ProductRepo(db)
    result = await product_repo.get_product_by_id(id)
    return result