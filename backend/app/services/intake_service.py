# backend/app/services/intake_service.py
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.schemas.intake import IntakeFormPayload
from app.services.metrics import calculate_bmi, TOBACCO_MAP, ALCOHOL_MAP, SNORING_EVOLUTION_MAP
import app.db.models as models

def get_or_create_period(db: Session, table_name: str, patient_id: str, period_date) -> int:
    """
    Reutiliza la lógica de visitas:
    - Si ya existe un registro en la misma fecha para este paciente, reutiliza el Period existente.
    - Si es una nueva fecha, incrementa el Period más alto en +1 (comenzando en 0).
    """
    query_exist = text(
        f"SELECT Period FROM {table_name} "
        f"WHERE Patient_ID = :pid AND Period_Date = :pdate LIMIT 1"
    )
    existing = db.execute(query_exist, {"pid": patient_id, "pdate": period_date}).scalar_one_or_none()
    if existing is not None:
        return existing

    query_next = text(
        f"SELECT COALESCE(MAX(Period), -1) + 1 FROM {table_name} WHERE Patient_ID = :pid"
    )
    return db.execute(query_next, {"pid": patient_id}).scalar_one()

def process_intake_form(payload: IntakeFormPayload, db: Session) -> dict:
    """Procesa e inserta atómicamente la totalidad del formulario V2 en MySQL."""
    try:
        # 1. Base Patient
        patient = models.Patient(
            Patient_ID=payload.patient_id,
            Consultation_Date=payload.consultation_date
        )
        db.merge(patient)

        # -------------------------------------------------------------
        # FORZAR A MYSQL A REGISTRAR EL PADRE ANTES DE LAS TABLAS DEPENDIENTES
        # -------------------------------------------------------------
        db.flush()

        # 2. Patient Demographics
        bmi = calculate_bmi(payload.height_cm, payload.weight_kg)
        demographics = models.PatientDemographic(
            Patient_ID=payload.patient_id,
            Date_of_Birth=payload.date_of_birth,
            Age=payload.age,
            Sex=payload.gender,
            Height_cm=payload.height_cm,
            Weight_kg=payload.weight_kg,
            BMI=bmi if bmi is not None else 0.0,
            Tobacco_Use=TOBACCO_MAP.get(payload.tobacco_use),
            Alcohol_Use=ALCOHOL_MAP.get(payload.alcohol_use),
            Primary_Concern=payload.primary_concern
        )
        db.merge(demographics)

        # 3. Medical History
        history = models.MedicalHistory(
            Patient_ID=payload.patient_id,
            Hypertension=payload.hypertension,
            Diabetes=payload.diabetes,
            Heart_Disease=payload.heart_disease,
            Stroke_TIA=payload.stroke_tia,
            Thyroid_Disorder=payload.thyroid_disorder,
            Depression=payload.depression,
            GERD=payload.gerd,
            Cancer=payload.cancer,
            Asthma_COPD=payload.asthma_copd,
            Other=payload.other_medical,
            Medication=payload.medications,
            Surgery=payload.surgery,
            Allergies=payload.allergies
        )
        db.merge(history)

        # 4. Tablas longitudinales con Period
        period = get_or_create_period(
            db, "patients_sleep_assessment", payload.patient_id, payload.consultation_date
        )

        sleep_eval = models.PatientSleepAssessment(
            Patient_ID=payload.patient_id,
            Period=period,
            Period_Date=payload.consultation_date,
            Sleep_Initiation=payload.sleep_initiation,
            Nighttime_Awakening=payload.nighttime_awakening,
            Sleep_Maintenance_Difficulty=payload.sleep_maintenance_difficulty,
            Early_Morning_Awakening=payload.early_morning_awakening,
            Nonrestorative_Sleep=payload.nonrestorative_sleep,
            Daytime_Sleepiness=payload.daytime_sleepiness,
            Observed_Apnea=payload.observed_apnea,
            Nocturia=payload.nocturia,
            Morning_Headaches=payload.morning_headaches,
            Bruxism=payload.bruxism,
            Jawjoint_Pain=payload.jawjoint_pain,
            Sleep_Related_Distress=payload.sleep_related_distress,
            Snoring_Affects_Others=payload.snoring_affects_others,
            Partner_Alert_Stop_Noise=payload.partner_alert_stop_noise,
            Acid_Reflux_Symptoms=payload.acid_reflux,
            Jaw_Joint_Click=payload.jaw_joint_click
        )
        db.merge(sleep_eval)

        # 5. Snoring Assessment
        snoring_key = payload.snoring_evolution.strip().lower() if payload.snoring_evolution else None
        snoring_evo = SNORING_EVOLUTION_MAP.get(snoring_key) if snoring_key else None

        snoring = models.SnoringAssessment(
            Patient_ID=payload.patient_id,
            Period=period,
            Period_Date=payload.consultation_date,
            Snoring_Evolution=snoring_evo,
            Snoring_Frequency=payload.snoring_frequency,
            Snoring_Intensity=payload.snoring_intensity,
            Snoring_Position=payload.snoring_position,
            Dry_Mouth=payload.dry_mouth,
            Irritated_Throat=payload.irritated_throat,
            Nasal_Congestion=payload.nasal_congestion,
            Tooth_Grinding=payload.tooth_grinding
        )
        db.merge(snoring)

        # 6. Questionnaire Scores (manejo seguro con diccionarios vacíos por defecto)
        isi = payload.isi_scores or {}
        ess = payload.ess_scores or {}
        qol = payload.qol_scores or {}

        scores = models.QuestionnaireScores(
            Patient_ID=payload.patient_id,
            Period=period,
            Period_Date=payload.consultation_date,
            ISI_Fall_Asleep=isi.get("fall_asleep"),
            ISI_Stay_Asleep=isi.get("stay_asleep"),
            ISI_Waking_Up_Early=isi.get("waking_early"),
            ISI_Sleep_Pattern=isi.get("pattern"),
            ISI_Daily_Functioning=isi.get("functioning"),
            ISI_Noticeble_Sleep_Problem=isi.get("noticeble"),
            ISI_Worry_Sleep_Problem=isi.get("worry"),
            ESS_Sitting_Reading=ess.get("reading"),
            ESS_Watching_TV=ess.get("tv"),
            ESS_Sitting_Inactive=ess.get("inactive"),
            ESS_Passenger=ess.get("passenger"),
            ESS_Lying_Down=ess.get("lying"),
            ESS_Sitting_Talking=ess.get("talking"),
            ESS_Sitting_No_Alcohol=ess.get("no_alcohol"),
            ESS_Car_Traffic=ess.get("traffic"),
            QoL_Effort_Tasks=qol.get("effort_tasks"),
            QoL_Decrease_Abilities_Work=qol.get("decrease_abilities"),
            QoL_Difficulty_Remembering=qol.get("remembering"),
            QoL_Difficulty_Concentrating=qol.get("concentrating"),
            QoL_Depression=qol.get("depression"),
            QoL_Anxiety=qol.get("anxiety"),
            QoL_Difficulty_Activities=qol.get("activities"),
            QoL_Relationships_Guiltiness=qol.get("guiltiness"),
            QoL_Trouble_Alert=qol.get("trouble_alert"),
            QoL_Risk_Daily_Activities=qol.get("risk_activities"),
        )
        db.merge(scores)

        # Confirmación atómica de toda la transacción
        db.commit()
        return {"status": "success", "patient_id": payload.patient_id, "period": period}

    except Exception:
        db.rollback()
        raise