from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.database import create_tables
from src.routers import routers
from src.urls import origins, allow_methods, allow_headers


app = FastAPI(title="CleanBuy")
app.mount("/static", StaticFiles(directory="src/static"), name="static")


for router in routers:
    app.include_router(router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=allow_methods,
    allow_headers=allow_headers,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is started")
    # await create_tables()
    # print("Database is ready")
    yield
    print("Application is closed")
