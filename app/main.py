from fastapi import FastAPI
from app.database import engine, Base
from app.api.auth import router as auth_router
from app.api.empresas import router as empresas_router
from app.api.orcamentos import router as orcamentos_router
from app.api.usuarios import router as usuarios_router
import app.models.empresa
import app.models.usuario
import app.models.orcamento

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mede.ai API B2B", description="Plataforma SaaS de Medicoes Tecnicas", version="1.0.0")

app.include_router(auth_router)
app.include_router(empresas_router)
app.include_router(orcamentos_router)
app.include_router(usuarios_router)

@app.get("/")
def home():
    return {"status": "online", "sistema": "Mede.ai B2B API"}
