from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from starlette.staticfiles import StaticFiles

from src.database import create_tables, delete_tables
from src.auth import auth_router
from src.users_operations import users_router
from src.pages.router import router as page_router
from src.config import origins


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
app.include_router(page_router)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": f"Welcome inside CleanBuy API!"
    }
