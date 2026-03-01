import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = INSTANCE_DIR / "database.db"

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

    # Handle Postgres URL
    database_url = os.getenv("DATABASE_URL")
    if database_url and database_url.startswith("postgres://"):
        # Replace postgres with postgresql to work with SQLAlchemy
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    # Default to SQLite in the local environment if databse url is not set
    SQLALCHEMY_DATABASE_URI = database_url or f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False