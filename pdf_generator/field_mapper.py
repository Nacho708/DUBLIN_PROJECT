"""
field_mapper.py
===============

Automatic inference of the PDF template to use when a field
is not explicitly defined in field_metadata.metadata.

The goal of this class is NOT to build the whole form,
but to provide a smart fallback based on the database schema.
"""

from field_metadata.templates import (
    TEXT_TEMPLATE,
    TEXTAREA_TEMPLATE,
    INTEGER_TEMPLATE,
    DECIMAL_2_TEMPLATE,
    DATE_TEMPLATE,
    TIME_TEMPLATE,
    DATETIME_TEMPLATE,
    CHECKBOX_TEMPLATE,
)

from field_metadata.constants import DataType


class FieldMapper:
    """
    Maps a database column to the most appropriate PDF template.
    """

    def __init__(self):

        self.type_map = {

            # ===============================
            # Text
            # ===============================

            "CHAR": TEXT_TEMPLATE,
            "VARCHAR": TEXT_TEMPLATE,
            "TINYTEXT": TEXT_TEMPLATE,

            "TEXT": TEXTAREA_TEMPLATE,
            "MEDIUMTEXT": TEXTAREA_TEMPLATE,
            "LONGTEXT": TEXTAREA_TEMPLATE,

            # ===============================
            # Integers
            # ===============================

            "TINYINT": INTEGER_TEMPLATE,
            "SMALLINT": INTEGER_TEMPLATE,
            "MEDIUMINT": INTEGER_TEMPLATE,
            "INT": INTEGER_TEMPLATE,
            "INTEGER": INTEGER_TEMPLATE,
            "BIGINT": INTEGER_TEMPLATE,

            # ===============================
            # Decimals
            # ===============================

            "DECIMAL": DECIMAL_2_TEMPLATE,
            "NUMERIC": DECIMAL_2_TEMPLATE,
            "FLOAT": DECIMAL_2_TEMPLATE,
            "DOUBLE": DECIMAL_2_TEMPLATE,
            "REAL": DECIMAL_2_TEMPLATE,

            # ===============================
            # Dates
            # ===============================

            "DATE": DATE_TEMPLATE,
            "TIME": TIME_TEMPLATE,
            "DATETIME": DATETIME_TEMPLATE,
            "TIMESTAMP": DATETIME_TEMPLATE,

            # ===============================
            # Boolean
            # ===============================

            "BOOL": CHECKBOX_TEMPLATE,
            "BOOLEAN": CHECKBOX_TEMPLATE,
        }

    # ==========================================================
    # PUBLIC API
    # ==========================================================

    def map_field(self, sql_type: str):
        """
        Returns the default template for a SQL type.
        """

        if not sql_type:
            return TEXT_TEMPLATE

        sql_type = sql_type.upper()

        return self.type_map.get(
            sql_type,
            TEXT_TEMPLATE
        )

    # ----------------------------------------------------------

    def infer_from_column(self, column):
        """
        Infers the most appropriate template from a ColumnSchema.
        """

        # Auto-increment primary keys
        if column.auto_increment:
            return INTEGER_TEMPLATE

        # ENUM
        # (later we can replace this with a ComboBox template)
        if column.enum_values:
            return TEXT_TEMPLATE

        return self.map_field(column.sql_type)

    # ==========================================================
    # HELPERS
    # ==========================================================

    @staticmethod
    def is_numeric(template):

        return template.data_type in (
            DataType.INTEGER,
            DataType.FLOAT,
            DataType.DECIMAL,
        )

    @staticmethod
    def is_date(template):

        return template.data_type in (
            DataType.DATE,
            DataType.TIME,
            DataType.DATETIME,
        )

    @staticmethod
    def is_text(template):

        return template.data_type == DataType.TEXT

    @staticmethod
    def is_multiline(template):

        return template.multiline

    @staticmethod
    def is_required(template):

        return template.required

    @staticmethod
    def is_read_only(template):

        return template.read_only

    @staticmethod
    def has_options(template):

        return bool(template.options)