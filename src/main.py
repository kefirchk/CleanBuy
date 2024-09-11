from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.kafka import kafka_client, kafka_config, create_topic
from src.routers import routers
from src.urls import origins, allow_methods, allow_headers
from src.exception_handlers import exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[INFO] Application is started")
    create_topic(kafka_config.KAFKA_TOPIC)
    await kafka_client.start()
    print("[INFO] Kafka is started")
    yield
    await kafka_client.stop()
    print("[INFO] Kafka is closed")
    print("[INFO] Application is closed")


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
