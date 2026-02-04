"""
Validación del body para POST /comprobante.
"""
from pydantic import BaseModel, Field


class ComprobanteBody(BaseModel):
    aztlan_id: str = Field(..., min_length=1)
    comprobante: str = Field(..., min_length=1)  # base64
    comprobante_filename: str = Field(..., min_length=1, max_length=255)
    comprobante_media_type: str = Field(..., min_length=1, max_length=100)
    comprobante_size_bytes: int = Field(..., ge=0)
    timestamp: str = Field(..., min_length=1)  # ISO
