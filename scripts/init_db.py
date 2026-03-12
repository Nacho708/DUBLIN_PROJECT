import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.db_conection import get_connection
from db.db_schema import create_all_tables


def initialize_database():

    connection = get_connection()

    create_all_tables(connection)

    connection.close()

    print("Database initialized successfully")


if __name__ == "__main__":
    initialize_database()