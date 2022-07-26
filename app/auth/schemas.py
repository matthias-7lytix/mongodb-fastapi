import datetime

from enum import Enum
from beanie import PydanticObjectId
from fastapi_users import schemas
from pydantic import BaseModel, Field
from typing import List, Optional


class GroupType(Enum):
    COMPANY = "company"
    NGO = "ngo"
    EDU = "edu"
    GOV = "gov"
    OTHER = "other"


class UserGroup(BaseModel):
    group_name: str
    group_type: GroupType = GroupType.OTHER
    is_public: bool = False
    
    class Config:
        use_enum_values = True


class UserGroupMember(BaseModel):
    group: UserGroup
    is_admin: bool = False


class Participant(BaseModel):
    experiment_name: str
    is_owner: bool = False


class UserRead(schemas.BaseUser[PydanticObjectId]):
    public_key: str
    registered_on: datetime.datetime
    groups: List[UserGroupMember]
    experiments: List[Participant]


class UserCreate(schemas.BaseUserCreate):
    public_key: str
    registered_on: datetime.datetime = Field(default_factory=datetime.datetime.now)  # noqa: E501
    groups: List[UserGroupMember] = []
    experiments: List[Participant] = []


class UserUpdate(schemas.BaseUserUpdate):
    public_key: Optional[str]
    groups: Optional[List[UserGroupMember]]
    experiments: Optional[List[Participant]]