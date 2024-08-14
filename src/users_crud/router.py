from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.users_crud.schemas import UserCreate, UserUpdate, UserRead
from src.users_crud.repositories import UserRepo
from src.auth import Authenticator


router = APIRouter(
    prefix="/users",
    tags=["Users CRUD"]
)


@router.post("/register")
async def register_user(user_create: UserCreate) -> JSONResponse:
    user_orm = await UserRepo.create_user(user_create)
    if user_orm is None:
        raise HTTPException(status_code=400, detail="Username already registered")
    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "user_id": user_orm.id
        }
    )


@router.get("/me", response_model=UserRead)
async def get_me(
    current_user: Annotated[UserRead, Depends(Authenticator.get_current_user)],
):
    return current_user


@router.get("/all", response_model=list[UserRead])
async def get_users():
    users_orm = await UserRepo.get_users()
    if not users_orm:
        raise HTTPException(status_code=404, detail="Users not found")
    users_read = [UserRead.from_orm(user_orm) for user_orm in users_orm]
    return users_read


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int):
    user_orm = await UserRepo.get_user(user_id=user_id)
    if user_orm is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_read = UserRead.from_orm(user_orm)
    return user_read


@router.put("/{user_id}")
async def update_user(
        user_id: int,
        user_update: UserUpdate,
) -> JSONResponse:
    user_orm = await UserRepo.update_user(user_id, user_update)
    if user_orm is None:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(
        content={
            "status": "success",
            "user_id": user_orm.id
        }
    )


@router.delete('/{user_id}')
async def delete_user(user_id: int) -> JSONResponse:
    is_deleted = await UserRepo.delete_user(user_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(
        content={
            "status": "success",
            "detail": "User deleted successfully"
        }
    )
