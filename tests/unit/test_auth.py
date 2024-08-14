from datetime import timedelta, datetime, timezone
from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient

import jwt

from src.auth import auth_config
from src.auth import pwd_context
from src.auth.utils import get_password_hash, verify_password
from src.users_crud.models import UserOrm
from src.users_crud.schemas import UserRead
from src.auth import Token, Authenticator

from fastapi import HTTPException, status


async def test_login(mocker, ac: AsyncClient, user_read_data):
    form_data = {
        "username": "bob",
        "password": "1234"
    }
    mock_authenticate_user = mocker.patch(
        'src.auth.router.Authenticator.authenticate_user',
        return_value=UserRead(**user_read_data)
    )
    mock_create_access_token = mocker.patch(
        'src.auth.router.Token.create_access_token',
        return_value="TOKEN"
    )
    response = await ac.post(url="/auth/login", data=form_data)

    assert response.status_code == 200
    json_response = response.json()
    assert json_response == {"access_token": "TOKEN", "token_type": "bearer"}


@pytest.mark.parametrize("expires_delta, expected_exp", [
    (None, timedelta(minutes=15)),
    (timedelta(minutes=5), timedelta(minutes=5)),
])
def test_create_access_token(expires_delta, expected_exp):
    data = {"sub": "test_user"}
    token = Token.create_access_token(data, expires_delta)

    decoded_token = jwt.decode(token, auth_config.SECRET_KEY, algorithms=[auth_config.ALGORITHM])
    assert decoded_token["sub"] == data["sub"]

    expected_exp_time = datetime.now(timezone.utc) + expected_exp
    actual_exp_time = datetime.fromtimestamp(decoded_token["exp"], timezone.utc)
    assert abs((expected_exp_time - actual_exp_time).total_seconds()) < 1


async def test_authenticate_user_user_not_found(mocker):
    mock_get_user = mocker.patch(
        'src.auth.authenticator.UserRepo.get_user',
        new_callable=AsyncMock,
        return_value=None
    )

    result = await Authenticator.authenticate_user(
        username="test_user",
        password="wrong_password"
    )

    assert result is None
    mock_get_user.assert_called_once_with(username="test_user")


async def test_authenticate_user_incorrect_password(mocker):
    mock_get_user = mocker.patch(
        'src.auth.authenticator.UserRepo.get_user',
        new_callable=AsyncMock,
        return_value=UserOrm(hashed_password="hashed_password")
    )
    mock_verify_password = mocker.patch(
        'src.auth.authenticator.verify_password',
        return_value=False
    )
    result = await Authenticator.authenticate_user("test_user", "wrong_password")

    assert result is None
    mock_get_user.assert_called_once_with(username="test_user")
    mock_verify_password.assert_called_once_with("wrong_password", "hashed_password")


async def test_authenticate_user_success(mocker, user_orm_data):
    mock_get_user = mocker.patch(
        'src.auth.authenticator.UserRepo.get_user',
        new_callable=AsyncMock,
        return_value=UserOrm(**user_orm_data)
    )
    mock_verify_password = mocker.patch(
        'src.auth.authenticator.verify_password',
        return_value=True
    )
    result = await Authenticator.authenticate_user("test_user", "correct_password")

    assert result is not None
    assert isinstance(result, UserRead)
    assert result.username == "test_user"

    mock_get_user.assert_called_once_with(username="test_user")
    mock_verify_password.assert_called_once_with("correct_password", "hashed_password")


async def test_get_current_user_success(mocker, user_orm_data):
    mock_jwt_decode = mocker.patch(
        'jwt.decode',
        return_value={"sub": "test_user"}
    )
    mock_get_user = mocker.patch(
        'src.auth.authenticator.UserRepo.get_user',
        new_callable=AsyncMock,
        return_value=UserOrm(**user_orm_data)
    )
    result = await Authenticator.get_current_user("valid_token")

    assert result is not None
    assert isinstance(result, UserRead)
    assert result.username == "test_user"

    mock_jwt_decode.assert_called_once_with("valid_token", auth_config.SECRET_KEY, algorithms=[auth_config.ALGORITHM])
    mock_get_user.assert_called_once_with(username="test_user")


async def test_get_current_user_invalid_token(mocker):
    mock_jwt_decode = mocker.patch(
        'jwt.decode',
        side_effect=jwt.InvalidTokenError
    )
    with pytest.raises(HTTPException) as exc_info:
        await Authenticator.get_current_user("invalid_token")

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate credentials"
    assert exc_info.value.headers["WWW-Authenticate"] == "Bearer"

    mock_jwt_decode.assert_called_once_with("invalid_token", auth_config.SECRET_KEY, algorithms=[auth_config.ALGORITHM])


async def test_get_current_user_user_not_found(mocker):
    mock_jwt_decode = mocker.patch(
        'jwt.decode',
        return_value={"sub": "test_user"}
    )
    mock_get_user = mocker.patch(
        'src.auth.authenticator.UserRepo.get_user',
        new_callable=AsyncMock,
        return_value=None
    )
    with pytest.raises(HTTPException) as exc_info:
        await Authenticator.get_current_user("valid_token")

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate credentials"
    assert exc_info.value.headers["WWW-Authenticate"] == "Bearer"

    mock_jwt_decode.assert_called_once_with("valid_token", auth_config.SECRET_KEY, algorithms=[auth_config.ALGORITHM])
    mock_get_user.assert_called_once_with(username="test_user")


def test_get_password_hash():
    password = "my_secret_password"
    hashed_password = get_password_hash(password)
    assert hashed_password != password
    assert pwd_context.verify(password, hashed_password)


def test_verify_password():
    password = "my_secret_password"
    hashed_password = pwd_context.hash(password)
    assert verify_password(password, hashed_password) is True
    assert verify_password("wrong_password", hashed_password) is False

