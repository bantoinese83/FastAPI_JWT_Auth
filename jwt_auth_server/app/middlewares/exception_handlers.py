from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging_config import setup_logger

logger = setup_logger()


async def ratelimit_handler(request: Request, exc: RateLimitExceeded):
    logger.error(f"Rate limit exceeded: {exc}")
    return JSONResponse(
        status_code=429,
        content={"detail": "Too Many Requests"},
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"Error occurred: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error occurred: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"Starlette HTTP exception occurred: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )



def setup_exception_handlers(app):
    app.add_exception_handler(RateLimitExceeded, ratelimit_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, starlette_http_exception_handler)
