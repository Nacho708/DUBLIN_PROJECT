from pathlib import Path
from pydantic_settings import BaseSettings

# Ruta raíz de backend/ (dos niveles arriba de core/)
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "Beacon Sleep Health Clinic API"
    API_V1_STR: str = "/api/v1"
    
    # Parámetros de base de datos MySQL (por defecto o desde .env)
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "db_dublin_landing_new"

    # Rutas absolutas resueltas dinámicamente
    BASE_DIR: Path = BACKEND_DIR
    FRONTEND_DIR: Path = BACKEND_DIR / "frontend"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4"
        )

    class Config:
        env_file = str(BACKEND_DIR / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()