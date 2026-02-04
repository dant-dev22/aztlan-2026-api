"""
POST /registro - Recibir formularios de registro.
"""
from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from schemas.registro import parse_registro_body
from services.registro_service import create_registro

bp = Blueprint("registro", __name__, url_prefix="/registro")


@bp.route("", methods=["POST"])
def post_registro():
    """
    Registro de participante (juvenil, adultos o masters)
    ---
    tags:
      - Registro
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - tipoRegistro
            - nombreCompleto
            - email
            - timestamp
          properties:
            tipoRegistro:
              type: string
              enum: [juvenil, adultos, masters]
            nombreCompleto:
              type: string
            email:
              type: string
            timestamp:
              type: string
              format: date-time
            sexo:
              type: string
            cinta:
              type: string
            nivelExperiencia:
              type: string
            categoriaEdad:
              type: string
            categoriaPeso:
              type: string
            edad:
              type: integer
            categoriaPesoTipo:
              type: string
              enum: [varonil, femenil]
    responses:
      201:
        description: Registro creado
        schema:
          type: object
          properties:
            nombreParticipante:
              type: string
            mensaje:
              type: string
            statusCode:
              type: integer
              example: 200
            aztlan_id:
              type: string
      400:
        description: Validación fallida
    """
    try:
        body = request.get_json(force=True, silent=True) or {}
        payload = parse_registro_body(body)
    except ValidationError as e:
        return jsonify({"error": "Validación fallida", "detalles": e.errors()}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    reg = create_registro(payload)
    return (
        jsonify({
            "nombreParticipante": reg.nombre_completo,
            "mensaje": "Registro creado correctamente. Envía tu comprobante para completar.",
            "statusCode": 200,
            "aztlan_id": reg.aztlan_id,
        }),
        201,
    )
