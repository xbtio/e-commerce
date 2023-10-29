from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db_config.session import get_async_session
from fastapi_users import FastAPIUsers
from model.data.model import User
from auth.manager import get_user_manager
from auth.auth import auth_backend

from service.category import CategoryService
from model.request.category import CategorySchema


fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_superuser = fastapi_users.current_user(active=True, superuser=True)


router = APIRouter()

@router.post("/", dependencies=[Depends(current_superuser)])
async def create_category(category: CategorySchema, db: AsyncSession = Depends(get_async_session)):
    category_service = CategoryService(db)
    content_dict = category.model_dump()
    result = await category_service.create_category(content_dict)
    if result:
        return JSONResponse({"message": "category created successfully"})
    return JSONResponse({"message": "category creation failed"})

@router.put("/{id}", dependencies=[Depends(current_superuser)])
async def update_category(id: int, category: CategorySchema, db: AsyncSession = Depends(get_async_session)):
    category_service = CategoryService(db)
    content = category.model_dump()
    result = await category_service.update_category(id, content)
    if result:
        return JSONResponse({"message": "category updated successfully"})
    return JSONResponse({"message": "category update failed"})

@router.delete("/{id}", dependencies=[Depends(current_superuser)])
async def delete_category(id: int, db: AsyncSession = Depends(get_async_session)):
    category_service = CategoryService(db)
    result = await category_service.delete_category(id)
    return result

@router.get("/")
async def get_all_categories(db: AsyncSession = Depends(get_async_session)):
    category_service = CategoryService(db)
    result = await category_service.get_all_categories()
    return result
