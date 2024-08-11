from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.auth import AuthManager
from src.repositories import UserRepo
from src.schemas import UserRead, UserUpdate


router = APIRouter(
    prefix="/users",
    tags=["User Operations"]
)


@router.get("/me", response_model=UserRead)
async def get_me(
    current_user: Annotated[UserRead, Depends(AuthManager.get_current_user)],
):
    return current_user


@router.get("/all", response_model=list[UserRead])
async def get_users():
    users_orm = await UserRepo.get_users()
    if not users_orm:
        raise HTTPException(status_code=404, detail="Buyers not found")
    users_read = [UserRead.from_orm(user_orm) for user_orm in users_orm]
    return users_read


@router.get("/{user_id}")
async def get_user(user_id: int):
    user_orm = await UserRepo.get_user(user_id=user_id)
    if user_orm is None:
        raise HTTPException(status_code=404, detail="Buyer not found")
    user_read = UserRead.from_orm(user_orm)
    print(user_read)
    return user_read


@router.put("/{user_id}", response_model=dict)
async def update_user(
        user_id: int,
        user_update: UserUpdate,
):
    user_orm = await UserRepo.update_user(user_id, user_update)
    if user_orm is None:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return {
        "status": "success",
        "user_id": user_orm.id
    }


@router.delete('/{user_id}', response_model=dict)
async def delete_user(user_id: int):
    is_deleted = await UserRepo.delete_user(user_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return {
        "status": "success",
        "message": "Buyer deleted successfully."
    }
