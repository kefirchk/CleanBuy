from typing import Annotated, List

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates

from src.users_crud.schemas import UserRead
from src.auth import Authenticator
from src.users_crud.router import get_users, get_me

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/home")
async def get_home_page(
        request: Request,
        optional_user: Annotated[UserRead, Depends(Authenticator.get_optional_user)]
):
    return templates.TemplateResponse(
        "home.html", {
            "request": request,
            "current_user": optional_user
        }
    )


@router.get("/chat")
async def get_chat_page(
        request: Request,
        all_users: Annotated[List[UserRead], Depends(get_users)],
        current_user: Annotated[UserRead, Depends(get_me)],
        username: str = "",
):
    users = [u for u in all_users if u.username.startswith(username)]
    return templates.TemplateResponse(
        "chat.html", {
            "request": request,
            "users": users,
            "current_user": current_user
        }
    )


@router.get("/account")
async def get_account_page(
        request: Request,
        current_user: UserRead = Depends(get_me)
):
    return templates.TemplateResponse(
        "account.html", {
            "request": request,
            "current_user": current_user
        }
    )

