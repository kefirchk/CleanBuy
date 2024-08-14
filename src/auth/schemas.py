from datetime import timedelta, datetime, timezone
from typing import Union

import jwt
from pydantic import BaseModel

from src.auth import auth_config


class Token(BaseModel):
    access_token: str
    token_type: str

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, auth_config.SECRET_KEY, algorithm=auth_config.ALGORITHM)
        return encoded_jwt
