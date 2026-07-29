import pdfplumber
import pandas as pd


def read_pdf_modelo_2(file):

    # Otra lógica completamente distinta

    datos = []

    with pdfplumber.open(file) as pdf:

        texto = ""

        for pagina in pdf.pages:
            texto += pagina.extract_text() or ""

    # Procesamiento del texto...

    df = pd.DataFrame(datos)

    return df