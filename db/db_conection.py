from sqlalchemy import create_engine


def get_engine():

    USER = "root"
    PASSWORD = "Deadmau58$"
    HOST = "localhost"
    DATABASE = "db_dublin_landing"

    connection_string = (
        f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}"
    )

    engine = create_engine(
        connection_string,
        pool_pre_ping=True,
        future=True
    )
    
    return engine