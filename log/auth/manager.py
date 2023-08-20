from typing import Optional
from config import SECRET
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase

from log.db.engine import get_async_session
from log.db.models import DBUser


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, DBUser)


class UserManager(IntegerIDMixin, BaseUserManager[DBUser, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: DBUser, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
