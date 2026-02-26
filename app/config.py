import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "")