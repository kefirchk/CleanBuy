from enum import Enum

from pydantic import BaseModel


class ChatType(str, Enum):
    PERSONAL = "PERSONAL"


class File(BaseModel):
    file_url: str | None
    filename: str | None
    file_size: int | None
    file_type: str | None


class Message(BaseModel):
    chat_id: int
    sender_id: int
    message: str | None
    username: str | None
    timestamp: str | None
    file: File | None
