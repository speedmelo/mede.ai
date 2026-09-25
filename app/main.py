from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.empresas import router as empresas_router
from app.api.orcamentos import router as orcamentos_router
from app.database import Base, engine
import app.models.empresa
import app.models.orcamento
import app.models.usuario

# Cria as tabelas do banco de dados automaticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mede.ai API B2B",
    description="Plataforma SaaS de Medicoes Tecnicas",
    version="1.0.0",
)

# Roteadores modulares B2B
app.include_router(auth_router)
app.include_router(empresas_router)
app.include_router(orcamentos_router)


@app.get("/")
def home():
  return {"status": "online", "sistema": "Mede.ai B2B API"}