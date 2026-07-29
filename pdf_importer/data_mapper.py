"""
data_mapper.py

Converts PDF form data into a structure grouped by database table.

Input:

{
    "patient_demographics.Patient_ID": "123",
    "patient_demographics.Sex": "Male",
    "medical_history.Diabetes": "Yes",
}

Output:

{
    "patient_demographics": {
        "Patient_ID": "123",
        "Sex": "Male",
    },
    "medical_history": {
        "Diabetes": "Yes",
    }
}
"""


class DataMapper:
    """
    Maps PDF fields to database tables.
    """

    def __init__(self):
        pass

    def map(self, data: dict) -> dict:
        """
        Convert flat PDF data into a dictionary grouped by table.

        Parameters
        ----------
        data : dict
            Dictionary returned by PDFReader.

        Returns
        -------
        dict
            Dictionary grouped by table.
        """

        tables = {}

        for field_name, value in data.items():

            table_name, column_name = self.split_field(field_name)

            if table_name is None:
                continue

            if table_name not in tables:
                tables[table_name] = {}

            tables[table_name][column_name] = value

        return tables

    def split_field(self, field_name):
        """
        Split a field into:

            table.column

        Returns
        -------
        tuple
            (table, column)
        """

        if "." not in field_name:
            return None, None

        return field_name.split(".", 1)