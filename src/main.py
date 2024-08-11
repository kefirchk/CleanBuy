from fastapi import FastAPI, Depends

from contextlib import asynccontextmanager

from src.database import create_tables, delete_tables
from src.auth import auth_router, AuthManager
from src.schemas import UserRead
from src.users_operations import users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_tables()
    # print("Database is cleaned!")
    await create_tables()
    print("Database is ready!")
    yield
    print("App is off.")


app = FastAPI(title="CleanBuy", lifespan=lifespan)
app.include_router(auth_router)
app.include_router(users_router)


@app.get("/", tags=["root"])
async def root(current_user: UserRead = Depends(AuthManager.get_current_user)):
    return {
        "message": f"Welcome inside CleanBuy API, {current_user.username}!"
    }
