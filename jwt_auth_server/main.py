# main.py
from fastapi import FastAPI

from app.api import auth_routes, user_routes, admin_routes, profile_routes
from app.core.config import setup_database
from app.core.events import shutdown_event, startup_event
from app.core.logging_config import setup_logger
from app.db.database import engine
from app.middlewares.cors import setup_cors
from app.middlewares.exception_handlers import setup_exception_handlers
from app.middlewares.limiter import get_limiter

app = FastAPI(
    title="JWT AUTH API", description="API for Authorization", version="0.1.0"
)
# Set up rate limiting
limiter = get_limiter(app)

# Setup CORS
setup_cors(app)

# Setup exception handlers
setup_exception_handlers(app)

# Setup logging
logger = setup_logger()

# Include the router
app.include_router(auth_routes.router, prefix="/auth")
app.include_router(user_routes.router, prefix="/users")
app.include_router(admin_routes.router, prefix="/admin")
app.include_router(profile_routes.router, prefix="/profile")


# Call the setup functions
setup_database()

# Setup startup and shutdown events
startup_event(app, engine, logger)
shutdown_event(app, logger)
