"""
Genera aztlan_id único: prefijo "azt" + 3 caracteres aleatorios (6 caracteres total).
"""
import random
import string


def generate_aztlan_id() -> str:
    """Formato: azt + 3 caracteres alfanuméricos. Ej: azt1b2, aztx9k."""
    rand = "".join(random.choices(string.ascii_lowercase + string.digits, k=3))
    return f"azt{rand}"
