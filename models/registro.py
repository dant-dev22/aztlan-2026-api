"""
Modelo de registro compatible con MySQL (SQLAlchemy).
Un solo modelo con campos opcionales según tipoRegistro (juvenil / adultos / masters).
"""
import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


class Registro(db.Model):
    """
    Registro de participante. Campos comunes + opcionales por tipo.
    MySQL: tipos equivalentes (VARCHAR, INT, TEXT, DATETIME, BOOLEAN).
    """
    __tablename__ = "registros"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    aztlan_id = db.Column(db.String(64), unique=True, nullable=False, index=True)

    tipo_registro = db.Column(db.String(20), nullable=False)  # juvenil | adultos | masters
    nombre_completo = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)  # ISO string recibido

    # Juvenil
    sexo = db.Column(db.String(20), nullable=True)
    cinta = db.Column(db.String(50), nullable=True)
    nivel_experiencia = db.Column(db.String(100), nullable=True)
    categoria_edad = db.Column(db.String(50), nullable=True)
    categoria_peso = db.Column(db.String(50), nullable=True)

    # Adultos / Masters
    edad = db.Column(db.Numeric(5, 0), nullable=True)
    categoria_peso_tipo = db.Column(db.String(20), nullable=True)  # varonil | femenil

    # Comprobante
    comprobante_aprobado = db.Column(db.Boolean, default=False, nullable=False)
    comprobante_url = db.Column(db.String(512), nullable=True)
    comprobante_filename = db.Column(db.String(255), nullable=True)
    comprobante_media_type = db.Column(db.String(100), nullable=True)
    comprobante_size_bytes = db.Column(db.Numeric(12, 0), nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        d = {
            "id": self.id,
            "tipoRegistro": self.tipo_registro,
            "nombreCompleto": self.nombre_completo,
            "email": self.email,
            "timestamp": self.timestamp,
            "aztlan_id": self.aztlan_id,
            "comprobanteAprobado": self.comprobante_aprobado,
            "comprobanteUrl": self.comprobante_url,
            "createdAt": self.created_at.isoformat() if self.created_at else None,
        }
        if self.sexo is not None:
            d["sexo"] = self.sexo
        if self.cinta is not None:
            d["cinta"] = self.cinta
        if self.nivel_experiencia is not None:
            d["nivelExperiencia"] = self.nivel_experiencia
        if self.categoria_edad is not None:
            d["categoriaEdad"] = self.categoria_edad
        if self.categoria_peso is not None:
            d["categoriaPeso"] = self.categoria_peso
        if self.edad is not None:
            d["edad"] = int(self.edad)
        if self.categoria_peso_tipo is not None:
            d["categoriaPesoTipo"] = self.categoria_peso_tipo
        return d
