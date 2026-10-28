# app/db/models.py
from sqlalchemy import (
    Column, String, Integer, Float, Date, Boolean, 
    Text, ForeignKey, PrimaryKeyConstraint, Enum
)
from app.db.base_class import Base

class Patient(Base):
    __tablename__ = "patients"

    Patient_ID = Column(String(50), primary_key=True)
    Consultation_Date = Column(Date, nullable=False)
    Clinic_Number = Column(String(50), nullable=True)
    Referring_Physician = Column(String(100), nullable=True)
    Insurance_Type = Column(String(100), nullable=True)
    Payment_Type = Column(Enum('Insurance', 'Self-pay'), nullable=True)

class PatientDemographic(Base):
    __tablename__ = "patient_demographics"

    Patient_ID = Column(String(50), ForeignKey("patients.Patient_ID"), primary_key=True)
    Date_of_Birth = Column(Date, nullable=False)
    Age = Column(Integer, nullable=False)
    Sex = Column(Enum('Male', 'Female', 'Other'), nullable=False)
    Height_cm = Column(Float, nullable=False)
    Weight_kg = Column(Float, nullable=False)
    BMI = Column(Float, nullable=False)
    Tobacco_Use = Column(Integer, nullable=True)   # 1=Never, 2=Former, 3=Current
    Alcohol_Use = Column(Integer, nullable=True)   # 1=Never, 2=Occasional, 3=Regular
    Primary_Concern = Column(Text, nullable=True)  # Nuevo en V2

class MedicalHistory(Base):
    __tablename__ = "medical_history"

    Patient_ID = Column(String(50), ForeignKey("patients.Patient_ID"), primary_key=True)
    Hypertension = Column(Boolean, default=False)
    Diabetes = Column(Boolean, default=False)
    Heart_Disease = Column(Boolean, default=False)
    Stroke_TIA = Column(Boolean, default=False)
    Thyroid_Disorder = Column(Boolean, default=False)
    Depression = Column(Boolean, default=False)
    GERD = Column(Boolean, default=False)
    Cancer = Column(Boolean, default=False)
    Asthma_COPD = Column(Boolean, default=False)
    Other = Column(String(255), nullable=True)
    Medication = Column(String(255), nullable=True)
    Surgery = Column(String(255), nullable=True)
    Allergies = Column(Text, nullable=True)

class PatientSleepAssessment(Base):
    __tablename__ = "patients_sleep_assessment"

    Patient_ID = Column(String(50), ForeignKey("patients.Patient_ID"), nullable=False)
    Period = Column(Integer, nullable=False)
    Period_Date = Column(Date, nullable=False)

    # Preguntas de frecuencia (0=Never, 1=Occas, 2=Frequent)
    Sleep_Initiation = Column(Integer, nullable=True)
    Nighttime_Awakening = Column(Integer, nullable=True)
    Sleep_Maintenance_Difficulty = Column(Integer, nullable=True)
    Early_Morning_Awakening = Column(Integer, nullable=True)
    Nonrestorative_Sleep = Column(Integer, nullable=True)
    Daytime_Sleepiness = Column(Integer, nullable=True)
    Observed_Apnea = Column(Integer, nullable=True)
    Nocturia = Column(Integer, nullable=True)
    Morning_Headaches = Column(Integer, nullable=True)
    Bruxism = Column(Integer, nullable=True)
    Jawjoint_Pain = Column(Integer, nullable=True)  # Corregido typo 'Jawint_Pain'
    Sleep_Related_Distress = Column(Integer, nullable=True)
    
    # Nuevas preguntas en V2
    Snoring_Affects_Others = Column(Integer, nullable=True)
    Partner_Alert_Stop_Noise = Column(Integer, nullable=True)
    Acid_Reflux_Symptoms = Column(Integer, nullable=True)
    Jaw_Joint_Click = Column(Integer, nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint("Patient_ID", "Period"),
    )

class SnoringAssessment(Base):
    __tablename__ = "snoring_assessment"

    Patient_ID = Column(String(50), ForeignKey("patients.Patient_ID"), nullable=False)
    Period = Column(Integer, nullable=False)
    Period_Date = Column(Date, nullable=False)

    Snoring_Evolution = Column(Integer, nullable=True)
    Snoring_Frequency = Column(Integer, nullable=True)
    Snoring_Intensity = Column(Integer, nullable=True) # 0-10
    Snoring_Position = Column(String(50), nullable=True) # Back, Side, Any (Pregunta 19)
    Dry_Mouth = Column(Integer, nullable=True)
    Irritated_Throat = Column(Integer, nullable=True)
    Nasal_Congestion = Column(Integer, nullable=True)
    Tooth_Grinding = Column(Integer, nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint("Patient_ID", "Period"),
    )

class QuestionnaireScores(Base):
    __tablename__ = "questionnaire_scores"

    Patient_ID = Column(String(50), ForeignKey("patients.Patient_ID"), nullable=False)
    Period = Column(Integer, nullable=False)
    Period_Date = Column(Date, nullable=False)

    # ISI
    ISI_Fall_Asleep = Column(Integer, nullable=True)
    ISI_Stay_Asleep = Column(Integer, nullable=True)
    ISI_Waking_Up_Early = Column(Integer, nullable=True)
    ISI_Sleep_Pattern = Column(Integer, nullable=True)
    ISI_Daily_Functioning = Column(Integer, nullable=True)
    ISI_Noticeble_Sleep_Problem = Column(Integer, nullable=True)
    ISI_Worry_Sleep_Problem = Column(Integer, nullable=True)

    # ESS
    ESS_Sitting_Reading = Column(Integer, nullable=True)
    ESS_Watching_TV = Column(Integer, nullable=True)
    ESS_Sitting_Inactive = Column(Integer, nullable=True)
    ESS_Passenger = Column(Integer, nullable=True)
    ESS_Lying_Down = Column(Integer, nullable=True)
    ESS_Sitting_Talking = Column(Integer, nullable=True)
    ESS_Sitting_No_Alcohol = Column(Integer, nullable=True)
    ESS_Car_Traffic = Column(Integer, nullable=True)

    # QoL
    QoL_Effort_Tasks = Column(Integer, nullable=True)
    QoL_Decrease_Abilities_Work = Column(Integer, nullable=True)
    QoL_Difficulty_Remembering = Column(Integer, nullable=True)
    QoL_Difficulty_Concentrating = Column(Integer, nullable=True)
    QoL_Depression = Column(Integer, nullable=True)
    QoL_Anxiety = Column(Integer, nullable=True)
    QoL_Difficulty_Activities = Column(Integer, nullable=True)
    QoL_Relationships_Guiltiness = Column(Integer, nullable=True)
    QoL_Trouble_Alert = Column(Integer, nullable=True)
    QoL_Risk_Daily_Activities = Column(Integer, nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint("Patient_ID", "Period"),
    )