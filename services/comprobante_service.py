"""
Guardar comprobante en disco y asociar al registro.
"""
import base64
import uuid
from pathlib import Path

from models.registro import db, Registro
from config import UPLOAD_FOLDER


def save_comprobante(
    aztlan_id: str,
    comprobante_b64: str,
    filename: str,
    media_type: str,
    size_bytes: int,
) -> tuple[Registro | None, str | None]:
    """
    Busca registro por aztlan_id. Si existe, guarda el archivo y actualiza el registro.
    Devuelve (Registro, referencia_url) o (None, None) si no existe.
    """
    reg = Registro.query.filter_by(aztlan_id=aztlan_id).first()
    if not reg:
        return None, None

    try:
        data = base64.b64decode(comprobante_b64)
    except Exception:
        return reg, None  # Decode error: devolver registro para que el endpoint devuelva 400

    # Nombre único en disco
    ext = Path(filename).suffix or ""
    safe_name = f"{uuid.uuid4().hex}{ext}"
    file_path = UPLOAD_FOLDER / safe_name
    file_path.write_bytes(data)

    # URL/referencia: path relativo o absoluto según cómo lo sirvas
    referencia = f"/comprobantes/{safe_name}"

    reg.comprobante_url = referencia
    reg.comprobante_filename = filename
    reg.comprobante_media_type = media_type
    reg.comprobante_size_bytes = size_bytes
    reg.comprobante_aprobado = False
    db.session.commit()
    return reg, referencia
