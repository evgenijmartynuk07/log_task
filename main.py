from fastapi import FastAPI

from log.auth.permissions import fastapi_users
from log.routers import logs
from log.auth.auth import auth_backend
from log.schemas import UserRead, UserCreate

app = FastAPI()


app.include_router(logs.router)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
