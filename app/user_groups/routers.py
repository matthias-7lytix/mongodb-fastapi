from fastapi import APIRouter, Depends
from typing import List

from app.auth import current_active_user, User, Participant

router = APIRouter()


@router.get("/memberships",
            response_description="Get all memberships of current user.",
            response_model=List[Participant])
async def get_memberships(user: User = Depends(current_active_user)):
    return user.groups
