from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db_config.session import get_async_session
from fastapi_users import FastAPIUsers
from model.data.model import User
from auth.manager import get_user_manager
from auth.auth import auth_backend

from repository.parent_category import ParentCategoryRepo
from model.request.category import ParentCategorySchema


fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_superuser = fastapi_users.current_user(active=True, superuser=True)


router = APIRouter()

@router.post("/", dependencies=[Depends(current_superuser)])
async def create_category(category: ParentCategorySchema, db: AsyncSession = Depends(get_async_session)):
    category_repo = ParentCategoryRepo(db)
    content_dict = category.model_dump()
    result = await category_repo.insert_parent_category(content_dict)
    if result:
        return JSONResponse({"message": "category created successfully"})
    return JSONResponse({"message": "category creation failed"})

@router.put("/{id}", dependencies=[Depends(current_superuser)])
async def update_category(id: int, category: ParentCategorySchema, db: AsyncSession = Depends(get_async_session)):
    category_repo = ParentCategoryRepo(db)
    content = category.model_dump()
    result = await category_repo.update_parent_category(id, content)
    if result:
        return JSONResponse({"message": "category updated successfully"})
    return JSONResponse({"message": "category update failed"})

@router.delete("/{id}", dependencies=[Depends(current_superuser)])
async def delete_category(id: int, db: AsyncSession = Depends(get_async_session)):
    category_repo = ParentCategoryRepo(db)
    result = await category_repo.delete_parent_category(id)
    return result

@router.get("/")
async def get_all_categories(db: AsyncSession = Depends(get_async_session)):
    category_repo = ParentCategoryRepo(db)
    result = await category_repo.get_all_parent_categories()
    return result

@router.get("/{id}")
async def get_category_by_id(id: int, db: AsyncSession = Depends(get_async_session)):
    category_repo = ParentCategoryRepo(db)
    result = await category_repo.get_parent_category_by_id(id)
    return result

