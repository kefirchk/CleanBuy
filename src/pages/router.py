from typing import Annotated, List

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.schemas import UserRead
from src.users_operations.router import get_users, get_me

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@router.get("/home")
def get_home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/search/")
def get_search_page(request: Request, all_users: Annotated[List[UserRead], Depends(get_users)], username: str = ""):
    users = []
    for u in all_users:
        if u.username.startswith(username):
            users.append(u)
    return templates.TemplateResponse(
        "search.html", {
            "request": request,
            "users": users
        }
    )
