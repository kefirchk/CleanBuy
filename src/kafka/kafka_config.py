from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaConfig(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC: str
    KAFKA_GROUP_ID: str

    model_config = SettingsConfigDict(env_file='_envs/.env.kafka')


kafka_config = KafkaConfig()
