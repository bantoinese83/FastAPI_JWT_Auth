from starlette.responses import JSONResponse
from app.core.logging_config import setup_logger

# Setup logger
logger = setup_logger()

def rate_limit_exceeded_handler(request, exc):
    try:
        # Log the rate limit exceeded event
        logger.error(f"Rate limit exceeded: {str(exc)}")

        return JSONResponse(
            status_code=429,
            content={"message": "Rate limit exceeded", "detail": str(exc)},
        )
    except Exception as e:
        # Log the unexpected error
        logger.error(f"An unexpected error occurred in rate_limit_exceeded_handler: {str(e)}")

        return JSONResponse(
            status_code=500,
            content={"message": "An unexpected error occurred"},
        )