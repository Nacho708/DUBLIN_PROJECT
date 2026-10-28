# backend/app/schemas/patient.py
from datetime import date
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict

class PatientBase(BaseModel):
    patient_id: str
    consultation_date: date
    clinic_number: Optional[str] = None
    referring_physician: Optional[str] = None
    insurance_type: Optional[str] = None
    payment_type: Optional[Literal["Insurance", "Self-pay"]] = None

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    model_config = ConfigDict(from_attributes=True)