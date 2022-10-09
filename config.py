import os
from pathlib import Path

BASE_DIR = Path(__file__).parent


class Config:
    PATH_TO_FIXTURES = BASE_DIR / "fixtures"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or f"sqlite:///{BASE_DIR / 'main.db'}"
    TEST_DATABASE = f"sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Зачем эта настройка: https://flask-sqlalchemy-russian.readthedocs.io/ru/latest/config.html#id2
    DEBUG = True
    PORT = 5000
    SECRET_KEY = "My secret key =)"
    RESTFUL_JSON = {
        'ensure_ascii': False,
    }
