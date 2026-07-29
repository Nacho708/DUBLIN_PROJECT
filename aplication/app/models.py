from pydantic import BaseModel

class PatientInput(BaseModel):
    date_of_birth: str
    sex: str
    height_cm: float
    weight_kg: float
    neck_circumference_cm: float
    family_history_osa: int
    tobacco_use: int
    alcohol_use: int
    caffeine_use: int
    shift_work: int