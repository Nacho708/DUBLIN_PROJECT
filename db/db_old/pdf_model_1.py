import pdfplumber
import pandas as pd


def read_pdf_modelo_1(file):

    # Aquí irá la lógica específica
    # para este tipo de PDF

    datos = []

    with pdfplumber.open(file) as pdf:

        for pagina in pdf.pages:

            tabla = pagina.extract_table()

            if tabla:
                datos.extend(tabla)

    df = pd.DataFrame(datos)

    return df