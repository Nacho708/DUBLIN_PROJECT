import sys
import os

from sqlalchemy import text

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from db.db_conection import (
    get_server_engine,
    get_engine,
)

from db.db_schema_new import create_all_tables


DATABASE_NAME = "db_dublin_landing_new"


def create_database():

    engine = get_server_engine()

    try:

        with engine.connect() as connection:

            connection.execute(
                text(
                    f"CREATE DATABASE IF NOT EXISTS `{DATABASE_NAME}`"
                )
            )

            connection.commit()

        print(
            f"Database '{DATABASE_NAME}' ready."
        )

    finally:

        engine.dispose()


def initialize_database():

    # ==================================================
    # 1. CREATE DATABASE
    # ==================================================

    create_database()

    # ==================================================
    # 2. CONNECT TO DATABASE
    # ==================================================

    engine = get_engine()

    # ==================================================
    # 3. GET DB-API CONNECTION
    # ==================================================

    connection = engine.raw_connection()

    try:

        # ==================================================
        # 4. CREATE TABLES
        # ==================================================

        create_all_tables(connection)

        print(
            "Database initialized successfully."
        )

    finally:

        connection.close()
        engine.dispose()


if __name__ == "__main__":
    initialize_database()