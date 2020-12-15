import os

from .custom_errors import EnvironmentVariablesError


def get_db_url():
    connection_data = {
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "host": os.getenv("DATABASE_HOST"),
        "port": os.getenv("DATABASE_PORT"),
        "database": os.getenv("POSTGRES_DB"),
    }

    if None in connection_data.values():
        raise EnvironmentVariablesError

    return "postgres://{user}:{password}@{host}:{port}/{database}".format(
        user=connection_data["user"],
        password=connection_data["password"],
        host=connection_data["host"],
        port=connection_data["port"],
        database=connection_data["database"],
    )
