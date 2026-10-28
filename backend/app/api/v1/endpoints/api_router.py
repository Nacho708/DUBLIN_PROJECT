# backend/app/api/v1/endpoints/api_router.py
from fastapi import APIRouter
from app.api.v1.endpoints import intake, patients

api_router = APIRouter()

# Prefijo final: /api/v1/intake
api_router.include_router(intake.router, prefix="/intake", tags=["Intake Form"])

# Prefijo final: /api/v1/patients
api_router.include_router(patients.router, prefix="/patients", tags=["Patients"])