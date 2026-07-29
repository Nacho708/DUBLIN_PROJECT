"""
type_converter.py

Converts raw values to the correct Python type based on the SQL type.
"""

from datetime import datetime


class TypeConverter:

    @staticmethod
    def convert(value, column):
        """
        Converts a raw value according to the SQL type defined
        in the ColumnSchema.

        Parameters
        ----------
        value
            Raw value read from the PDF.

        column : ColumnSchema
            Column metadata.

        Returns
        -------
        Converted Python value.
        """

        if value in ("", None):
            return None

        sql_type = column.sql_type.upper()

        if sql_type in (
            "INT",
            "INTEGER",
            "BIGINT",
            "SMALLINT",
            "TINYINT",
            "MEDIUMINT",
        ):
            return TypeConverter._to_int(value)

        if sql_type in (
            "FLOAT",
            "DOUBLE",
            "DECIMAL",
            "NUMERIC",
        ):
            return TypeConverter._to_float(value)

        if sql_type in (
            "DATE",
            "DATETIME",
            "TIMESTAMP",
        ):
            return TypeConverter._to_date(value, sql_type)

        if sql_type == "BOOLEAN":
            return TypeConverter._to_bool(value)

        return str(value).strip()

    # -----------------------------------------------------

    @staticmethod
    def _to_int(value):
        """
        Converts a value to integer.

        Also supports common boolean values stored as TINYINT(1).
        """

        if isinstance(value, int):
            return value

        value = str(value).strip()

        if value == "":
            return None

        value_lower = value.lower()

        true_values = {
            "1",
            "true",
            "yes",
            "y",
            "si",
            "sí",
            "on",
        }

        false_values = {
            "0",
            "false",
            "no",
            "n",
            "off",
        }

        if value_lower in true_values:
            return 1

        if value_lower in false_values:
            return 0

        return int(value)

    # -----------------------------------------------------

    @staticmethod
    def _to_float(value):

        if isinstance(value, float):
            return value

        value = str(value).replace(",", ".")

        return float(value)

    # -----------------------------------------------------

    @staticmethod
    def _to_bool(value):

        if isinstance(value, bool):
            return value

        value = str(value).strip().lower()

        if value in (
            "true",
            "yes",
            "y",
            "si",
            "sí",
            "1",
        ):
            return True

        if value in (
            "false",
            "no",
            "n",
            "0",
        ):
            return False

        raise ValueError(f"Cannot convert '{value}' to BOOLEAN.")

    # -----------------------------------------------------

    @staticmethod
    def _to_date(value, sql_type):

        if isinstance(value, datetime):
            return value

        value = str(value).strip()

        formats = [

            "%d/%m/%Y",

            "%Y-%m-%d",

            "%d-%m-%Y",

            "%Y/%m/%d",
        ]

        for fmt in formats:

            try:

                date = datetime.strptime(value, fmt)

                if sql_type == "DATE":
                    return date.date()

                return date

            except ValueError:
                continue

        raise ValueError(f"Cannot convert '{value}' to {sql_type}.")