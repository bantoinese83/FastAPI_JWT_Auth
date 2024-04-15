from dotenv import load_dotenv
from loguru import logger
from rich.logging import RichHandler

from app.db.base import Base
from app.db.database import engine

load_dotenv()


def setup_database():
    # Database setup
    Base.metadata.create_all(bind=engine)


def setup_logger():
    # Setup logging
    FORMAT = "%(time)s %(level)s %(message)s"
    logger.remove()
    logger.add(RichHandler(rich_tracebacks=True), format=FORMAT)
    return logger




# Call the setup functions
setup_database()
setup_logger()
