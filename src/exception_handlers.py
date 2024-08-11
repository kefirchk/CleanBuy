from main import app

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import ResponseValidationError, HTTPException


@app.exception_handler(ResponseValidationError)
async def response_validation_exception_handler(request: Request, exc: ResponseValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": [
                {
                    "loc": err["loc"],
                    "msg": err["msg"],
                    "type": err["type"],
                }
                for err in exc.errors()
            ]
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error."},
    )


@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"detail": "Route not found"},
    )
