from pathlib import Path

# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PDF_INPUT_DIR = BASE_DIR / "files"

PDF_EXTENSION = "*.pdf"

# ==========================================================
# DATABASE
# ==========================================================

DATABASE_NAME = "apnea"

# ==========================================================
# IMPORT OPTIONS
# ==========================================================

VERBOSE = True

STOP_ON_ERROR = False


# ==========================================================
# HELPERS
# ==========================================================

def get_input_pdf():

    pdfs = sorted(PDF_INPUT_DIR.glob(PDF_EXTENSION))

    if not pdfs:
        raise FileNotFoundError(
            f"No PDF found in '{PDF_INPUT_DIR}'."
        )

    return pdfs

def get_input_pdfs():

    pdfs = sorted(PDF_INPUT_DIR.glob(PDF_EXTENSION))

    if not pdfs:
        raise FileNotFoundError(
            f"No PDF found in '{PDF_INPUT_DIR}'."
        )

    return pdfs