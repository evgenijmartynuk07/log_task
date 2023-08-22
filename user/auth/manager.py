from typing import Optional

from config import SECRET
from fastapi import Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase

from db.engine import get_async_session
from user.models import DBUser


async def get_user_db(
        session: AsyncSession = Depends(get_async_session)
) -> SQLAlchemyUserDatabase:

    yield SQLAlchemyUserDatabase(session, DBUser)


class UserManager(IntegerIDMixin, BaseUserManager[DBUser, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(
            self,
            user: DBUser,
            request: Optional[Request] = None
    ) -> None:

        print(f"User {user.id} has registered.")

    async def on_after_login(
        self,
        user: DBUser,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ):
        print(f"User {user.id} logged in.")


async def get_user_manager(user_db=Depends(get_user_db)) -> UserManager:
    yield UserManager(user_db)
