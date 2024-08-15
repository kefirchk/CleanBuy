from typing import Annotated, List

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.users_crud.schemas import UserRead
from src.users_crud.router import get_users, get_me


router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/home")
def get_home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/chat")
async def get_chat_page(
        request: Request,
        current_user: Annotated[UserRead, Depends(get_me)],
        all_users: Annotated[List[UserRead], Depends(get_users)],
        username: str = ""
):
    users = [u for u in all_users if u.username.startswith(username)]
    return templates.TemplateResponse(
        "chat.html", {
            "request": request,
            "users": users
        }
    )
