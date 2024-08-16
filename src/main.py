from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.database import create_tables
from src.routers import routers
from src.urls import origins, allow_methods, allow_headers
from src.exception_handlers import exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is started")
    # await create_tables()           # If you don't use Alembic, then you can use this
    # print("Database is ready")
    yield
    print("Application is closed")


app = FastAPI(title="CleanBuy", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="src/static"), name="static")


for router in routers:
    app.include_router(router)


for exc_type, handler in exception_handlers.items():
    app.add_exception_handler(exc_type, handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=allow_methods,
    allow_headers=allow_headers,
)


# It doesn't work:
# if __name__ == "__main__":
#     uvicorn.run(
#         app="main:app",
#         host="localhost",
#         port=443,
#         ssl_certfile='../certs/cert.pem',
#         ssl_keyfile='../certs/key.pem'
#     )
#
# Use instead in console:
# uvicorn src.main:app --loop asyncio --host localhost --port 443 --ssl-keyfile=certs/key.pem --ssl-certfile=certs/cert.pem
