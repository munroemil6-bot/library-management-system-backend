import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")


def _normalize_database_uri(database_uri):
    if not database_uri:
        return f"sqlite:///{os.path.join(INSTANCE_DIR, 'library.db')}"

    if database_uri.startswith("sqlite:///"):
        relative_path = database_uri[len("sqlite:///"):]
        if relative_path and not os.path.isabs(relative_path):
            absolute_path = os.path.abspath(os.path.join(BASE_DIR, relative_path))
            return f"sqlite:///{absolute_path}"

    return database_uri


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = _normalize_database_uri(os.getenv("DATABASE_URI"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "None")
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "True") == "True"
    REMEMBER_COOKIE_SAMESITE = os.getenv("REMEMBER_COOKIE_SAMESITE", "None")
    REMEMBER_COOKIE_SECURE = os.getenv("REMEMBER_COOKIE_SECURE", "True") == "True"
