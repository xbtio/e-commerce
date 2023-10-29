from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db_config.session import get_async_session
from model.request.blog import BlogSchema, BlogCreate
from fastapi_users import FastAPIUsers
from model.data.model import User
from auth.manager import get_user_manager
from auth.auth import auth_backend
from service.blog import BlogService

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_superuser = fastapi_users.current_user(active=True, superuser=True)
current_user = fastapi_users.current_user(active=True, verified=True)

router = APIRouter()

@router.post("/")
async def create_blog(blog: BlogCreate, current_userr: User = Depends(current_superuser),db: AsyncSession = Depends(get_async_session)):
    blog_service = BlogService(db)
    content_dict = blog.model_dump()
    content_dict['user_id'] = current_userr.id
    result = await blog_service.create_blog(content_dict)
    if result:
        return JSONResponse({"message": "blog created successfully"})
    return JSONResponse({"message": "blog creation failed"})

@router.put("/{id}")
async def update_blog(id: int, blog: BlogCreate, current_userr: User = Depends(current_superuser), db: AsyncSession = Depends(get_async_session)):
    blog_service = BlogService(db)
    content = blog.model_dump()
    result = await blog_service.update_blog(id, content)
    if result:
        return JSONResponse({"message": "blog updated successfully"})
    return JSONResponse({"message": "blog update failed"})

@router.delete("/{id}", dependencies=[Depends(current_superuser)])
async def delete_blog(id: int, db: AsyncSession = Depends(get_async_session)):
    blog_service = BlogService(db)
    result = await blog_service.delete_blog(id)
    return result

@router.get("/")
async def get_all_blogs(db: AsyncSession = Depends(get_async_session)):
    blog_service = BlogService(db)
    result = await blog_service.get_all_blogs()
    return result

@router.get("/{id}")
async def get_blog_by_id(id: int, db: AsyncSession = Depends(get_async_session)):
    blog_service = BlogService(db)
    result = await blog_service.get_blog_by_id(id)
    return result

