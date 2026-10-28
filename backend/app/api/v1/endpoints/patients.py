# backend/app/api/v1/endpoints/patients.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.v1.deps import get_db
import app.db.models as models

router = APIRouter()

@router.get("/{patient_id}")
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    """Obtiene la información demográfica básica de un paciente."""
    patient = db.query(models.Patient).filter(models.Patient.Patient_ID == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Paciente con ID {patient_id} no encontrado"
        )
    
    demo = db.query(models.PatientDemographic).filter(models.PatientDemographic.Patient_ID == patient_id).first()
    
    return {
        "patient_id": patient.Patient_ID,
        "consultation_date": patient.Consultation_Date,
        "demographics": {
            "dob": demo.Date_of_Birth if demo else None,
            "age": demo.Age if demo else None,
            "gender": demo.Sex if demo else None,
            "bmi": demo.BMI if demo else None
        } if demo else None
    }