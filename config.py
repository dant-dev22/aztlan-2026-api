"""
Configuración de la aplicación desde variables de entorno.
Base de datos: MySQL (configurar .env en el servidor).
"""
import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()

# Servidor
PORT = int(os.getenv("PORT", "5000"))

# Base de datos MySQL
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "aztlan2026")

# URI con contraseña escapada por si contiene caracteres especiales
_password = quote_plus(DB_PASSWORD)
SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{DB_USER}:{_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

# Comprobantes
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / os.getenv("UPLOAD_FOLDER", "uploads/comprobantes")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# Email (Gmail SMTP)
GMAIL_USER = os.getenv("GMAIL_USER", "").strip()
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "").strip()
EMAIL_ENABLED = bool(GMAIL_USER and GMAIL_APP_PASSWORD)
