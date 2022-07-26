import datetime

from typing import List, Optional
from beanie import PydanticObjectId
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase
from pydantic import Field

from .schemas import UserGroupMember, Participant, UserGroup


class User(BeanieBaseUser[PydanticObjectId]):
    public_key: str
    registered_on: datetime.datetime = Field(default_factory=datetime.datetime.now)  # noqa: E501
    groups: List[UserGroupMember] = []
    experiments: List[Participant] = []
    
    @classmethod
    async def find_group_by_name(cls, group_name: str) -> Optional[UserGroup]:
        result = None
        async for user in cls.find_all():
            try:
                result = next(member.group for member in user.groups
                              if member.group.group_name == group_name)
            except StopIteration:
                pass
        
        return result


async def get_user_db():
    yield BeanieUserDatabase(User)
