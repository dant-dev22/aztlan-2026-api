"""
Genera aztlan_id único de máximo 6 caracteres alfanuméricos.
"""
import random
import string


def generate_aztlan_id() -> str:
    """Formato: 6 caracteres alfanuméricos (mayúsculas + dígitos). Ej: A1B2C3."""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
