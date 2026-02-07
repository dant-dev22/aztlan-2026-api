"""
GET /usuarios, PATCH /usuarios/:id, DELETE /usuarios/:id - Dashboard.
"""
from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from models.registro import Registro, db
from schemas.usuarios import PatchComprobanteAprobado
from services.email_service import send_email_pago_aprobado

bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@bp.route("", methods=["GET"])
def get_usuarios():
    """
    Lista todos los registros (dashboard)
    ---
    tags:
      - Usuarios
    responses:
      200:
        description: Lista de registros
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              tipoRegistro:
                type: string
              nombreCompleto:
                type: string
              email:
                type: string
              timestamp:
                type: string
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
              comprobanteAprobado:
                type: boolean
              comprobanteUrl:
                type: string
              createdAt:
                type: string
    """
    registros = Registro.query.order_by(Registro.created_at.desc()).all()
    return jsonify([r.to_dict() for r in registros]), 200


@bp.route("/<id>", methods=["PATCH"])
def patch_usuario(id: str):
    """
    Actualizar comprobanteAprobado (aprobar/rechazar comprobante)
    ---
    tags:
      - Usuarios
    parameters:
      - in: path
        name: id
        required: true
        type: string
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - comprobanteAprobado
          properties:
            comprobanteAprobado:
              type: boolean
    responses:
      200:
        description: Registro actualizado
      404:
        description: Registro no encontrado
      400:
        description: Validación fallida
    """
    reg = Registro.query.get(id)
    if not reg:
        return jsonify({"error": "Registro no encontrado"}), 404

    try:
        body = request.get_json(force=True, silent=True) or {}
        payload = PatchComprobanteAprobado.model_validate(body)
    except ValidationError as e:
        return jsonify({"error": "Validación fallida", "detalles": e.errors()}), 400

    aprobado_antes = reg.comprobante_aprobado
    reg.comprobante_aprobado = payload.comprobanteAprobado
    db.session.commit()
    # Enviar correo solo cuando el admin aprueba (pasa de no aprobado a aprobado)
    if payload.comprobanteAprobado and not aprobado_antes:
        send_email_pago_aprobado(to_email=reg.email, nombre=reg.nombre_completo)
    return jsonify(reg.to_dict()), 200


@bp.route("/<id>", methods=["DELETE"])
def delete_usuario(id: str):
    """
    Eliminar registro por id
    ---
    tags:
      - Usuarios
    parameters:
      - in: path
        name: id
        required: true
        type: string
    responses:
      204:
        description: Registro eliminado
      404:
        description: Registro no encontrado
    """
    reg = Registro.query.get(id)
    if not reg:
        return jsonify({"error": "Registro no encontrado"}), 404

    db.session.delete(reg)
    db.session.commit()
    return "", 204
