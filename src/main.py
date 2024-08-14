from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.database import create_tables
from src.routers import routers
from src.urls import origins, allow_methods, allow_headers


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is started")
    # await create_tables()
    # print("Database is ready")
    yield
    print("Application is closed")


app = FastAPI(title="CleanBuy", lifespan=lifespan)
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

# It doesn't work:
# if __name__ == "__main__":
#     uvicorn.run(
#         app="main:app",
#         host="localhost",
#         port=443,
#         ssl_certfile='../certs/cert.pem',
#         ssl_keyfile='../certs/key.pem'
#     )
# Use
# uvicorn src.main:app --loop asyncio --host localhost --port 443 --ssl-keyfile=certs/key.pem --ssl-certfile=certs/cert.pem
# instead
