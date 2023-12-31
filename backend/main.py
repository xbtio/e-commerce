from model.data.model import User
from redis import asyncio as aioredis
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from auth.manager import get_user_manager
from auth.auth import auth_backend
from auth.schemas import UserCreate, UserRead, UserUpdate

from api import product, category, review, blog, review_blog, sdek, address, product_description, cart, parent_category, product_image, users
from config import REDIS_HOST, REDIS_PORT



fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/api/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/api/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    users.router,
    prefix="/user",
    tags=["user"],
)

app.include_router(product.router, prefix="/api/product", tags=["product"])
app.include_router(cart.router, prefix="/api/cart", tags=["cart"])
app.include_router(category.router, prefix="/api/category", tags=["category"])
app.include_router(parent_category.router, prefix="/api/parent_category", tags=["parent_category"])
app.include_router(review.router, prefix="/api/review", tags=["review"])
app.include_router(blog.router, prefix="/api/blog", tags=["blog"])
app.include_router(review_blog.router, prefix="/api/review_blog", tags=["review_blog"])
app.include_router(sdek.router, prefix="/api/sdek", tags=["sdek"])
app.include_router(address.router, prefix='/api/address', tags=['address'])
app.include_router(product_description.router, prefix='/api/product_description', tags=['product_description'])
app.include_router(product_image.router, prefix='/api/product_image', tags=['product_image'])

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")