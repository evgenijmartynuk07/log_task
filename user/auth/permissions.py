from user.auth.manager import get_user_manager
from fastapi_users import FastAPIUsers
from user.models import DBUser
from user.auth.auth import auth_backend

fastapi_users = FastAPIUsers[DBUser, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
