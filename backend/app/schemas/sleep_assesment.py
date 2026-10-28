# backend/app/schemas/sleep_assessment.py
from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict

class SleepAssessmentBase(BaseModel):
    patient_id: str
    period: int
    period_date: date
    sleep_initiation: Optional[int] = None
    nighttime_awakening: Optional[int] = None
    sleep_maintenance_difficulty: Optional[int] = None
    early_morning_awakening: Optional[int] = None
    nonrestorative_sleep: Optional[int] = None
    daytime_sleepiness: Optional[int] = None
    observed_apnea: Optional[int] = None
    nocturia: Optional[int] = None
    morning_headaches: Optional[int] = None
    bruxism: Optional[int] = None
    jawjoint_pain: Optional[int] = None
    sleep_related_distress: Optional[int] = None
    snoring_affects_others: Optional[int] = None
    partner_alert_stop_noise: Optional[int] = None
    acid_reflux_symptoms: Optional[int] = None
    jaw_joint_click: Optional[int] = None

class SleepAssessmentResponse(SleepAssessmentBase):
    model_config = ConfigDict(from_attributes=True)