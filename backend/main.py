from model.data.model import User
import uuid
from fastapi.middleware.cors import CORSMiddleware


from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from auth.manager import get_user_manager
from auth.auth import auth_backend
from auth.schemas import UserCreate, UserRead, UserUpdate

from api import product, category, review, blog, review_blog, sdek, address




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

app.include_router(product.router, prefix="/api/product", tags=["product"])
app.include_router(category.router, prefix="/api/category", tags=["category"])
app.include_router(review.router, prefix="/api/review", tags=["review"])
app.include_router(blog.router, prefix="/api/blog", tags=["blog"])
app.include_router(review_blog.router, prefix="/api/review_blog", tags=["review_blog"])
app.include_router(sdek.router, prefix="/api/sdek", tags=["sdek"])
app.include_router(address.router, prefix='/api/address', tags=['address'])

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)