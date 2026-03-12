# Carga de librerías y paquetes necesarios
from functools import reduce
import pandas as pd
import numpy as np
import os

def create_patients_table(cursor):

    query = """
    CREATE TABLE IF NOT EXISTS patients (
        Patient_ID VARCHAR(50) PRIMARY KEY,
        Consultation_Date DATE,
        Clinic_Number VARCHAR(50),
        Referring_Physician VARCHAR(100),
        Insurance_Type VARCHAR(100),
        Payment_Type ENUM('Insurance','Self-pay')
    )
    """

    cursor.execute(query)


def create_patient_demographics_table(cursor):

    query = """
    CREATE TABLE IF NOT EXISTS patient_demographics (
        Patient_ID VARCHAR(50),
        Date_of_Birth DATE,
        Age INT,
        Sex ENUM('Male','Female','Other'),
        Height_cm FLOAT,
        Weight_kg FLOAT,
        BMI FLOAT,
        Neck_Circumference_cm FLOAT,
        Family_History_OSA BOOLEAN,
        Tobacco_Use BOOLEAN,
        Alcohol_Use BOOLEAN,
        Caffeine_Use BOOLEAN,
        Shift_Work BOOLEAN,
        FOREIGN KEY (Patient_ID) REFERENCES patients(Patient_ID)
    )
    """

    cursor.execute(query)


def create_patient_symptoms_table(cursor):

    query = """
    CREATE TABLE IF NOT EXISTS patient_symptoms (
        Patient_ID VARCHAR(50),
        Snoring BOOLEAN,
        Witnessed_Apneas BOOLEAN,
        Nocturnal_Choking BOOLEAN,
        Insomnia BOOLEAN,
        Night_Awakenings BOOLEAN,
        Non_Restorative_Sleep BOOLEAN,
        Daytime_Sleepiness BOOLEAN,
        Nasal_Obstruction BOOLEAN,
        Dry_Mouth BOOLEAN,
        Morning_Headaches BOOLEAN,
        Jaw_Pain BOOLEAN,
        Teeth_Grinding BOOLEAN,
        FOREIGN KEY (Patient_ID) REFERENCES patients(Patient_ID)
    )
    """

    cursor.execute(query)


def create_medical_history_table(cursor):

    query = """
    CREATE TABLE IF NOT EXISTS medical_history (

        Patient_ID VARCHAR(50),
        Hypertension BOOLEAN,
        Diabetes BOOLEAN,
        Depression BOOLEAN,
        GERD BOOLEAN,
        Cancer BOOLEAN,
        Medication VARCHAR(255),
        Surgery VARCHAR(255),
        Allergies TEXT,
        FOREIGN KEY (Patient_ID) REFERENCES patients(Patient_ID)
    )
    """

    cursor.execute(query)


def create_sleep_history_table(cursor):

    query = """
    CREATE TABLE IF NOT EXISTS sleep_history (

        Patient_ID VARCHAR(50),
        Previous_Sleep_Study BOOLEAN,
        RLS BOOLEAN,
        Insomnia BOOLEAN,
        Parasomnias BOOLEAN,
        CPAP_Use BOOLEAN,
        Sleep_Position BOOLEAN,
        MFT BOOLEAN,
        Maxillofacial BOOLEAN,
        ENT_Surgery BOOLEAN,
        Medication_Sleep VARCHAR(255),
        FOREIGN KEY (Patient_ID) REFERENCES patients(Patient_ID)
    )
    """

    cursor.execute(query)


def create_questionnaire_scores_table(cursor):

    query = """
    CREATE TABLE IF NOT EXISTS questionnaire_scores (

        Patient_ID VARCHAR(50),
        Epworth_Score INT,
        ISI_Score INT,
        QoL_Score FLOAT,
        SnoreLab_Score FLOAT,
        SnoreLab_Epic FLOAT,
        FOREIGN KEY (Patient_ID) REFERENCES patients(Patient_ID)
    )
    """

    cursor.execute(query)

def create_sleep_symptom_frequency_table(cursor):

    query = """
    CREATE TABLE IF NOT EXISTS sleep_symptom_frequency (

        Patient_ID VARCHAR(50),
        Observed_Apnea TINYINT,
        Morning_Headaches TINYINT,
        Nighttime_Awakening TINYINT,
        Nocturia TINYINT,
        Nonrestorative_Sleep TINYINT,
        EDS TINYINT,
        FOREIGN KEY (Patient_ID) REFERENCES patients(Patient_ID)
    )
    """

    cursor.execute(query)

def create_snoring_assessment_table(cursor):

    query = """
    CREATE TABLE IF NOT EXISTS snoring_assessment (

        Patient_ID VARCHAR(50),
        Snoring_Evolution TINYINT,
        Snoring_Frequency TINYINT,
        Snoring_Intensity TINYINT,
        Dry_Mouth TINYINT,
        Irritated_Throat TINYINT,
        Nasal_Congestion TINYINT,
        Tooth_Grinding TINYINT,
        FOREIGN KEY (Patient_ID) REFERENCES patients(Patient_ID)
    )
    """

    cursor.execute(query)

def create_physical_exam_table(cursor):

    query = """
    CREATE TABLE IF NOT EXISTS physical_exam (

        Patient_ID VARCHAR(50),
        Tonsil_Size TINYINT,
        Friedman_Tongue TINYINT,
        Uvula_Elongation TINYINT,
        Lingual_Frenulum TINYINT,
        Dental_Status TEXT,
        Dental_Arch TEXT,
        Jaw_Relation TINYINT,
        Facial_Profile TINYINT,
        ROM_Vertical FLOAT,
        ROM_AP FLOAT,
        GeorgeG_Max_Retruison FLOAT,
        GeorgeG_Max_Protrusion FLOAT,
        Linea_Alba BOOLEAN,
        Torus BOOLEAN,
        Worn_Teeth BOOLEAN,
        Muscle_Tenderness BOOLEAN,
        Joint_Sounds TINYINT,
        Mouth_Breathing BOOLEAN,
        FOREIGN KEY (Patient_ID) REFERENCES patients(Patient_ID)
    )
    """

    cursor.execute(query)

def create_sleep_study_table(cursor):

    query = """
    CREATE TABLE IF NOT EXISTS sleep_study (

        Patient_ID VARCHAR(50),
        AHI DECIMAL(5,2),
        AI DECIMAL(5,2),
        Supine_AHI DECIMAL(5,2),
        Time_Supine DECIMAL(5,2),
        Hypoxic_Burden DECIMAL(6,2),
        SaO2_Min DECIMAL(5,2),
        SaO2_Mean DECIMAL(5,2),
        CT90 DECIMAL(5,2),
        Total_Sleep_Time DECIMAL(6,2),
        FOREIGN KEY (Patient_ID) REFERENCES patients(Patient_ID)
    )
    """

    cursor.execute(query)


def create_cbct_measurements_table(cursor):

    query = """
    CREATE TABLE IF NOT EXISTS cbct_measurements (

        Patient_ID VARCHAR(50),
        CBCT_AP DECIMAL(6,2),
        CBCT_RL DECIMAL(6,2),
        CBCT_CSA DECIMAL(8,2),
        CBCT_SoftPalate_Length DECIMAL(6,2),
        CBCT_SoftPalate_Width DECIMAL(6,2),
        FOREIGN KEY (Patient_ID) REFERENCES patients(Patient_ID)
    )
    """

    cursor.execute(query)

def create_treatment_table(cursor):

    query = """
    CREATE TABLE IF NOT EXISTS treatment (

        Patient_ID VARCHAR(50),
        Device_Type VARCHAR(100),
        Protrusion_Setting DECIMAL(5,2),
        Vertical_Setting DECIMAL(5,2),
        CPAP_Used BOOLEAN,
        Positional_Device VARCHAR(100),
        Weight_Treatment BOOLEAN,
        Lifestyle_Modification BOOLEAN,
        FOREIGN KEY (Patient_ID) REFERENCES patients(Patient_ID)
    )
    """

    cursor.execute(query)


def create_followup_table(cursor):

    query = """
    CREATE TABLE IF NOT EXISTS followup (

        Patient_ID VARCHAR(50),
        Followup_Date DATE,
        Followup_AHI DECIMAL(5,2),
        Compliance BOOLEAN,
        QoL_Score FLOAT,
        Adverse_Effects BOOLEAN,
        FOREIGN KEY (Patient_ID) REFERENCES patients(Patient_ID)
    )
    """

    cursor.execute(query)

def create_all_tables(connection):

    cursor = connection.cursor()

    create_patients_table(cursor)
    create_patient_demographics_table(cursor)
    create_patient_symptoms_table(cursor)
    create_medical_history_table(cursor)
    create_sleep_history_table(cursor)
    create_questionnaire_scores_table(cursor)
    create_sleep_symptom_frequency_table(cursor)
    create_snoring_assessment_table(cursor)
    create_physical_exam_table(cursor)
    create_sleep_study_table(cursor)
    create_cbct_measurements_table(cursor)
    create_treatment_table(cursor)
    create_followup_table(cursor)

    connection.commit()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    print("\nTables currently in database:\n")

    for i, table in enumerate(tables, start=1):
        print(f"{i}. {table[0]}")

    print(f"\nTotal tables: {len(tables)}")

    cursor.close()

    print("All tables created successfully.")


