from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import delete_tables, create_tables
from src.routing.buyer_router import router as buyer_router
from src.routing.auth_router import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_tables()
    # print("Database is cleaned!")
    await create_tables()
    print("Database is ready!")
    yield
    print("App is off.")


app = FastAPI(title="CleanBuy", lifespan=lifespan)
app.include_router(buyer_router)
app.include_router(auth_router)
