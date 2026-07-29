from db.db_old.factory import FileFactory
from db.db import Database

df = FileFactory.read(
    "pacientes.xlsx",
    sheet_name="Patient_Demographics"
)

Database.insert_dataframe(
    dataframe=df,
    table="patient_demographics"
)