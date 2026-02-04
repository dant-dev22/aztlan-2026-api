"""
Configuración de la aplicación desde variables de entorno.
Modo mock: SQLite en memoria cuando DB_USE_MOCK=true (sin MySQL).
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Servidor
PORT = int(os.getenv("PORT", "5000"))

# Base de datos
DB_USE_MOCK = os.getenv("DB_USE_MOCK", "true").lower() in ("true", "1", "yes")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "aztlan26")

if DB_USE_MOCK:
    # SQLite en memoria: mismo modelo, sin MySQL. Cambiar a MySQL después.
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
else:
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True} if not DB_USE_MOCK else {}

# Comprobantes
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / os.getenv("UPLOAD_FOLDER", "uploads/comprobantes")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
