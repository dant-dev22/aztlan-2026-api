"""
Lógica de negocio para registros.
"""
from schemas.registro import RegistroJuvenil, RegistroAdultosMasters
from models.registro import db, Registro
from utils.aztlan_id import generate_aztlan_id


def create_registro(
    payload: RegistroJuvenil | RegistroAdultosMasters,
) -> Registro:
    """Crea un registro y lo persiste. Genera id y aztlan_id."""
    aztlan_id = generate_aztlan_id()
    # Asegurar unicidad de aztlan_id (poco probable colisión)
    while Registro.query.filter_by(aztlan_id=aztlan_id).first() is not None:
        aztlan_id = generate_aztlan_id()

    r = Registro(
        aztlan_id=aztlan_id,
        tipo_registro=payload.tipo_registro,
        nombre_completo=payload.nombre_completo,
        email=payload.email,
        timestamp=payload.timestamp,
        sexo=getattr(payload, "sexo", None),
        cinta=getattr(payload, "cinta", None),
        nivel_experiencia=getattr(payload, "nivel_experiencia", None),
        categoria_edad=getattr(payload, "categoria_edad", None),
        categoria_peso=payload.categoria_peso,
        edad=getattr(payload, "edad", None),
        categoria_peso_tipo=getattr(payload, "categoria_peso_tipo", None),
    )
    db.session.add(r)
    db.session.commit()
    return r
