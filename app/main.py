from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.auth import router as auth_router
from app.api.empresas import router as empresas_router
from app.core.calculadora import CalculadoraVidro
from app.core.gerador_pdf import GeradorContratoPDF
from app.database import Base, engine
import app.models.empresa
import app.models.orcamento
import app.models.usuario
from app.schemas.orcamento import EntradasMedicaoSchema

# Cria as tabelas do banco de dados automaticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mede.ai API B2B",
    description="Plataforma SaaS de Medicoes Tecnicas",
    version="1.0.0",
)

# Inclui os roteadores das rotas criadas
app.include_router(auth_router)
app.include_router(empresas_router)


@app.get("/")
def home():
  return {"status": "online", "sistema": "Mede.ai B2B API"}


@app.post("/api/v1/gerar-contrato-pdf")
def gerar_contrato(dados: EntradasMedicaoSchema):
  resultado = CalculadoraVidro.calcular_pecas_sacada_reta(
      largura_vao_mm=dados.largura_vao_mm,
      altura_vao_mm=dados.altura_vao_mm,
      qtd_pecas=dados.qtd_pecas,
  )

  caminho = "temp/contrato_teste.pdf"

  GeradorContratoPDF.gerar_pdf_orcamento(
      caminho_saida=caminho,
      dados_empresa={
          "nome_fantasia": "Vidracaria Modelo B2B",
          "cnpj": "12.345.678/0001-90",
      },
      dados_cliente={
          "nome": "Cliente Exemplo",
          "whatsapp": "(11) 99999-9999",
      },
      especificacoes={
          "cor_vidro": dados.cor_vidro,
          "espessura": dados.espessura_vidro,
          "cor_aluminio": dados.cor_aluminio,
      },
      resultado_corte=resultado,
  )

  return FileResponse(
      caminho, media_type="application/pdf", filename="contrato_medicao.pdf"
  )