"""
field_metadata/templates.py
===========================

Plantillas reutilizables para la generación automática
de formularios PDF.

Una plantilla define el comportamiento de un campo, no el
nombre del campo.

Este módulo NO contiene lógica específica del dominio.
"""

from dataclasses import dataclass, field, replace
from typing import Any

from . import options
from .constants import (
    Alignment,
    ControlType,
    DataType,
    FieldState,
    NumberFormat,
    TextTransform,
    ValidationType,
)


# ==========================================================
# FIELD TEMPLATE
# ==========================================================

@dataclass(frozen=True, slots=True)
class FieldTemplate:
    """Representa una plantilla reutilizable de un campo PDF."""

    # Tipo de control
    control: ControlType

    # Tipo de dato
    data_type: DataType

    # Etiqueta por defecto
    label: str | None = None

    # Lista de opciones
    options: list[Any] | None = None

    # Unidad
    unit: str | None = None

    # Valor por defecto
    default: Any = None

    # Validación
    validation: ValidationType = ValidationType.NONE

    # Restricciones numéricas
    minimum: float | None = None
    maximum: float | None = None

    # Formato
    number_format: NumberFormat | None = None
    decimals: int | None = None

    # Comportamiento
    required: bool = False
    multiline: bool = False
    read_only: bool = False

    # Estado
    visible: bool = True
    state: FieldState = FieldState.VISIBLE

    # Apariencia
    alignment: Alignment = Alignment.LEFT
    transform: TextTransform = TextTransform.NONE

    # Ayuda
    tooltip: str | None = None
    placeholder: str | None = None

    # Tamaño
    width: int | None = None
    height: int | None = None

    # Propiedades adicionales
    extra: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# HELPERS
# ==========================================================

def derive(template: FieldTemplate, **changes) -> FieldTemplate:
    """
    Crea una nueva plantilla modificando únicamente
    las propiedades indicadas.
    """
    return replace(template, **changes)


# ==========================================================
# BASE TEMPLATES
# ==========================================================

TEXT_TEMPLATE = FieldTemplate(
    control=ControlType.TEXT,
    data_type=DataType.STRING,
)

TEXTAREA_TEMPLATE = derive(
    TEXT_TEMPLATE,
    control=ControlType.TEXTAREA,
    multiline=True,
)

NUMBER_TEMPLATE = FieldTemplate(
    control=ControlType.NUMBER,
    data_type=DataType.FLOAT,
)

INTEGER_TEMPLATE = derive(
    NUMBER_TEMPLATE,
    data_type=DataType.INTEGER,
    number_format=NumberFormat.INTEGER,
    decimals=0,
)

DATE_TEMPLATE = FieldTemplate(
    control=ControlType.DATE,
    data_type=DataType.DATE,
)

TIME_TEMPLATE = FieldTemplate(
    control=ControlType.TIME,
    data_type=DataType.TIME,
)

DATETIME_TEMPLATE = FieldTemplate(
    control=ControlType.DATETIME,
    data_type=DataType.DATETIME,
)

CHECKBOX_TEMPLATE = FieldTemplate(
    control=ControlType.CHECKBOX,
    data_type=DataType.BOOLEAN,
)

RADIO_TEMPLATE = FieldTemplate(
    control=ControlType.RADIO,
    data_type=DataType.STRING,
)

DROPDOWN_TEMPLATE = FieldTemplate(
    control=ControlType.DROPDOWN,
    data_type=DataType.STRING,
)

LISTBOX_TEMPLATE = FieldTemplate(
    control=ControlType.LISTBOX,
    data_type=DataType.STRING,
)


# ==========================================================
# OPTION TEMPLATES
# ==========================================================

YES_NO_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.YES_NO,
)

YES_NO_UNKNOWN_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.YES_NO_UNKNOWN,
)

TRUE_FALSE_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.TRUE_FALSE,
)

MALE_FEMALE_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.MALE_FEMALE,
)

LEFT_RIGHT_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.LEFT_RIGHT,
)

LEFT_RIGHT_BILATERAL_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.LEFT_RIGHT_BILATERAL,
)

FREQUENCY_4_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.NEVER_ALWAYS_4,
)

FREQUENCY_5_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.NEVER_ALWAYS_5,
)

CLASS_1_3_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.CLASS_1_3,
)

CLASS_1_4_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.CLASS_1_4,
)

CLASS_1_5_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.CLASS_1_5,
)

GRADE_0_3_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.GRADE_0_3,
)

GRADE_0_4_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.GRADE_0_4,
)

GRADE_1_3_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.GRADE_1_3,
)

GRADE_1_4_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.GRADE_1_4,
)

GRADE_1_5_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.GRADE_1_5,
)

SCALE_0_5_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.SCALE_0_5,
)

SCALE_0_10_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.SCALE_0_10,
)

SCALE_0_24_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.SCALE_0_24,
)

SCALE_0_28_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.SCALE_0_28,
)

SCALE_0_100_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    options=options.SCALE_0_100,
)


# ==========================================================
# NUMERIC TEMPLATES
# ==========================================================

DECIMAL_1_TEMPLATE = derive(
    NUMBER_TEMPLATE,
    decimals=1,
    number_format=NumberFormat.DECIMAL_1,
)

DECIMAL_2_TEMPLATE = derive(
    NUMBER_TEMPLATE,
    decimals=2,
    number_format=NumberFormat.DECIMAL_2,
)

DECIMAL_3_TEMPLATE = derive(
    NUMBER_TEMPLATE,
    decimals=3,
    number_format=NumberFormat.DECIMAL_3,
)


# ==========================================================
# REQUIRED TEMPLATES
# ==========================================================

REQUIRED_TEXT_TEMPLATE = derive(
    TEXT_TEMPLATE,
    required=True,
)

REQUIRED_TEXTAREA_TEMPLATE = derive(
    TEXTAREA_TEMPLATE,
    required=True,
)

REQUIRED_NUMBER_TEMPLATE = derive(
    NUMBER_TEMPLATE,
    required=True,
)

REQUIRED_INTEGER_TEMPLATE = derive(
    INTEGER_TEMPLATE,
    required=True,
)

REQUIRED_DATE_TEMPLATE = derive(
    DATE_TEMPLATE,
    required=True,
)

REQUIRED_DROPDOWN_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    required=True,
)


# ==========================================================
# READ ONLY TEMPLATES
# ==========================================================

READONLY_TEXT_TEMPLATE = derive(
    TEXT_TEMPLATE,
    read_only=True,
)

READONLY_NUMBER_TEMPLATE = derive(
    NUMBER_TEMPLATE,
    read_only=True,
)

READONLY_DATE_TEMPLATE = derive(
    DATE_TEMPLATE,
    read_only=True,
)

READONLY_DROPDOWN_TEMPLATE = derive(
    DROPDOWN_TEMPLATE,
    read_only=True,
)