from fastapi import APIRouter
from app.models import PatientInput
from app.utils import calculate_age, calculate_bmi
from app.crud import insert_patient

router = APIRouter()

@router.post("/insert-patient")
def create_patient(data: PatientInput):
    age = calculate_age(data.date_of_birth)
    bmi = calculate_bmi(data.weight_kg, data.height_cm)

    insert_patient(data, age, bmi)

    return {"status": "ok"}