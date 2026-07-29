"""
field_metadata/constants.py
===========================

Constantes globales utilizadas por el sistema de generación de
formularios PDF.

Este módulo NO contiene lógica.

Únicamente define constantes reutilizables por:

    - options.py
    - templates.py
    - metadata.py
    - pdf_builder.py

"""

from enum import StrEnum


# ==========================================================
# PDF CONTROL TYPES
# ==========================================================

class ControlType(StrEnum):
    TEXT = "text"
    TEXTAREA = "textarea"

    NUMBER = "number"
    INTEGER = "integer"
    DECIMAL = "decimal"

    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"

    CHECKBOX = "checkbox"
    RADIO = "radio"

    DROPDOWN = "dropdown"
    LISTBOX = "listbox"

    SIGNATURE = "signature"

    LABEL = "label"
    SECTION = "section"
    SEPARATOR = "separator"


# ==========================================================
# DATABASE TYPES
# ==========================================================

class DataType(StrEnum):
    STRING = "string"

    BOOLEAN = "boolean"

    INTEGER = "integer"

    FLOAT = "float"

    DATE = "date"

    DATETIME = "datetime"

    TIME = "time"


# ==========================================================
# ALIGNMENT
# ==========================================================

class Alignment(StrEnum):
    LEFT = "left"

    CENTER = "center"

    RIGHT = "right"


# ==========================================================
# TEXT TRANSFORMATION
# ==========================================================

class TextTransform(StrEnum):
    NONE = "none"

    UPPERCASE = "uppercase"

    LOWERCASE = "lowercase"

    TITLE = "title"


# ==========================================================
# VALIDATION TYPES
# ==========================================================

class ValidationType(StrEnum):
    NONE = "none"

    REQUIRED = "required"

    RANGE = "range"

    OPTIONS = "options"

    REGEX = "regex"

    LENGTH = "length"


# ==========================================================
# PDF FIELD STATE
# ==========================================================

class FieldState(StrEnum):
    VISIBLE = "visible"

    HIDDEN = "hidden"

    READ_ONLY = "read_only"

    DISABLED = "disabled"


# ==========================================================
# COMMON UNITS
# ==========================================================

class Unit(StrEnum):
    MILLIMETERS = "mm"

    CENTIMETERS = "cm"

    METERS = "m"

    KILOGRAMS = "kg"

    GRAMS = "g"

    BMI = "kg/m²"

    YEARS = "years"

    MONTHS = "months"

    DAYS = "days"

    HOURS = "hours"

    MINUTES = "minutes"

    SECONDS = "seconds"

    PERCENT = "%"


# ==========================================================
# NUMBER FORMAT
# ==========================================================

class NumberFormat(StrEnum):
    INTEGER = "integer"

    DECIMAL_1 = "decimal_1"

    DECIMAL_2 = "decimal_2"

    DECIMAL_3 = "decimal_3"


# ==========================================================
# DEFAULT PDF LAYOUT
# ==========================================================

DEFAULT_FONT = "Helvetica"

DEFAULT_FONT_SIZE = 10

DEFAULT_TITLE_SIZE = 16

DEFAULT_SECTION_SIZE = 13

DEFAULT_LABEL_SIZE = 10

DEFAULT_FIELD_WIDTH = 180

DEFAULT_FIELD_HEIGHT = 20

DEFAULT_TEXTAREA_HEIGHT = 70

DEFAULT_MARGIN = 40

DEFAULT_VERTICAL_SPACING = 8

DEFAULT_SECTION_SPACING = 20


# ==========================================================
# DEFAULT FIELD PROPERTIES
# ==========================================================

DEFAULT_REQUIRED = False

DEFAULT_VISIBLE = True

DEFAULT_READ_ONLY = False

DEFAULT_MULTILINE = False

DEFAULT_ALIGNMENT = Alignment.LEFT

DEFAULT_TRANSFORM = TextTransform.NONE

DEFAULT_VALIDATION = ValidationType.NONE

DEFAULT_STATE = FieldState.VISIBLE


# ==========================================================
# BOOLEAN VALUES
# ==========================================================

TRUE = True

FALSE = False


# ==========================================================
# SPECIAL VALUES
# ==========================================================

AUTO = "auto"

NONE = None

UNLIMITED = -1


# ==========================================================
# PDF SECTIONS
# ==========================================================

PATIENT_INFORMATION = "patient_information"

PATIENT_DEMOGRAPHICS = "patient_demographics"

PATIENT_SYMPTOMS = "patient_symptoms"

MEDICAL_HISTORY = "medical_history"

SLEEP_HISTORY = "sleep_history"

QUESTIONNAIRES = "questionnaires"

APNEA_QUESTIONNAIRE = "apnea_questionnaire"

SNORING_QUESTIONNAIRE = "snoring_questionnaire"

PHYSICAL_EXAMINATION = "physical_examination"

CBCT = "cbct"

TREATMENT = "treatment"

FOLLOW_UP = "follow_up"


# ==========================================================
# COMMON PROPERTY NAMES
# ==========================================================

CONTROL = "control"

LABEL = "label"

OPTIONS = "options"

UNIT = "unit"

DEFAULT = "default"

MIN = "min"

MAX = "max"

STEP = "step"

REQUIRED = "required"

MULTILINE = "multiline"

TOOLTIP = "tooltip"

PLACEHOLDER = "placeholder"

VALIDATION = "validation"

FORMAT = "format"

WIDTH = "width"

HEIGHT = "height"

DECIMALS = "decimals"

ALIGNMENT = "alignment"

STATE = "state"

TRANSFORM = "transform"

DATA_TYPE = "data_type"