# backend/app/schemas/questionnaires.py
from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict

class QuestionnaireScoresBase(BaseModel):
    patient_id: str
    period: int
    period_date: date
    
    # ISI
    isi_fall_asleep: Optional[int] = None
    isi_stay_asleep: Optional[int] = None
    isi_waking_up_early: Optional[int] = None
    isi_sleep_pattern: Optional[int] = None
    isi_daily_functioning: Optional[int] = None
    isi_noticeble_sleep_problem: Optional[int] = None
    isi_worry_sleep_problem: Optional[int] = None

    # ESS
    ess_sitting_reading: Optional[int] = None
    ess_watching_tv: Optional[int] = None
    ess_sitting_inactive: Optional[int] = None
    ess_passenger: Optional[int] = None
    ess_lying_down: Optional[int] = None
    ess_sitting_talking: Optional[int] = None
    ess_sitting_no_alcohol: Optional[int] = None
    ess_car_traffic: Optional[int] = None

    # QoL
    qol_effort_tasks: Optional[int] = None
    qol_decrease_abilities_work: Optional[int] = None
    qol_difficulty_remembering: Optional[int] = None
    qol_difficulty_concentrating: Optional[int] = None
    qol_depression: Optional[int] = None
    qol_anxiety: Optional[int] = None
    qol_difficulty_activities: Optional[int] = None
    qol_relationships_guiltiness: Optional[int] = None
    qol_trouble_alert: Optional[int] = None
    qol_risk_daily_activities: Optional[int] = None

class QuestionnaireScoresResponse(QuestionnaireScoresBase):
    model_config = ConfigDict(from_attributes=True)