"""
pdf_builder/__init__.py
========================

API pública del paquete pdf_builder.

Permite importar las clases, constantes y plantillas más utilizadas
sin necesidad de conocer la estructura interna del paquete.
"""

from .constants import *
from .options import *
from .templates import *
from .metadata import (
    DEFAULT_TEMPLATE,
    FIELD_METADATA,
    FieldMetadata,
)

__all__ = [
    "DEFAULT_TEMPLATE",
    "FIELD_METADATA",
    "FieldMetadata",
]