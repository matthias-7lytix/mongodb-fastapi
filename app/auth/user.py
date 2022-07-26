from http.client import HTTPException
import redis.asyncio
import re

from typing import Optional, Union
from beanie import PydanticObjectId
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, \
    CookieTransport, RedisStrategy
from fastapi_users.db import BeanieUserDatabase, ObjectIDIDMixin
from fastapi_users import schemas, models
from fastapi_users.exceptions import InvalidPasswordException

from app.settings import settings

from .schemas import UserCreate
from .db import User, get_user_db

SECRET = "SECRET"


class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(
        self,
        user: User,
        request: Optional[Request] = None
    ):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. "
              f"Reset token: {token}")

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. "
              f"Verification token: {token}")
        
    async def validate_password(
        self,
        password: str,
        user: Union[schemas.UC, models.UP]
    ) -> None:
        char_classes = [re.compile("[A-Z]"),
                        re.compile("[a-z]"),
                        re.compile("[0-9]")]

        if len(password) < 8:
            raise InvalidPasswordException("VERIFY_PASSWORD_INVALID_SHORT")
        
        elif any(rgx.search(password) is None for rgx in char_classes):
            raise InvalidPasswordException("VERIFY_PASSWORD_INVALID_CHARS")

        return await super().validate_password(password, user)
    
    async def create(self,
                     user_create: UserCreate,
                     safe: bool = False,
                     request: Optional[Request] = None) -> models.UP:
        for user_group in user_create.groups:
            group_name = user_group.group.group_name
            if (group := await User.find_group_by_name(group_name)) is None:
                user_group.is_admin = True

            elif (group.group_type == user_group.group.group_type
                  and group.is_public == user_group.group.is_public):
                user_group.is_admin = False

            else:
                raise HTTPException(
                    status_code=409,
                    detail=(f"{'Public g' if group.is_public else 'G'}roup"
                            f"{group.group_name} alread exists "
                            f"with type '{group.group_type}'.")
                    )

        return await super().create(user_create, safe, request)


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

cookie_transport = CookieTransport(cookie_max_age=3600)

redis = redis.asyncio.from_url(settings.redis_url, decode_responses=True)

def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(redis, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_redis_strategy,
)

fastapi_users = FastAPIUsers[User, PydanticObjectId](
    get_user_manager,
    [auth_backend]
)

current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
