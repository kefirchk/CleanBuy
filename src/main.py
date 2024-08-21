from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.kafka import kafka_client, kafka_config, create_topic
from src.s3 import S3Client
from src.routers import routers
from src.urls import origins, allow_methods, allow_headers
from src.exception_handlers import exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[INFO] Application is started")

    # s3_client = S3Client(
    #     access_key="",
    #     secret_key="",
    #     endpoint_url="",  # для Selectel используйте https://s3.storage.selcloud.ru
    #     bucket_name="",
    # )

    # Проверка, что мы можем загрузить, скачать и удалить файл
    # await s3_client.upload_file("test.txt")
    # await s3_client.get_file("test.txt", "text_local_file.txt")
    # await s3_client.delete_file("test.txt")

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


# It doesn't work:
# if __name__ == "__main__":
#     uvicorn.run(
#         app="main:app",
#         host="localhost",
#         port=443,
#         ssl_certfile='../certs/cert.pem',
#         ssl_keyfile='../certs/key.pem'
#     )

# Use instead in console:
# uvicorn src.main:app --host localhost --port 443 --ssl-keyfile=certs/key.pem --ssl-certfile=certs/cert.pem
