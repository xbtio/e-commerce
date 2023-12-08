from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from auth.manager import get_user_manager
from auth.auth import auth_backend
from model.data.model import User
from fastapi_users import FastAPIUsers

from sqlalchemy import select 

from db_config.session import get_async_session
from model.data.model import User

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_superuser = fastapi_users.current_user(active=True, superuser=True)


router = APIRouter()

@router.get('/get_all_users', dependencies=[Depends(current_superuser)])
async def get_all_users(db: AsyncSession = Depends(get_async_session)):
    stmt = select(User)
    result = await db.execute(stmt)
    users = result.scalars().all()
    if users is None:
        return JSONResponse(status_code=404, content={"message": "Users not found"})
    return users