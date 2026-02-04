"""
Genera aztlan_id único: AZT + timestamp + string aleatorio.
"""
import random
import string
import time


def generate_aztlan_id() -> str:
    """Formato: AZT + timestamp (ms) + 6 caracteres alfanuméricos."""
    ts = str(int(time.time() * 1000))
    rand = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"AZT{ts}{rand}"
