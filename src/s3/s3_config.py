# ATTENTION! I use IDrive S3

from pydantic_settings import BaseSettings, SettingsConfigDict


class S3Config(BaseSettings):
    ACCESS_KEY: str
    SECRET_KEY: str
    ENDPOINT_URL: str
    BUCKET_NAME: str

    model_config = SettingsConfigDict(env_file='_envs/.env.s3')


s3_config = S3Config()
