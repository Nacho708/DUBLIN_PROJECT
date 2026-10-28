# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# 1. Configuración, motor y modelos relacionales
from app.core.config import settings
from app.db.session import engine
from app.db.base_class import Base
import app.db.models  # Importa los modelos para registrarlos en los metadatos

# 2. Router principal unificado (V1)
from app.api.v1.endpoints.api_router import api_router

# 3. Crear las tablas en MySQL si aún no existen
Base.metadata.create_all(bind=engine)

# 4. Inicializar FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 5. Configuración de CORS para pruebas locales y Cloudflare Tunnel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 6. Montar los endpoints de la API (/api/v1/intake, /api/v1/patients)
app.include_router(api_router, prefix=settings.API_V1_STR)

# 7. Servir Frontend estático (index.html)
if settings.FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=settings.FRONTEND_DIR), name="static")

@app.get("/", include_in_schema=False)
def serve_frontend():
    index_file = settings.FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {
        "status": "warning",
        "message": f"El archivo index.html no fue localizado en {settings.FRONTEND_DIR}"
    }

@app.get("/health", tags=["Health Check"])
def health_check():
    """Endpoint ligero para monitorizar la salud del backend y el túnel."""
    return {"status": "healthy", "project": settings.PROJECT_NAME}