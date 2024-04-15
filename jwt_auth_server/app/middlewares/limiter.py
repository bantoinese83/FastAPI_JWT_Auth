from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

def setup_limiter(app):
    # Rate limiting setup
    limiter = Limiter(key_func=get_remote_address, default_limits=["100 per minute"])

    # Add the middleware to the app
    app.add_middleware(SlowAPIMiddleware)
    return limiter

def get_limiter(app) -> Limiter:
    # Get the limiter instance
    limiter = setup_limiter(app)
    return limiter