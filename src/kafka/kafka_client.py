import json

from aiokafka import AIOKafkaProducer

from src.chat import Message
from src.kafka import kafka_config


class KafkaClient:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def send_message(self, topic: str, key: str, msg: Message):
        if self.producer:
            print(f"[INFO] Sending message to topic {topic}")
            await self.producer.send_and_wait(topic, KafkaClient.__msg_to_json(msg).encode('utf-8'), key=key.encode('utf-8'))

    @staticmethod
    def __msg_to_dict(msg: Message):
        return {
            "chat_id": msg.chat_id,
            "sender_id": msg.sender_id,
            "message": msg.message,
            "username": msg.username,
            "timestamp": msg.timestamp,
            "file": msg.file.model_dump() if msg.file else None
        }

    @staticmethod
    def __msg_to_json(msg: Message):
        return json.dumps(KafkaClient.__msg_to_dict(msg))


kafka_client = KafkaClient(bootstrap_servers=kafka_config.KAFKA_BOOTSTRAP_SERVERS)
