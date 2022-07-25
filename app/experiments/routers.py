from gettext import dpgettext
from http.client import HTTPException
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Body
from typing import List

from app.auth import current_active_user, current_superuser, User, Participant

router = APIRouter()


@router.get("/experiments",
            response_description="Get all experiments for current user.",
            response_model=List[Participant])
async def get_my_experiments(user: User = Depends(current_active_user)):
    return user.experiments


@router.put("/experiments",
            response_description="Add an experiment to current user",
            response_model=List[Participant])
async def add_my_experiment(user: User = Depends(current_active_user),
                            participant: Participant = Body()):
    user.experiments.append(participant)
    await user.save()
    return user.experiments


@router.get("/users/{id_}/experiments",
            response_description="Get all experiments for user.",
            response_model=List[Participant])
async def get_user_experiments(id_: PydanticObjectId,
                               user: User = Depends(current_superuser)):
    other_user = await User.get(id_)
    
    if other_user is None:
        raise HTTPException(status_code=404, detail=f"User {id_} not found.")
    else:
        return other_user.experiments


@router.put("/users/{id_}/experiments",
            response_description="Add an experiment to user",
            response_model=List[Participant])
async def add_user_experiments(id_: PydanticObjectId,
                               user: User = Depends(current_superuser),
                               participant: Participant = Body()):
    other_user = await User.get(id_)
    
    if other_user is None:
        raise HTTPException(satus_code=404, detail=f"User {id_} not found.")
    else:
        other_user.experiments.append(participant)
        await other_user.save()
        
        return other_user.experiments


@router.get("/all_experiments",
            response_description="Get all experiments.",
            response_model=List[str])
async def list_experiments(user: User = Depends(current_superuser)):
    experiments = set()

    async for user_ in User.find_all():
        experiments = experiments.union(participant.experiment_name
                                        for participant in user_.experiments)

    return list(experiments)
