"""
field_metadata/metadata.py
==========================

Registro de metadatos utilizado para asociar cada campo de la base
de datos con la plantilla que utilizará el generador de formularios.
"""

from .templates import *


# ==========================================================
# DEFAULT TEMPLATE
# ==========================================================

DEFAULT_TEMPLATE = TEXT_TEMPLATE


# ==========================================================
# COMMON FIELD GROUPS
# ==========================================================

PATIENT_ID = {
    "Patient_ID": READONLY_TEXT_TEMPLATE,
}

YES_NO_FIELDS = {
    "Family_History_OSA": YES_NO_TEMPLATE,
    "Tobacco_Use": YES_NO_TEMPLATE,
    "Alcohol_Use": YES_NO_TEMPLATE,
    "Caffeine_Use": YES_NO_TEMPLATE,
    "Shift_Work": YES_NO_TEMPLATE,

    "Snoring": YES_NO_TEMPLATE,
    "Witnessed_Apneas": YES_NO_TEMPLATE,
    "Nocturnal_Choking": YES_NO_TEMPLATE,
    "Insomnia": YES_NO_TEMPLATE,
    "Night_Awakenings": YES_NO_TEMPLATE,
    "Non_Restorative_Sleep": YES_NO_TEMPLATE,
    "Daytime_Sleepiness": YES_NO_TEMPLATE,
    "Nasal_Obstruction": YES_NO_TEMPLATE,
    "Dry_Mouth": YES_NO_TEMPLATE,
    "Morning_Headaches": YES_NO_TEMPLATE,
    "Jaw_Pain": YES_NO_TEMPLATE,
    "Teeth_Grinding": YES_NO_TEMPLATE,

    "Hypertension": YES_NO_TEMPLATE,
    "Diabetes": YES_NO_TEMPLATE,
    "Depression": YES_NO_TEMPLATE,
    "GERD": YES_NO_TEMPLATE,
    "Cancer": YES_NO_TEMPLATE,

    "Previous_Sleep_Study": YES_NO_TEMPLATE,
    "RLS": YES_NO_TEMPLATE,
    "Parasomnias": YES_NO_TEMPLATE,
    "CPAP_Use": YES_NO_TEMPLATE,
    "Sleep_Position": YES_NO_TEMPLATE,
    "MFT": YES_NO_TEMPLATE,
    "Maxillofacial": YES_NO_TEMPLATE,
    "ENT_Surgery": YES_NO_TEMPLATE,

    "Linea_Alba": YES_NO_TEMPLATE,
    "Torus": YES_NO_TEMPLATE,
    "Worn_Teeth": YES_NO_TEMPLATE,
    "Muscle_Tenderness": YES_NO_TEMPLATE,
    "Mouth_Breathing": YES_NO_TEMPLATE,

    "CPAP_Used": YES_NO_TEMPLATE,
    "Weight_Treatment": YES_NO_TEMPLATE,
    "Lifestyle_Modification": YES_NO_TEMPLATE,

    "Compliance": YES_NO_TEMPLATE,
    "Adverse_Effects": YES_NO_TEMPLATE,
}

GRADE_0_4_FIELDS = {
    "Observed_Apnea": GRADE_0_4_TEMPLATE,
    "Morning_Headaches": GRADE_0_4_TEMPLATE,
    "Nighttime_Awakening": GRADE_0_4_TEMPLATE,
    "Nocturia": GRADE_0_4_TEMPLATE,
    "Nonrestorative_Sleep": GRADE_0_4_TEMPLATE,
    "EDS": GRADE_0_4_TEMPLATE,

    "Snoring_Evolution": GRADE_0_4_TEMPLATE,
    "Snoring_Frequency": GRADE_0_4_TEMPLATE,
    "Snoring_Intensity": GRADE_0_4_TEMPLATE,
    "Dry_Mouth": GRADE_0_4_TEMPLATE,
    "Irritated_Throat": GRADE_0_4_TEMPLATE,
    "Nasal_Congestion": GRADE_0_4_TEMPLATE,
    "Tooth_Grinding": GRADE_0_4_TEMPLATE,

    "Tonsil_Size": GRADE_0_4_TEMPLATE,
    "Friedman_Tongue": GRADE_0_4_TEMPLATE,
    "Uvula_Elongation": GRADE_0_4_TEMPLATE,
    "Lingual_Frenulum": GRADE_0_4_TEMPLATE,
    "Jaw_Relation": GRADE_0_4_TEMPLATE,
    "Facial_Profile": GRADE_0_4_TEMPLATE,
    "Joint_Sounds": GRADE_0_4_TEMPLATE,
}


# ==========================================================
# FIELD METADATA
# ==========================================================

FIELD_METADATA = {

    "patient_demographics": {

        **PATIENT_ID,

        "Date_of_Birth": DATE_TEMPLATE,
        "Age": INTEGER_TEMPLATE,
        "Sex": MALE_FEMALE_TEMPLATE,

        "Height_cm": DECIMAL_1_TEMPLATE,
        "Weight_kg": DECIMAL_1_TEMPLATE,
        "BMI": DECIMAL_2_TEMPLATE,
        "Neck_Circumference_cm": DECIMAL_1_TEMPLATE,

        "Family_History_OSA": YES_NO_TEMPLATE,
        "Tobacco_Use": YES_NO_TEMPLATE,
        "Alcohol_Use": YES_NO_TEMPLATE,
        "Caffeine_Use": YES_NO_TEMPLATE,
        "Shift_Work": YES_NO_TEMPLATE,
    },

    "patients": {

        **PATIENT_ID,

        "Consultation_Date": DATE_TEMPLATE,
        "Clinic_Number": TEXT_TEMPLATE,
        "Referring_Physician": TEXT_TEMPLATE,
        "Insurance_Type": TEXT_TEMPLATE,
        "Payment_Type": TEXT_TEMPLATE,
    },

    "patient_symptoms": {

        **PATIENT_ID,

        "Snoring": YES_NO_TEMPLATE,
        "Witnessed_Apneas": YES_NO_TEMPLATE,
        "Nocturnal_Choking": YES_NO_TEMPLATE,
        "Insomnia": YES_NO_TEMPLATE,
        "Night_Awakenings": YES_NO_TEMPLATE,
        "Non_Restorative_Sleep": YES_NO_TEMPLATE,
        "Daytime_Sleepiness": YES_NO_TEMPLATE,
        "Nasal_Obstruction": YES_NO_TEMPLATE,
        "Dry_Mouth": YES_NO_TEMPLATE,
        "Morning_Headaches": YES_NO_TEMPLATE,
        "Jaw_Pain": YES_NO_TEMPLATE,
        "Teeth_Grinding": YES_NO_TEMPLATE,
    },

    "medical_history": {

        **PATIENT_ID,

        "Hypertension": YES_NO_TEMPLATE,
        "Diabetes": YES_NO_TEMPLATE,
        "Depression": YES_NO_TEMPLATE,
        "GERD": YES_NO_TEMPLATE,
        "Cancer": YES_NO_TEMPLATE,

        "Medication": TEXTAREA_TEMPLATE,
        "Surgery": TEXTAREA_TEMPLATE,
        "Allergies": TEXTAREA_TEMPLATE,
    },

    "sleep_history": {

        **PATIENT_ID,

        "Previous_Sleep_Study": YES_NO_TEMPLATE,
        "RLS": YES_NO_TEMPLATE,
        "Insomnia": YES_NO_TEMPLATE,
        "Parasomnias": YES_NO_TEMPLATE,
        "CPAP_Use": YES_NO_TEMPLATE,

        "Sleep_Position": YES_NO_TEMPLATE,
        "MFT": YES_NO_TEMPLATE,
        "Maxillofacial": YES_NO_TEMPLATE,
        "ENT_Surgery": YES_NO_TEMPLATE,

        "Medication_Sleep": TEXTAREA_TEMPLATE,
    },

    "questionnaire_scores": {

        **PATIENT_ID,

        "Epworth_Score": INTEGER_TEMPLATE,
        "ISI_Score": INTEGER_TEMPLATE,

        "QoL_Score": DECIMAL_2_TEMPLATE,
        "SnoreLab_Score": DECIMAL_2_TEMPLATE,
        "SnoreLab_Epic": DECIMAL_2_TEMPLATE,
    },

    "sleep_symptom_frequency": {

        **PATIENT_ID,

        **GRADE_0_4_FIELDS,
    },

    "snoring_assessment": {

        **PATIENT_ID,

        "Snoring_Evolution": GRADE_0_4_TEMPLATE,
        "Snoring_Frequency": GRADE_0_4_TEMPLATE,
        "Snoring_Intensity": GRADE_0_4_TEMPLATE,
        "Dry_Mouth": GRADE_0_4_TEMPLATE,
        "Irritated_Throat": GRADE_0_4_TEMPLATE,
        "Nasal_Congestion": GRADE_0_4_TEMPLATE,
        "Tooth_Grinding": GRADE_0_4_TEMPLATE,
    },

    "physical_exam": {

        **PATIENT_ID,

        "Tonsil_Size": GRADE_0_4_TEMPLATE,
        "Friedman_Tongue": GRADE_0_4_TEMPLATE,
        "Uvula_Elongation": GRADE_0_4_TEMPLATE,
        "Lingual_Frenulum": GRADE_0_4_TEMPLATE,

        "Dental_Status": TEXTAREA_TEMPLATE,
        "Dental_Arch": TEXTAREA_TEMPLATE,

        "Jaw_Relation": GRADE_0_4_TEMPLATE,
        "Facial_Profile": GRADE_0_4_TEMPLATE,

        "ROM_Vertical": DECIMAL_2_TEMPLATE,
        "ROM_AP": DECIMAL_2_TEMPLATE,

        "GeorgeG_Max_Retruison": DECIMAL_2_TEMPLATE,
        "GeorgeG_Max_Protrusion": DECIMAL_2_TEMPLATE,

        "Linea_Alba": YES_NO_TEMPLATE,
        "Torus": YES_NO_TEMPLATE,
        "Worn_Teeth": YES_NO_TEMPLATE,
        "Muscle_Tenderness": YES_NO_TEMPLATE,
        "Joint_Sounds": GRADE_0_4_TEMPLATE,
        "Mouth_Breathing": YES_NO_TEMPLATE,
    },

    "sleep_study": {

        **PATIENT_ID,

        "AHI": DECIMAL_2_TEMPLATE,
        "AI": DECIMAL_2_TEMPLATE,
        "Supine_AHI": DECIMAL_2_TEMPLATE,
        "Time_Supine": DECIMAL_2_TEMPLATE,
        "Hypoxic_Burden": DECIMAL_2_TEMPLATE,
        "SaO2_Min": DECIMAL_2_TEMPLATE,
        "SaO2_Mean": DECIMAL_2_TEMPLATE,
        "CT90": DECIMAL_2_TEMPLATE,
        "Total_Sleep_Time": DECIMAL_2_TEMPLATE,
    },

    "cbct_measurements": {

        **PATIENT_ID,

        "CBCT_AP": DECIMAL_2_TEMPLATE,
        "CBCT_RL": DECIMAL_2_TEMPLATE,
        "CBCT_CSA": DECIMAL_2_TEMPLATE,
        "CBCT_SoftPalate_Length": DECIMAL_2_TEMPLATE,
        "CBCT_SoftPalate_Width": DECIMAL_2_TEMPLATE,
    },

    "treatment": {

        **PATIENT_ID,

        "Device_Type": TEXT_TEMPLATE,

        "Protrusion_Setting": DECIMAL_2_TEMPLATE,
        "Vertical_Setting": DECIMAL_2_TEMPLATE,

        "CPAP_Used": YES_NO_TEMPLATE,

        "Positional_Device": TEXT_TEMPLATE,

        "Weight_Treatment": YES_NO_TEMPLATE,
        "Lifestyle_Modification": YES_NO_TEMPLATE,
    },

    "followup": {

        **PATIENT_ID,

        "Followup_Date": DATE_TEMPLATE,

        "Followup_AHI": DECIMAL_2_TEMPLATE,

        "Compliance": YES_NO_TEMPLATE,

        "QoL_Score": DECIMAL_2_TEMPLATE,

        "Adverse_Effects": YES_NO_TEMPLATE,
    },
}


# ==========================================================
# API
# ==========================================================

class FieldMetadata:

    def __init__(self):
        self._metadata = FIELD_METADATA

    def get(self, table_name: str, field_name: str):

        return (
            self._metadata
            .get(table_name, {})
            .get(field_name, DEFAULT_TEMPLATE)
        )

    def get_table(self, table_name: str):
        return self._metadata.get(table_name, {})

    def has_table(self, table_name: str) -> bool:
        return table_name in self._metadata

    def has_field(self, table_name: str, field_name: str) -> bool:
        return field_name in self._metadata.get(table_name, {})

    def tables(self):
        return self._metadata.keys()

    def fields(self, table_name: str):
        return self._metadata.get(table_name, {}).keys()

    