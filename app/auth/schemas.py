from enum import Enum
from beanie import PydanticObjectId
from fastapi_users import schemas
from pydantic import BaseModel
from typing import List, Optional


class GroupType(Enum):
    COMPANY = "company"
    NGO = "ngo"
    EDU = "edu"
    GOV = "gov"
    PUBLIC = "public"
    PRIVATE = "private"
    OTHER = "other"


class UserGroup(BaseModel):
    group_name: str
    group_type: GroupType = GroupType.PRIVATE
    
    class Config:
        use_enum_values = True


class UserGroupMember(BaseModel):
    group: UserGroup
    is_admin: bool = False


class Participant(BaseModel):
    experiment_name: str
    is_owner: bool = False


class UserRead(schemas.BaseUser[PydanticObjectId]):
    groups: List[UserGroupMember]
    experiments: List[Participant]


class UserCreate(schemas.BaseUserCreate):
    groups: List[UserGroupMember]
    experiments: List[Participant]


class UserUpdate(schemas.BaseUserUpdate):
    groups: Optional[List[UserGroupMember]]
    experiments: Optional[List[Participant]]