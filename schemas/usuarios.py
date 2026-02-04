"""
Body para PATCH /usuarios/:id (solo comprobanteAprobado).
"""
from pydantic import BaseModel


class PatchComprobanteAprobado(BaseModel):
    comprobanteAprobado: bool
