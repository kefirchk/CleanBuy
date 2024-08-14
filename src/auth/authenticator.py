from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import Depends, HTTPException, status

from src.auth import oauth2_scheme, auth_config
from src.auth import verify_password
from src.users_crud.schemas import UserRead
from src.users_crud.repositories import UserRepo


class Authenticator:
    @staticmethod
    async def authenticate_user(username: str, password: str) -> UserRead | None:
        user = await UserRepo.get_user(username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return UserRead.from_orm(user)

    @staticmethod
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, auth_config.SECRET_KEY, algorithms=[auth_config.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception
        user = await UserRepo.get_user(username=username)
        if user is None:
            raise credentials_exception
        return UserRead.from_orm(user)
