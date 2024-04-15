from fastapi import FastAPI
from sqlalchemy import Engine
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.logging_config import log_progress, log_tasks
from app.core.logging_config import setup_logger
from app.utils.task_utils import create_tasks
from app.errors.error_handlers import rate_limit_exceeded_handler

# Setup logger
logger = setup_logger()
limiter = Limiter(key_func=get_remote_address)

class State:
    limiter: Limiter = None

app = FastAPI()
app.state = State()

# events.py
def startup_event(fastapi_app: FastAPI, engine: Engine, event_logger):
    @fastapi_app.on_event("startup")
    async def startup():
        # Add the limiter instance to the state
        fastapi_app.state.limiter = limiter
        # Add the rate limit exceeded handler
        fastapi_app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
        try:
            tasks = create_tasks(fastapi_app, engine)
            event_logger.info("Application startup")
            for task_name, task_func in tasks:
                event_logger.info(f"Running {task_name}")
                task_func()  # Execute the task function
                event_logger.info(f"Completed {task_name}")
            log_progress("Startup", 100, 100)
            log_tasks(tasks)  # Log the tasks
        except Exception as e:
            logger.error(f"Error occurred during startup: {str(e)}")

# Shutdown event handler
def shutdown_event(fastapi_app: FastAPI, event_logger):
    @fastapi_app.on_event("shutdown")
    async def shutdown():
        try:
            event_logger.info("Application shutdown")
            log_progress("Shutdown", 100, 100)
        except Exception as e:
            logger.error(f"Error occurred during shutdown: {str(e)}")