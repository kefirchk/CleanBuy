from enum import Enum

from pydantic import BaseModel


class ChatType(str, Enum):
    PERSONAL = "PERSONAL"


class Message(BaseModel):
    message: str
    timestamp: str
    sender_id: int
    chat_id: int
    username: str
