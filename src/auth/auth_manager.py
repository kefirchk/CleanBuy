from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

import jwt
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError

from src.auth.utils import verify_password
from src.config import settings
from src.repositories import UserRepo

from src.auth.base_config import oauth2_scheme
from src.schemas import UserRead


class AuthManager:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @classmethod
    async def authenticate_user(cls, username: str, password: str) -> UserRead | None:
        user = await UserRepo.get_user(username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return UserRead.from_orm(user)

    @classmethod
    async def get_current_user(cls, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception
        user = await UserRepo.get_user(username=username)
        if user is None:
            raise credentials_exception
        return UserRead.from_orm(user)
