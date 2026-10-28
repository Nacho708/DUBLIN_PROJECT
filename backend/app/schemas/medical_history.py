# backend/app/schemas/medical_history.py
from typing import Optional
from pydantic import BaseModel, ConfigDict

class MedicalHistoryBase(BaseModel):
    hypertension: bool = False
    diabetes: bool = False
    heart_disease: bool = False
    stroke_tia: bool = False
    thyroid_disorder: bool = False
    depression: bool = False
    gerd: bool = False
    cancer: bool = False
    asthma_copd: bool = False
    other: Optional[str] = None
    medication: Optional[str] = None
    surgery: Optional[str] = None
    allergies: Optional[str] = None

class MedicalHistoryResponse(MedicalHistoryBase):
    patient_id: str
    model_config = ConfigDict(from_attributes=True)