# backend/app/legacy_pdf_importer.py
from __future__ import annotations

import argparse
from datetime import datetime, date
import io
from pathlib import Path
from typing import Any

from pypdf import PdfReader
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, engine
from app.schemas.intake import IntakeFormPayload
from app.services.intake_service import process_intake_form


def clean_pdf_val(val: Any) -> Any:
    if val is None:
        return None
    val_str = str(val).strip()
    if val_str.startswith("/"):
        val_str = val_str[1:]
    return val_str if val_str else None


def parse_date(date_raw: Any) -> date | None:
    if not date_raw:
        return None
    date_str = str(date_raw).strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    return None


def parse_float(val: Any) -> float | None:
    if val in (None, "", "None"):
        return None
    try:
        return float(str(val).replace(",", ".").strip())
    except ValueError:
        return None


def parse_int_or_bool(val: Any) -> int | None:
    if val in (None, "", "None"):
        return None
    s = str(val).strip().lower()
    if s in ("no", "none", "false", "never"):
        return 0
    if s in ("yes", "true"):
        return 1
    try:
        return int(float(s.replace(",", ".")))
    except ValueError:
        return None


class LegacyPDFImporter:
    """
    Importador integral para formularios interactivos AcroForm (V2 / OAT Clinical Registry).
    Procesa las tablas principales de Intake y persiste las tablas clínicas complementarias.
    """

    def __init__(self, db_session: Session | None = None):
        self.db = db_session or SessionLocal()

    def read_pdf_fields(self, pdf_source: Path | str | io.BytesIO) -> dict[str, Any]:
        reader = PdfReader(pdf_source)
        fields = reader.get_fields() or {}
        return {k: clean_pdf_val(v.get("/V", "")) for k, v in fields.items()}

    def extract_structured_tables(self, raw: dict[str, Any]) -> dict[str, dict[str, Any]]:
        """Agrupa campos por tabla según prefijo (ej: physical_exam.Tonsil_Size)."""
        tables_data: dict[str, dict[str, Any]] = {}
        for key, value in raw.items():
            if "." in key:
                table, col = key.split(".", 1)
                tables_data.setdefault(table, {})[col] = value
            else:
                tables_data.setdefault("unassigned", {})[key] = value
        return tables_data

    def build_payload_from_fields(self, raw: dict[str, Any], fallback_filename: str | None = None) -> IntakeFormPayload:
        """Extrae y normaliza los datos al esquema oficial IntakeFormPayload."""
        def get_val(*field_names: str) -> Any:
            for name in field_names:
                # 1. Búsqueda exacta
                if name in raw and raw[name] not in (None, ""):
                    return raw[name]
                # 2. Búsqueda por sufijo o clave normalizada
                for k, v in raw.items():
                    if v not in (None, ""):
                        if k.split(".")[-1].lower() == name.lower():
                            return v
                        k_clean = k.split(".")[-1].lower().replace(" ", "").replace("_", "")
                        n_clean = name.lower().replace(" ", "").replace("_", "")
                        if k_clean == n_clean:
                            return v
            return None

        # Patient ID
        patient_id = get_val("patient_demographics.Patient_ID", "patients.Patient_ID", "Patient_ID", "ID")
        if not patient_id and fallback_filename:
            import re
            m = re.search(r'(?:P\d+|\d+)', fallback_filename)
            if m:
                patient_id = m.group(0)

        if not patient_id:
            raise ValueError("The PDF does not contain a valid 'Patient_ID'.")

        patient_id = str(patient_id).strip()

        # Fechas
        consult_date = parse_date(get_val("Consultation_Date", "Period_Date", "Date")) or date.today()
        dob = parse_date(get_val("Date_of_Birth", "DOB"))

        # Hábitos
        tobacco_raw = get_val("Tobacco_Use")
        tobacco = "Never" if str(tobacco_raw).strip().lower() in ("no", "0", "never") else str(tobacco_raw or "Never")
        
        alcohol_raw = get_val("Alcohol_Use")
        alcohol = "Never" if str(alcohol_raw).strip().lower() in ("no", "0", "never") else str(alcohol_raw or "Never")

        # ISI scores (7 ítems independientes)
        isi = {
            "fall_asleep": parse_int_or_bool(get_val("Isi_Fall_Asleep")),
            "stay_asleep": parse_int_or_bool(get_val("Isi_Stay_Asleep")),
            "waking_early": parse_int_or_bool(get_val("Isi_Waking_Up_Early")),
            "pattern": parse_int_or_bool(get_val("Isi_Sleep_Pattern")),
            "functioning": parse_int_or_bool(get_val("Isi_Daily_Functioning")),
            "noticeble": parse_int_or_bool(get_val("Isi_Noticeable_Sleep_Problem", "Isi_Noticeble_Sleep_Problem")),
            "worry": parse_int_or_bool(get_val("Isi_Worry_Sleep_Problem")),
        }

        # ESS scores (8 situaciones independientes)
        ess = {
            "reading": parse_int_or_bool(get_val("Ess_Sitting_Reading")),
            "tv": parse_int_or_bool(get_val("Ess_Watching_TV")),
            "inactive": parse_int_or_bool(get_val("Ess_Sitting_Inactive")),
            "passenger": parse_int_or_bool(get_val("Ess_Passenger")),
            "lying": parse_int_or_bool(get_val("Ess_Lying_Down")),
            "talking": parse_int_or_bool(get_val("Ess_Sitting_Talking")),
            "no_alcohol": parse_int_or_bool(get_val("Ess_Sitting_No_Alcohol")),
            "traffic": parse_int_or_bool(get_val("Ess_Car_Traffic")),
        }

        # QoL scores (10 ítems independientes)
        qol = {
            "effort_tasks": parse_int_or_bool(get_val("Qol_Effort_Tasks")),
            "decrease_abilities": parse_int_or_bool(get_val("Qol_Decrease_Abilities_Work")),
            "remembering": parse_int_or_bool(get_val("Qol_Difficulty_Remembering")),
            "concentrating": parse_int_or_bool(get_val("Qol_Difficulty_Concentrating")),
            "depression": parse_int_or_bool(get_val("Qol_Depression")),
            "anxiety": parse_int_or_bool(get_val("Qol_Anxiety")),
            "activities": parse_int_or_bool(get_val("Qol_Difficulty_Activities")),
            "guiltiness": parse_int_or_bool(get_val("Qol_Relationships_Guiltiness")),
            "trouble_alert": parse_int_or_bool(get_val("Qol_Trouble_Alert")),
            "risk_activities": parse_int_or_bool(get_val("Qol_Risk_Daily_Activities")),
        }

        return IntakeFormPayload(
            patient_id=patient_id,
            consultation_date=consult_date,
            date_of_birth=dob,
            age=parse_int_or_bool(get_val("Age")),
            gender=get_val("Sex", "Gender") or "Other",
            height_cm=parse_float(get_val("Height_cm")),
            weight_kg=parse_float(get_val("Weight_kg")),
            tobacco_use=tobacco,
            alcohol_use=alcohol,
            primary_concern=get_val("Primary_Concern"),

            # Medical History
            hypertension=parse_int_or_bool(get_val("Hypertension")),
            diabetes=parse_int_or_bool(get_val("Diabetes")),
            heart_disease=parse_int_or_bool(get_val("Heart_Disease")),
            stroke_tia=parse_int_or_bool(get_val("Stroke_TIA")),
            thyroid_disorder=parse_int_or_bool(get_val("Thyroid_Disorder")),
            depression=parse_int_or_bool(get_val("Depression")),
            gerd=parse_int_or_bool(get_val("GERD")),
            cancer=parse_int_or_bool(get_val("Cancer")),
            asthma_copd=parse_int_or_bool(get_val("Asthma_COPD")),
            other_medical=get_val("Other") if get_val("Other") != "None" else None,
            medications=get_val("Medication") if get_val("Medication") != "None" else None,
            surgery=get_val("Surgery") if get_val("Surgery") != "None" else "No",
            allergies=get_val("Allergies") if get_val("Allergies") != "None" else "No",

            # Sleep Assessment (con preguntas V2)
            sleep_initiation=parse_int_or_bool(get_val("Sleep_Initiation")),
            nighttime_awakening=parse_int_or_bool(get_val("Nighttime_Awakening")),
            sleep_maintenance_difficulty=parse_int_or_bool(get_val("Sleep_Maintenance_Difficulty")),
            early_morning_awakening=parse_int_or_bool(get_val("Early_Morning_Awakening")),
            nonrestorative_sleep=parse_int_or_bool(get_val("Nonrestorative_Sleep")),
            daytime_sleepiness=parse_int_or_bool(get_val("Daytime_Sleepiness")),
            observed_apnea=parse_int_or_bool(get_val("Observed_Apnea")),
            nocturia=parse_int_or_bool(get_val("Nocturia")),
            morning_headaches=parse_int_or_bool(get_val("Morning_Headaches")),
            bruxism=parse_int_or_bool(get_val("Bruxism")),
            jawjoint_pain=parse_int_or_bool(get_val("Jawjoint_Pain")),
            sleep_related_distress=parse_int_or_bool(get_val("Sleep_Related_Distress")),
            snoring_affects_others=parse_int_or_bool(get_val("Snoring_Affects_Others")),
            partner_alert_stop_noise=parse_int_or_bool(get_val("Partner_Alert_Stop_Noise")),
            acid_reflux=parse_int_or_bool(get_val("Acid_Reflux_Symptoms")),
            jaw_joint_click=parse_int_or_bool(get_val("Jaw_Joint_Click")),

            # Snoring
            snoring_evolution=get_val("Snoring_Evolution"),
            snoring_frequency=parse_int_or_bool(get_val("Snoring_Frequency")),
            snoring_intensity=parse_int_or_bool(get_val("Snoring_Intensity")),
            snoring_position=get_val("Snoring_Position"),
            dry_mouth=parse_int_or_bool(get_val("Dry_Mouth")),
            irritated_throat=parse_int_or_bool(get_val("Irritated_Throat")),
            nasal_congestion=parse_int_or_bool(get_val("Nasal_Congestion")),
            tooth_grinding=parse_int_or_bool(get_val("Tooth_Grinding")),

            # Questionnaires
            isi_scores=isi,
            ess_scores=ess,
            qol_scores=qol,
        )

    def persist_additional_clinical_tables(self, patient_id: str, period: int, period_date: date, tables_data: dict[str, dict[str, Any]]):
        """Vuelca las tablas clínicas auxiliares (CBCT, PSG, Examen Físico, Tratamiento, Seguimiento)."""
        allowed_additional_tables = [
            "physical_exam",
            "sleep_study",
            "cbct_measurements",
            "treatment",
            "followup",
            "sleep_history",
        ]

        with engine.begin() as conn:
            for table in allowed_additional_tables:
                if table not in tables_data:
                    continue

                row = dict(tables_data[table])
                row["Patient_ID"] = patient_id
                row["Period"] = period
                row["Period_Date"] = period_date

                cols = list(row.keys())
                col_names = ", ".join(f"`{c}`" for c in cols)
                placeholders = ", ".join(f":{c}" for c in cols)
                updates = ", ".join(f"`{c}`=VALUES(`{c}`)" for c in cols if c not in ("Patient_ID", "Period"))

                stmt = text(f"""
                    INSERT INTO `{table}` ({col_names})
                    VALUES ({placeholders})
                    ON DUPLICATE KEY UPDATE {updates}
                """)
                try:
                    conn.execute(stmt, row)
                except Exception as e:
                    print(f"[WARN] No se pudo guardar tabla adicional '{table}': {e}")

    def import_single_pdf(self, pdf_source: Path | str | io.BytesIO, filename: str | None = None) -> dict[str, Any]:
        """Extrae el PDF y ejecuta el volcado atómico en MySQL."""
        raw_fields = self.read_pdf_fields(pdf_source)
        if not raw_fields:
            raise ValueError("No se encontraron campos interactivos en el PDF.")

        payload = self.build_payload_from_fields(raw_fields, fallback_filename=filename)
        
        # 1. Guardar admisión principal
        intake_res = process_intake_form(payload, self.db)
        patient_id = intake_res["patient_id"]
        period = intake_res["period"]

        # 2. Persistir tablas clínicas avanzadas
        structured_tables = self.extract_structured_tables(raw_fields)
        self.persist_additional_clinical_tables(
            patient_id=patient_id,
            period=period,
            period_date=payload.consultation_date,
            tables_data=structured_tables,
        )

        return {
            "patient_id": patient_id,
            "period": period,
            "additional_tables_saved": [t for t in structured_tables if t != "unassigned"],
        }


def main():
    parser = argparse.ArgumentParser(description="Importador de PDFs clínicos a MySQL V2.")
    parser.add_argument(
        "--file",
        type=str,
        default="legacy/sample_files/pdfs/OAT_Clinical_Form_P011_Fillable_V2.pdf",
        help="Ruta al archivo PDF a importar",
    )
    args = parser.parse_args()

    importer = LegacyPDFImporter()
    pdf_path = Path(args.file)
    print(f"Importando {pdf_path.name}...")
    res = importer.import_single_pdf(pdf_path, filename=pdf_path.name)
    print(f"✅ ¡Éxito! Patient ID: {res['patient_id']} | Period: {res['period']}")
    print(f"   Tablas complementarias guardadas: {res['additional_tables_saved']}")


if __name__ == "__main__":
    main()