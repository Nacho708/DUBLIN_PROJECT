import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from db.db_conection import get_connection
import openpyxl

def export_database_to_excel():

    connection = get_connection()
    cursor = connection.cursor()

    # Obtener todas las tablas
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    # Crear archivo Excel
    with pd.ExcelWriter("D:\\Documentos\\DUBLIN_PROJECT\\excel\\database_dublin.xlsx", engine="openpyxl") as writer:

        for table in tables:

            table_name = table[0]

            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, connection)

            df.to_excel(writer, sheet_name=table_name, index=False)

            print(f"✔ Exported: {table_name}")

    cursor.close()
    connection.close()

    print("\n✅ Database exported successfully to database_export.xlsx")


if __name__ == "__main__":
    export_database_to_excel()