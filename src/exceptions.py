from main import app

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import ResponseValidationError


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
