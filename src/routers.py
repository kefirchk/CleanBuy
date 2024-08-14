from src.auth import auth_router
from src.users_crud.router import router as users_crud_router
from src.pages import pages_router
from src.chat import chat_router

routers = [
    auth_router,
    users_crud_router,
    pages_router,
    chat_router
]
