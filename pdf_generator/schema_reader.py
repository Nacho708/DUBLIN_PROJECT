"""
schema_reader.py

Reads the complete MySQL schema and exposes helper methods that can be
used by both the PDF Generator and the PDF Importer.
"""

import os
import re
import sys
from dataclasses import dataclass, field
from typing import Optional

from sqlalchemy import text

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from db.db_conection import get_engine


# ==========================================================
# Data Models
# ==========================================================

@dataclass
class ColumnSchema:

    table: str

    name: str

    sql_type: str

    raw_type: str

    nullable: bool

    primary_key: bool

    foreign_key: bool

    references_table: Optional[str] = None

    references_column: Optional[str] = None

    default: Optional[str] = None

    auto_increment: bool = False

    max_length: Optional[int] = None

    enum_values: Optional[list] = None


@dataclass
class TableSchema:

    name: str

    columns: dict[str, ColumnSchema] = field(default_factory=dict)


# ==========================================================
# Schema Reader
# ==========================================================

class SchemaReader:

    def __init__(self):

        self.engine = get_engine()

    # ------------------------------------------------------

    def get_tables(self):

        query = text("""
            SELECT TABLE_NAME
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = DATABASE()
            ORDER BY TABLE_NAME
        """)

        with self.engine.connect() as connection:

            result = connection.execute(query)

            return [row.TABLE_NAME for row in result]

    # ------------------------------------------------------

    def get_foreign_keys(self, table):

        query = text("""
            SELECT

                COLUMN_NAME,

                REFERENCED_TABLE_NAME,

                REFERENCED_COLUMN_NAME

            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE

            WHERE TABLE_SCHEMA = DATABASE()

            AND TABLE_NAME = :table

            AND REFERENCED_TABLE_NAME IS NOT NULL
        """)

        with self.engine.connect() as connection:

            result = connection.execute(
                query,
                {"table": table}
            )

            foreign_keys = {}

            for row in result:

                foreign_keys[row.COLUMN_NAME] = {

                    "table": row.REFERENCED_TABLE_NAME,

                    "column": row.REFERENCED_COLUMN_NAME
                }

            return foreign_keys

    # ------------------------------------------------------

    def get_table_schema(self, table):

        fk = self.get_foreign_keys(table)

        query = text("""
            SELECT

                COLUMN_NAME,

                DATA_TYPE,

                COLUMN_TYPE,

                IS_NULLABLE,

                COLUMN_KEY,

                COLUMN_DEFAULT,

                EXTRA

            FROM INFORMATION_SCHEMA.COLUMNS

            WHERE TABLE_SCHEMA = DATABASE()

            AND TABLE_NAME = :table

            ORDER BY ORDINAL_POSITION
        """)

        with self.engine.connect() as connection:

            result = connection.execute(
                query,
                {"table": table}
            )

            columns = {}

            for row in result:

                max_length = None

                if "(" in row.COLUMN_TYPE:

                    match = re.search(
                        r"\((\d+)\)",
                        row.COLUMN_TYPE
                    )

                    if match:

                        max_length = int(match.group(1))

                enum_values = None

                if row.DATA_TYPE == "enum":

                    enum_values = re.findall(
                        r"'([^']*)'",
                        row.COLUMN_TYPE
                    )

                column = ColumnSchema(

                    table=table,

                    name=row.COLUMN_NAME,

                    sql_type=row.DATA_TYPE.upper(),

                    raw_type=row.COLUMN_TYPE,

                    nullable=row.IS_NULLABLE == "YES",

                    primary_key=row.COLUMN_KEY == "PRI",

                    foreign_key=row.COLUMN_NAME in fk,

                    references_table=(
                        fk[row.COLUMN_NAME]["table"]
                        if row.COLUMN_NAME in fk else None
                    ),

                    references_column=(
                        fk[row.COLUMN_NAME]["column"]
                        if row.COLUMN_NAME in fk else None
                    ),

                    default=row.COLUMN_DEFAULT,

                    auto_increment=(
                        "auto_increment"
                        in row.EXTRA.lower()
                    ),

                    max_length=max_length,

                    enum_values=enum_values
                )

                columns[column.name] = column

            return TableSchema(

                name=table,

                columns=columns
            )

    # ------------------------------------------------------

    def read_schema(self):

        schema = {}

        for table in self.get_tables():

            schema[table] = self.get_table_schema(table)

        return schema

    # ------------------------------------------------------

    def get_column(self, table_name, column_name):
        """
        Returns the schema of a specific column.
        """

        schema = self.read_schema()

        return schema[table_name].columns[column_name]

    # ------------------------------------------------------

    def get_insert_order(self):

        """
        Returns the tables ordered according to their
        foreign-key dependencies.
        """

        schema = self.read_schema()

        remaining = set(schema.keys())

        ordered = []

        while remaining:

            progress = False

            for table in list(remaining):

                dependencies = [

                    column.references_table

                    for column in schema[table].columns.values()

                    if column.foreign_key

                ]

                if all(

                    dependency in ordered

                    for dependency in dependencies

                ):

                    ordered.append(table)

                    remaining.remove(table)

                    progress = True

            if not progress:

                raise RuntimeError(
                    "Circular foreign-key dependency detected."
                )

        return ordered


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    reader = SchemaReader()

    schema = reader.read_schema()

    for table in schema.values():

        print(f"\n{'=' * 60}")

        print(table.name)

        print("=" * 60)

        for column in table.columns.values():

            print(column)

    print("\nINSERT ORDER")

    print(reader.get_insert_order())