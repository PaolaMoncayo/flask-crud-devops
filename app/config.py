import os
from dotenv import load_dotenv, find_dotenv

# Busca el .env en cualquier carpeta padre y cárgalo
dotenv_path = find_dotenv()
if not dotenv_path:
    raise RuntimeError("No se encontró .env en ninguna carpeta padre")
load_dotenv(dotenv_path)

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
        f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
