# ATTENTION! I use IDrive S3

from contextlib import asynccontextmanager

from aiobotocore.session import get_session
from botocore.exceptions import ClientError

from src.s3 import s3_config


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str
    ):
        self.config = {
            # "region_name": "Los Angeles",
            "aws_access_key_id": "DO52sy279IPjHmX5Q0RT",
            "aws_secret_access_key": "zvYw0PWeRj8UggqWEDOATPGpMpu7RJS1U3XuMYPI",
            "endpoint_url": "https://k7m8.la.idrivee2-37.com"  # endpoint_url,
        }
        self.bucket_name = "cleanbuy-chat-bucket"
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
            self,
            file_path: str,
    ):
        print("[INFO] <START UPLOAD_FILE FUNCTION>")
        object_name = file_path.split("/")[-1]  # /users/artem/cat.jpg
        try:
            async with self.get_client() as client:
                with open(file_path, "rb") as file:
                    await client.put_object(
                        Bucket=self.bucket_name,
                        Key=object_name,
                        Body=file,
                    )
                print(f"[INFO] File {object_name} uploaded to {self.bucket_name}")
        except ClientError as e:
            print(f"[ERROR] Failed to upload file: {e}")
        finally:
            print("[INFO] <END UPLOAD_FILE FUNCTION>")

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
                print(f"File {object_name} deleted from {self.bucket_name}")
        except ClientError as e:
            print(f"Error deleting file: {e}")

    async def get_file(self, object_name: str, destination_path: str):
        print("[INFO] START GET_FILE FUNCTION")
        try:
            async with self.get_client() as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=object_name)
                data = await response["Body"].read()
                with open(destination_path, "wb") as file:
                    file.write(data)
                print(f"[INFO] File {object_name} downloaded to {destination_path}")
        except ClientError as e:
            print(f"[ERROR] Failed to download file: {e}")
        finally:
            print("[INFO] END GET_FILE FUNCTION")


s3_client = S3Client(
    access_key=s3_config.ACCESS_KEY,
    secret_key=s3_config.SECRET_KEY,
    endpoint_url=s3_config.ENDPOINT_URL,
    bucket_name=s3_config.BUCKET_NAME,
)
