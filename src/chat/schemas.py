from enum import Enum

from pydantic import BaseModel
from datetime import datetime


class ChatType(str, Enum):
    PERSONAL = "PERSONAL"
    # GROUP = "GROUP"


class Message(BaseModel):
    message: str
    timestamp: datetime
    user_id: int
