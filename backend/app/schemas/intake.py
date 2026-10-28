# app/schemas/intake.py
from datetime import date
from typing import Optional, Literal
from pydantic import BaseModel, Field

class IntakeFormPayload(BaseModel):
    # Identificación y Demografía
    patient_id: str = Field(..., max_length=50)
    consultation_date: date
    date_of_birth: date
    age: int = Field(..., ge=0, le=120)
    gender: Literal["Male", "Female", "Other"]
    height_cm: float = Field(..., gt=0)
    weight_kg: float = Field(..., gt=0)
    tobacco_use: Literal["Never", "Former", "Current"]
    alcohol_use: Literal["Never", "Occasional", "Regular"]
    primary_concern: Optional[str] = None

    # Medical History (checkboxes)
    hypertension: bool = False
    diabetes: bool = False
    heart_disease: bool = False
    stroke_tia: bool = False
    thyroid_disorder: bool = False
    depression: bool = False
    gerd: bool = False
    cancer: bool = False
    asthma_copd: bool = False
    other_medical: Optional[str] = None
    medications: Optional[str] = None
    surgery: Optional[str] = None
    allergies: Optional[str] = None

    # Síntomas de sueño (0=Never, 1=Occas, 2=Frequent)
    sleep_initiation: int = Field(0, ge=0, le=2)
    nighttime_awakening: int = Field(0, ge=0, le=2)
    sleep_maintenance_difficulty: int = Field(0, ge=0, le=2)
    early_morning_awakening: int = Field(0, ge=0, le=2)
    nonrestorative_sleep: int = Field(0, ge=0, le=2)
    daytime_sleepiness: int = Field(0, ge=0, le=2)
    observed_apnea: int = Field(0, ge=0, le=2)
    nocturia: int = Field(0, ge=0, le=2)
    morning_headaches: int = Field(0, ge=0, le=2)
    bruxism: int = Field(0, ge=0, le=2)
    jawjoint_pain: int = Field(0, ge=0, le=2)
    sleep_related_distress: int = Field(0, ge=0, le=2)
    snoring_affects_others: int = Field(0, ge=0, le=2)
    partner_alert_stop_noise: int = Field(0, ge=0, le=2)
    acid_reflux: int = Field(0, ge=0, le=2)
    jaw_joint_click: int = Field(0, ge=0, le=2)

    # Ronquido
    snoring_evolution: Optional[str] = None
    snoring_frequency: int = Field(0, ge=0, le=2)
    snoring_intensity: int = Field(0, ge=0, le=10)
    snoring_position: Optional[str] = None
    dry_mouth: int = Field(0, ge=0, le=2)
    irritated_throat: int = Field(0, ge=0, le=2)
    nasal_congestion: int = Field(0, ge=0, le=2)
    tooth_grinding: int = Field(0, ge=0, le=2)

    # Cuestionarios
    isi_scores: dict[str, int]  # Claves: fall_asleep, stay_asleep, waking_early, pattern, functioning, noticeble, worry
    ess_scores: dict[str, int]  # Claves: reading, tv, inactive, passenger, lying, talking, no_alcohol, traffic
    qol_scores: dict[str, int]  # 10 ítems (0 a 4)