import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Deadmau58$",
        database="db_dublin_landing"
    )