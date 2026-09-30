import os
from urllib.parse import quote_plus

from dotenv import load_dotenv


load_dotenv()


def _resolve_database_url():
    existing_url = os.getenv("DATABASE_URL")
    if existing_url:
        if existing_url.startswith("mysql://"):
            return existing_url.replace("mysql://", "mysql+pymysql://", 1)
        if not existing_url.startswith("mysql+pymysql://"):
            raise RuntimeError("DATABASE_URL must use MySQL with the PyMySQL driver")
        return existing_url

    is_running_in_container = os.path.exists("/.dockerenv") or os.getenv("DOCKER_CONTAINER") == "1"
    if is_running_in_container:
        host = "db"
    else:
        host = os.getenv("MYSQL_HOST", "localhost")

    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD") or os.getenv("MYSQL_ROOT_PASSWORD")
    if not password:
        raise RuntimeError("Set DATABASE_URL or MYSQL_PASSWORD in the environment")
    database = os.getenv("MYSQL_DATABASE", "task_manager_db")

    return (
        f"mysql+pymysql://{quote_plus(user)}:{quote_plus(password)}"
        f"@{host}/{quote_plus(database)}"
    )


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    CORS_ORIGINS = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    )
    CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS.split(",") if origin.strip()]

    @staticmethod
    def resolve_database_url():
        return _resolve_database_url()
