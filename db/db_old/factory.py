from pathlib import Path

from db.db_connection import get_connection

from db.db_old.csv_reader import read_csv
from db.db_old.excel_reader import read_excel
from db.db_old.pdf_modelo_1 import read_pdf_modelo_1
from db.db_old.pdf_modelo_2 import read_pdf_modelo_2

import pdfplumber


class FileFactory:

    @staticmethod
    def read(file, **kwargs):

        extension = Path(file).suffix.lower()

        if extension == ".csv":
            return read_csv(file)

        elif extension in (".xlsx", ".xls"):
            sheet_name = kwargs.get("sheet_name", 0)
            return read_excel(file, sheet_name)

        elif extension == ".pdf":

            with pdfplumber.open(file) as pdf:
                texto = pdf.pages[0].extract_text() or ""

            if "FACTURA" in texto.upper():
                return read_pdf_modelo_1(file)

            else:
                return read_pdf_modelo_2(file)

        else:
            raise ValueError(f"Formato no soportado: {extension}")
        

class FileFactory:

    ...

    @staticmethod
    def load(file,
             table,
             if_exists="append",
             **kwargs):

        df = FileFactory.read(
            file,
            **kwargs
        )

        connection = get_connection()

        df.to_sql(
            table,
            con=connection,
            if_exists=if_exists,
            index=False
        )

        connection.close()

        return df