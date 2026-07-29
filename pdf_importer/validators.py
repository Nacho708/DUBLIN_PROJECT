"""
validators.py

Validates and converts PDF values according to the
database schema.
"""

from .type_converter import TypeConverter


class Validator:

    def __init__(self, schema):

        self.schema = schema

    # --------------------------------------------------

    def validate(self, mapped_data):
        """
        Validates every value contained in mapped_data.
        """

        validated_data = {}

        for table_name, row in mapped_data.items():

            validated_data[table_name] = {}

            table_schema = self.schema[table_name]

            for column_name, value in row.items():

                column = self._get_column(
                    table_schema,
                    column_name
                )

                print(
                    f"Validating {table_name}.{column_name} | "
                    f"value={value!r} | "
                    f"sql_type={column.sql_type}"
                )

                validated_data[table_name][column_name] = (
                    TypeConverter.convert(
                        value,
                        column
                    )
                )

        return validated_data

    # --------------------------------------------------

    @staticmethod
    def _get_column(table_schema, column_name):

        try:
            return table_schema.columns[column_name]

        except KeyError:

            raise ValueError(
                f"Column '{column_name}' not found "
                f"in table '{table_schema.name}'."
            )