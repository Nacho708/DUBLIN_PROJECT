"""
database_writer.py

Writes mapped PDF data into the MySQL database.
Uses UPSERT (INSERT ... ON DUPLICATE KEY UPDATE).
"""

from sqlalchemy import text

from db.db_conection import get_engine


INSERT_ORDER = [
    "patients",
    "patient_demographics",
    "medical_history",
    "patient_symptoms",
    "physical_exam",
    "questionnaire_scores",
    "sleep_history",
    "sleep_study",
    "cbct_measurements",
    "treatment",
    "followup",
    "sleep_symptom_frequency",
    "snoring_assessment",
]


class DatabaseWriter:

    def __init__(self):
        self.engine = get_engine()

    # --------------------------------------------------

    def write(self, data: dict):

        with self.engine.begin() as connection:

            for table_name in INSERT_ORDER:

                if table_name not in data:
                    continue

                self.upsert_row(
                    connection,
                    table_name,
                    data[table_name]
                )

    # --------------------------------------------------

    def upsert_row(self, connection, table_name: str, row_data: dict):

        columns = ", ".join(row_data.keys())

        placeholders = ", ".join(
            f":{column}"
            for column in row_data.keys()
        )

        # Build UPDATE clause excluding Patient_ID
        update_clause = ", ".join(
            f"{column}=VALUES({column})"
            for column in row_data.keys()
            if column != "Patient_ID"
        )

        query = text(
            f"""
            INSERT INTO {table_name}
            ({columns})
            VALUES ({placeholders})
            ON DUPLICATE KEY UPDATE
            {update_clause}
            """
        )

        print("\n==========================")
        print(f"TABLE: {table_name}")
        print(query)
        print(row_data)
        print("==========================")

        connection.execute(query, row_data)