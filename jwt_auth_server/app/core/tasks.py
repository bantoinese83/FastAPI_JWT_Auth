# app/core/tasks.py
import os
import subprocess

from fastapi import FastAPI
from fastapi.routing import APIRoute
from sqlalchemy import inspect
from sqlalchemy.engine import Engine

from app.core.logging_config import log_table, log_progress
from app.core.logging_config import setup_logger

# Setup logger
logger = setup_logger()


def get_directory_structure(rootdir):
    """Creates a nested dictionary that represents the folder structure of rootdir"""
    dir_dict = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir_dict = dir_dict
        for folder in folders[:-1]:
            subdir_dict = subdir_dict.setdefault(folder, {})
        if folders[-1] and not folders[-1].startswith("__pycache__"):
            subdir_dict = subdir_dict.setdefault(folders[-1], {})
        for file in files:
            if not file.endswith('.cpython-310.pyc'):
                subdir_dict.setdefault(file, {})
    return dir_dict


def run_black():
    # Specify the directory of your project here
    project_directory = "/Users/doepesci/Desktop/Gempedia/gempedia_server/main.py"

    # Run black on the project directory
    subprocess.run(["black", project_directory], check=True)
    logger.info("Ran black on project directory")
    logger.info("Formatted code using black")
    logger.info("Code formatting complete")
    log_progress("Code formatting", 100, 100)


def log_openapi_routes(app: FastAPI):
    openapi_schema = app.openapi()
    paths = openapi_schema["paths"]

    data = []
    for path, path_item in paths.items():
        for method, operation in path_item.items():
            data.append({
                "Path": path,
                "Method": method,
                "Operation ID": operation.get('operationId'),
                "Summary": operation.get('summary'),
                "Deprecated": operation.get('deprecated'),
                "Tags": operation.get('tags')
            })
    log_table(data)


# Function to log FastAPI routes
# Function to log FastAPI routes
def log_routes(app: FastAPI):
    try:
        data_route = []
        data_name = []
        data_endpoint = []
        data_methods = []
        data_operation = []
        data_tags = []
        data_summary = []
        data_description = []
        data_response = []
        data_deprecation = []
        data_callbacks = []
        data_include_in_schema = []

        for route in app.routes:
            if isinstance(route, APIRoute):
                data_route.append({"Route": route.path})
                data_name.append({"Name": route.name})
                data_endpoint.append({"Endpoint": route.endpoint})
                data_methods.append({"Methods": route.methods})
                data_operation.append({"Operation": route.operation_id})
                data_tags.append({"Tags": route.tags})
                data_summary.append({"Summary": route.summary})
                data_description.append({"Description": route.description})
                data_response.append({"Response": route.response_class})
                data_deprecation.append({"Deprecation": route.deprecated})
                data_callbacks.append({"Callbacks": route.callbacks})
                data_include_in_schema.append({"Include in schema": route.include_in_schema})

        log_table(data_route)
        log_table(data_name)
        log_table(data_endpoint)
        log_table(data_methods)
        log_table(data_operation)
        log_table(data_tags)
        log_table(data_summary)
        log_table(data_description)
        log_table(data_response)
        log_table(data_deprecation)
        log_table(data_callbacks)
        log_table(data_include_in_schema)
    except Exception as e:
        logger.error(f"Error occurred while logging routes: {str(e)}")


# Function to log database tables
def log_tables(engine: Engine):
    try:
        inspector = inspect(engine)
        for table_name in inspector.get_table_names():
            data = []
            for column in inspector.get_columns(table_name):
                data.append({
                    "Table": table_name,
                    "Column": column['name'],
                    "Type": column['type']
                })
            log_table(data)
    except Exception as e:
        logger.error(f"Error occurred while logging database tables: {str(e)}")
