from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from db_config.session import get_async_session
from model.request.product import ProductSchema
from fastapi_users import FastAPIUsers
from model.data.product import Product
from model.data.model import User
from auth.manager import get_user_manager
from auth.auth import auth_backend
from service.review import ReviewService
from model.request.review import ReviewCreate


fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_user = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)


router = APIRouter()

@router.get("/")
async def get_all_reviews(db: AsyncSession = Depends(get_async_session)):
    review_service = ReviewService(db)
    result = await review_service.get_all_reviews()
    return result

@router.post("/")
async def create_review(product_id: int, review: ReviewCreate, db: AsyncSession = Depends(get_async_session), current_user: User = Depends(current_user)):
    review_service = ReviewService(db)
    result = await review_service.create_review(product_id, current_user, review)
    if result:
        return JSONResponse({"message": "review created successfully"})
    return JSONResponse({"message": "review creation failed"})

@router.put("/{id}", dependencies=[Depends(current_user)])
async def update_review(id: int, review: ReviewCreate, db: AsyncSession = Depends(get_async_session)):
    review_service = ReviewService(db)
    result = await review_service.update_review(id,  review)
    if result:
        return JSONResponse({"message": "review updated successfully"})
    return JSONResponse({"message": "review update failed"})

@router.delete("/{id}", dependencies=[Depends(current_user)])
async def delete_review(id: int, db: AsyncSession = Depends(get_async_session)):
    review_service = ReviewService(db)
    result = await review_service.delete_review(id)
    if result:
        return JSONResponse({"message": "review deleted successfully"})
    return JSONResponse({"message": "review deletion failed"})

@router.get("/{product_id}")
async def get_review_by_product_id(product_id: int, db: AsyncSession = Depends(get_async_session)):
    review_service = ReviewService(db)
    result = await review_service.get_review_by_product_id(product_id)
    return result