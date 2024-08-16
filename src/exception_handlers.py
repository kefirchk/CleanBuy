from fastapi import Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import HTTPException


async def bad_request_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.detail},
    )


async def validation_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.detail},
    )


async def unauthorized_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return RedirectResponse(url="/pages/home")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def not_found_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Page not found"},
    )


async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


exception_handlers = {
    status.HTTP_400_BAD_REQUEST: bad_request_exception_handler,
    status.HTTP_401_UNAUTHORIZED: unauthorized_exception_handler,
    status.HTTP_404_NOT_FOUND: not_found_exception_handler,
    status.HTTP_422_UNPROCESSABLE_ENTITY: validation_exception_handler,
    Exception: global_exception_handler
}
