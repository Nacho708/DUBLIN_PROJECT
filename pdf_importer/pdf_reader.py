from pathlib import Path

from pypdf import PdfReader


class PDFReader:
    """
    Reads a fillable PDF (AcroForm) and returns its fields.
    """

    def __init__(self):
        pass

    def read(self, pdf_path: str | Path) -> dict:

        pdf_path = Path(pdf_path)

        reader = PdfReader(pdf_path)

        fields = reader.get_fields()

        if not fields:
            return {}

        return {
            field_name: field.get("/V", "")
            for field_name, field in fields.items()
        }