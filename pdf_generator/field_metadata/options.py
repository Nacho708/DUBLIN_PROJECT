"""
field_metadata/options.py
=========================

Catálogo de opciones reutilizables para campos de selección.

Este módulo NO contiene lógica ni conocimiento del dominio.
Todas las opciones son genéricas y pueden reutilizarse en
cualquier formulario.
"""

# ==========================================================
# BOOLEAN
# ==========================================================

YES_NO = [
    "Yes",
    "No"
]

YES_NO_UNKNOWN = [
    "Yes",
    "No",
    "Unknown"
]

TRUE_FALSE = [
    "True",
    "False"
]

ACTIVE_INACTIVE = [
    "Active",
    "Inactive"
]

ENABLED_DISABLED = [
    "Enabled",
    "Disabled"
]

PRESENT_ABSENT = [
    "Present",
    "Absent"
]

POSITIVE_NEGATIVE = [
    "Positive",
    "Negative"
]


# ==========================================================
# GENDER
# ==========================================================

MALE_FEMALE = [
    "Male",
    "Female"
]


# ==========================================================
# LATERALITY
# ==========================================================

LEFT_RIGHT = [
    "Left",
    "Right"
]

LEFT_RIGHT_BILATERAL = [
    "Left",
    "Right",
    "Bilateral"
]


# ==========================================================
# NORMALITY
# ==========================================================

NORMAL_ABNORMAL = [
    "Normal",
    "Abnormal"
]

NORMAL_ALTERED = [
    "Normal",
    "Altered"
]


# ==========================================================
# SEVERITY
# ==========================================================

LOW_MEDIUM_HIGH = [
    "Low",
    "Medium",
    "High"
]

NONE_MILD_MODERATE_SEVERE = [
    "None",
    "Mild",
    "Moderate",
    "Severe"
]

MILD_MODERATE_SEVERE = [
    "Mild",
    "Moderate",
    "Severe"
]


# ==========================================================
# FREQUENCY
# ==========================================================

NEVER_ALWAYS_4 = [
    "Never",
    "Occasionally",
    "Frequently",
    "Always"
]

NEVER_ALWAYS_5 = [
    "Never",
    "Rarely",
    "Sometimes",
    "Frequently",
    "Always"
]


# ==========================================================
# CLASSES
# ==========================================================

CLASS_1_3 = [
    "Class I",
    "Class II",
    "Class III"
]

CLASS_1_4 = [
    "Class I",
    "Class II",
    "Class III",
    "Class IV"
]

CLASS_1_5 = [
    "Class I",
    "Class II",
    "Class III",
    "Class IV",
    "Class V"
]


# ==========================================================
# GRADES
# ==========================================================

GRADE_0_3 = [
    0,
    1,
    2,
    3
]

GRADE_0_4 = [
    0,
    1,
    2,
    3,
    4
]

GRADE_1_3 = [
    1,
    2,
    3
]

GRADE_1_4 = [
    1,
    2,
    3,
    4
]

GRADE_1_5 = [
    1,
    2,
    3,
    4,
    5
]


# ==========================================================
# NUMERIC SCALES
# ==========================================================

SCALE_0_5 = list(range(6))

SCALE_0_10 = list(range(11))

SCALE_0_24 = list(range(25))

SCALE_0_28 = list(range(29))

SCALE_0_100 = list(range(101))


# ==========================================================
# RATINGS
# ==========================================================

RATING_1_5 = [
    1,
    2,
    3,
    4,
    5
]

RATING_1_10 = list(range(1, 11))


# ==========================================================
# STATUS
# ==========================================================

STATUS = [
    "Pending",
    "In Progress",
    "Completed"
]

STATUS_EXTENDED = [
    "Pending",
    "In Progress",
    "Completed",
    "Cancelled"
]


# ==========================================================
# BINARY CHOICE
# ==========================================================

PASS_FAIL = [
    "Pass",
    "Fail"
]

SUCCESS_FAILURE = [
    "Success",
    "Failure"
]


# ==========================================================
# TIME
# ==========================================================

DAY_NIGHT = [
    "Day",
    "Night"
]

AM_PM = [
    "AM",
    "PM"
]


# ==========================================================
# DIRECTION
# ==========================================================

HORIZONTAL_VERTICAL = [
    "Horizontal",
    "Vertical"
]

UP_DOWN = [
    "Up",
    "Down"
]

IN_OUT = [
    "In",
    "Out"
]


# ==========================================================
# ORDER
# ==========================================================

ASC_DESC = [
    "Ascending",
    "Descending"
]