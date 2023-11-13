from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db_config.session import get_async_session
from repository.product_description import ProductDescriptionRepo
from service.product_description import ProductDescriptionService
from model.request.product_description import ProductDescriptionCreateSchema, ProductDescriptionUpdateSchema
from fastapi_users import FastAPIUsers
from model.data.model import User
from auth.manager import get_user_manager
from auth.auth import auth_backend
from typing import List

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_superuser = fastapi_users.current_user(active=True, superuser=True)

router = APIRouter()

@router.post("/create", dependencies=[Depends(current_superuser)])
async def create_product_description(product_description: ProductDescriptionCreateSchema, db: AsyncSession = Depends(get_async_session)):
    product_description_repo = ProductDescriptionRepo(db)
    content_dict = product_description.model_dump()
    result = await product_description_repo.insert_product_description(content_dict)
    if result:
        return JSONResponse({"message": "product description created successfully"})
    return JSONResponse({"message": "product description creation failed"})

@router.put("/update", dependencies=[Depends(current_superuser)])
async def update_product_description(product_description: List[ProductDescriptionUpdateSchema], db: AsyncSession = Depends(get_async_session)):
    product_description_service = ProductDescriptionService(db)
    content = [i.model_dump() for i in product_description]
    result = await product_description_service.update_product_description(content)
    if result:
        return JSONResponse({"message": "product description updated successfully"})
    return JSONResponse({"message": "product description update failed"})

@router.delete("/delete/{id}", dependencies=[Depends(current_superuser)])
async def delete_product_description(id: int, db: AsyncSession = Depends(get_async_session)):
    product_description_repo = ProductDescriptionRepo(db)
    result = await product_description_repo.delete_product_description(id)
    return result

@router.get("/get/{id}")
async def get_product_description_by_product_id(id: int, db: AsyncSession = Depends(get_async_session)):
    product_description_repo = ProductDescriptionRepo(db)
    result = await product_description_repo.get_product_description_by_product_id(id)
    return result