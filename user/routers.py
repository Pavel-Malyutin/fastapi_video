from  fastapi import APIRouter
from fastapi_users import FastAPIUsers

from user.api import on_after_register
from user.models import user_db
from user.schema import User, UserDB, UserUpdate, UserCreate
from user.auth import auth_backends, jwt_authentication


user_router = APIRouter()


fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB
)

user_router.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix='/auth/jwt', tags=['auth']
)

user_router.include_router(
    fastapi_users.get_register_router(on_after_register), prefix='/auth', tags=['auth']
)

user_router.include_router(fastapi_users.get_users_router(), prefix='/users', tags=['users'])
