from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from src.auth import auth_config, Token, Authenticator


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await Authenticator.authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth_config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Token.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/pages/home")
    response.delete_cookie("Authorization")
    return response
