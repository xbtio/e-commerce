from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db_config.session import get_async_session
from model.request.blog import ReviewBlogSchema, ReviewBlogCreate
from fastapi_users import FastAPIUsers
from model.data.model import User
from auth.manager import get_user_manager
from auth.auth import auth_backend
from service.blog import ReviewBlogService

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_superuser = fastapi_users.current_user(active=True, superuser=True)
current_user = fastapi_users.current_user(active=True, verified=True)

router = APIRouter()

@router.post("/")
async def create_review(blog: ReviewBlogCreate, current_userr: User = Depends(current_user),db: AsyncSession = Depends(get_async_session)):
    review_blog_service = ReviewBlogService(db)
    content_dict = blog.model_dump()
    content_dict['user_id'] = current_userr.id
    content_dict['name_of_user'] = current_userr.name
    result = await review_blog_service.create_review(content_dict)
    if result:
        return JSONResponse({"message": "review for blog created successfully"})
    return JSONResponse({"message": "review for blog creation failed"})

@router.put("/{id}")
async def update_review(id: int, blog: ReviewBlogCreate, current_userr: User = Depends(current_user),db: AsyncSession = Depends(get_async_session)):
    review_blog_service = ReviewBlogService(db)
    content = blog.model_dump()
    content['user_id'] = current_userr.id
    result = await review_blog_service.update_review(id, content)
    if result:
        return JSONResponse({"message": "review for blog updated successfully"})
    return JSONResponse({"message": "review for blog update failed"})

@router.delete("/{id}", dependencies=[Depends(current_user)])
async def delete_review(id: int, db: AsyncSession = Depends(get_async_session)):
    review_blog_service = ReviewBlogService(db)
    result = await review_blog_service.delete_review(id)
    return result

@router.get("/", dependencies=[Depends(current_superuser)])
async def get_all_reviews(blog_id: int, db: AsyncSession = Depends(get_async_session)):
    review_blog_service = ReviewBlogService(db)
    result = await review_blog_service.get_all_reviews_of_blog(blog_id)
    return result

@router.get("/{blog_id}")
async def get_all_reviews_of_blog(blog_id: int, db: AsyncSession = Depends(get_async_session)):
    review_blog_service = ReviewBlogService(db)
    result = await review_blog_service.get_all_reviews_of_blog(blog_id)
    return result