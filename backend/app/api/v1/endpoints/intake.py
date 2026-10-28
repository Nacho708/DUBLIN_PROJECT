# backend/app/api/v1/endpoints/intake.py
import io
import traceback
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db
from app.schemas.intake import IntakeFormPayload
from app.services.intake_service import process_intake_form
from app.legacy_pdf_importer import LegacyPDFImporter

router = APIRouter()

@router.post("", status_code=status.HTTP_201_CREATED)
def submit_intake_form(payload: IntakeFormPayload, db: Session = Depends(get_db)):
    """Recibe y persiste los datos desde el formulario web manual."""
    try:
        return process_intake_form(payload, db)
    except Exception as e:
        db.rollback()
        print("\n" + "="*50 + " ERROR MANUAL INTAKE " + "="*50)
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al guardar el formulario de admisión: {str(e)}"
        )

@router.post("/upload-pdf", status_code=status.HTTP_200_OK)
async def upload_multiple_pdf_intake(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """
    Recibe uno o varios archivos PDF clínicos (AcroForm), los procesa sucesivamente
    e inserta cada expediente en la base de datos de manera atómica e independiente.
    """
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se ha recibido ningún archivo PDF."
        )

    results = []
    importer = LegacyPDFImporter(db_session=db)

    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            results.append({
                "filename": file.filename,
                "status": "error",
                "message": "Formato inválido (solo archivos .pdf)"
            })
            continue

        try:
            content = await file.read()
            pdf_stream = io.BytesIO(content)

            # Usamos el importador completo que persiste admisión + tablas clínicas
            res = importer.import_single_pdf(pdf_stream, filename=file.filename)

            results.append({
                "filename": file.filename,
                "status": "success",
                "patient_id": res["patient_id"],
                "period": res["period"],
                "additional_tables": res.get("additional_tables_saved", [])
            })

        except Exception as e:
            db.rollback()
            print(f"\n[ERROR PDF IMPORT] Error procesando '{file.filename}': {e}")
            traceback.print_exc()
            results.append({
                "filename": file.filename,
                "status": "error",
                "message": str(e)
            })

    total_success = sum(1 for r in results if r["status"] == "success")
    return {
        "total_files": len(files),
        "successful_imports": total_success,
        "results": results
    }