from fastapi import FastAPI
from sqlalchemy.engine import Engine

from app.core.logging_config import log_tree, setup_logger
from app.core.tasks import run_black, log_openapi_routes, log_routes, log_tables, get_directory_structure

# Setup logger
logger = setup_logger()


# task_utils.py
def create_tasks(app: FastAPI, engine: Engine):
    return [
        ("CodeFormattingAndLoggingRoutes", lambda: task1(app)),
        ("LoggingTablesAndDirectoryStructure", lambda: task2(engine))
    ]


def task1(app: FastAPI):
    logger.info("Running task1: Code formatting and logging routes")
    run_black()  # Run black
    log_openapi_routes(app)
    log_routes(app)
    logger.info("Completed task1")


def task2(engine: Engine):
    logger.info("Running task2: Logging tables and directory structure")
    log_tables(engine)
    directory_structure = get_directory_structure("/Users/doepesci/Desktop/Gempedia/gempedia_server")
    log_tree(directory_structure)
    logger.info("Completed task2")

# Add more tasks as needed
