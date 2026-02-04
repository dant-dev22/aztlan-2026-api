"""
Validación de body para POST /registro según tipoRegistro (Pydantic).
"""
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class RegistroComun(BaseModel):
    """Campos comunes a todos los tipos."""
    tipo_registro: Literal["juvenil", "adultos", "masters"]
    nombre_completo: str = Field(..., min_length=1, max_length=255)
    email: str = Field(..., min_length=1, max_length=255)
    timestamp: str = Field(..., min_length=1)  # ISO string


class RegistroJuvenil(RegistroComun):
    """Campos requeridos cuando tipoRegistro === 'juvenil'."""
    tipo_registro: Literal["juvenil"] = "juvenil"
    sexo: str = Field(..., min_length=1, max_length=20)
    cinta: str = Field(..., min_length=1, max_length=50)
    nivel_experiencia: str = Field(..., min_length=1, max_length=100)
    categoria_edad: str = Field(..., min_length=1, max_length=50)
    categoria_peso: str = Field(..., min_length=1, max_length=50)


class RegistroAdultosMasters(RegistroComun):
    """Campos requeridos cuando tipoRegistro === 'adultos' o 'masters'."""
    tipo_registro: Literal["adultos", "masters"]
    edad: int = Field(..., ge=1, le=120)
    sexo: str = Field(..., min_length=1, max_length=20)
    nivel_experiencia: str = Field(..., min_length=1, max_length=100)
    categoria_peso: str = Field(..., min_length=1, max_length=50)
    categoria_peso_tipo: Literal["varonil", "femenil"]


def parse_registro_body(data: dict) -> RegistroJuvenil | RegistroAdultosMasters:
    """
    Valida el body según tipoRegistro y devuelve el modelo correcto.
    Lanza ValidationError si falta algún campo requerido o es inválido.
    """
    tipo = data.get("tipoRegistro") or data.get("tipo_registro")
    if not tipo:
        raise ValueError("tipoRegistro es requerido")

    # Normalizar keys del JSON (camelCase) a nuestro modelo (snake_case)
    def to_snake(d: dict) -> dict:
        mapping = {
            "tipoRegistro": "tipo_registro",
            "nombreCompleto": "nombre_completo",
            "nivelExperiencia": "nivel_experiencia",
            "categoriaEdad": "categoria_edad",
            "categoriaPeso": "categoria_peso",
            "categoriaPesoTipo": "categoria_peso_tipo",
        }
        out = {}
        for k, v in d.items():
            out[mapping.get(k, k)] = v
        return out

    normalized = to_snake(data)

    if tipo == "juvenil":
        return RegistroJuvenil.model_validate(normalized)
    if tipo in ("adultos", "masters"):
        return RegistroAdultosMasters.model_validate(normalized)
    raise ValueError("tipoRegistro debe ser 'juvenil', 'adultos' o 'masters'")
