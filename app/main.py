from fastapi import FastAPI
from app.schemas.orcamento import EntradasMedicaoSchema
from app.core.calculadora import CalculadoraVidro

app = FastAPI(
    title="Mede.ai API B2B",
    description="Plataforma SaaS de Medições Técnicas, Orçamentos 3D e Pedidos de Vidro",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "status": "online",
        "sistema": "Mede.ai B2B API",
        "mensagem": "Servidor rodando perfeitamente!"
    }

@app.post("/api/v1/calcular-vidro")
def calcular_vidro(dados: EntradasMedicaoSchema):
    resultado = CalculadoraVidro.calcular_pecas_sacada_reta(
        largura_vao_mm=dados.largura_vao_mm,
        altura_vao_mm=dados.altura_vao_mm,
        qtd_pecas=dados.qtd_pecas
    )
    return {
        "especificacoes": {
            "cor_vidro": dados.cor_vidro,
            "espessura": dados.espessura_vidro,
            "cor_aluminio": dados.cor_aluminio
        },
        "resultado_corte": resultado
    }