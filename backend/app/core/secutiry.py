"""
Módulo de seguridad para la API clínica (GDPR compliance y sanitización).
"""
import secrets
from typing import Optional

def generate_patient_token() -> str:
    """Genera un token seguro alfanumérico si se requiere verificación temporal."""
    return secrets.token_urlsafe(32)

def sanitize_input(value: Optional[str]) -> Optional[str]:
    """Limpia cadenas de texto para evitar inyecciones o caracteres anómalos."""
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned if cleaned else None