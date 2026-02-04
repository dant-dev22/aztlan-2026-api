"""
POST /comprobante - Recibir comprobante y asociar al registro.
"""
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from datetime import datetime

from schemas.comprobante import ComprobanteBody
from services.comprobante_service import save_comprobante

bp = Blueprint("comprobante", __name__, url_prefix="/comprobante")


@bp.route("", methods=["POST"])
def post_comprobante():
    """
    Recibir comprobante y asociar al registro (terminar registro)
    ---
    tags:
      - Comprobante
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - aztlan_id
            - comprobante
            - comprobante_filename
            - comprobante_media_type
            - comprobante_size_bytes
            - timestamp
          properties:
            aztlan_id:
              type: string
            comprobante:
              type: string
              description: Contenido en base64
            comprobante_filename:
              type: string
            comprobante_media_type:
              type: string
            comprobante_size_bytes:
              type: integer
            timestamp:
              type: string
              format: date-time
    responses:
      200:
        description: Comprobante recibido
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
            referencia:
              type: string
            timestamp:
              type: string
      404:
        description: Registro no encontrado
      400:
        description: Validación fallida o comprobante inválido
    """
    try:
        body = request.get_json(force=True, silent=True) or {}
        payload = ComprobanteBody.model_validate(body)
    except ValidationError as e:
        return jsonify({"error": "Validación fallida", "detalles": e.errors()}), 400

    reg, referencia = save_comprobante(
        aztlan_id=payload.aztlan_id,
        comprobante_b64=payload.comprobante,
        filename=payload.comprobante_filename,
        media_type=payload.comprobante_media_type,
        size_bytes=payload.comprobante_size_bytes,
    )

    if reg is None:
        return jsonify({"error": "Registro no encontrado"}), 404

    if referencia is None:
        return jsonify({"error": "Comprobante inválido (base64)"}), 400

    return jsonify({
        "success": True,
        "message": "Comprobante recibido y pendiente de aprobación",
        "referencia": referencia,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }), 200
