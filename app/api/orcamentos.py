from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from app.api.auth import oauth2_scheme, ALGORITHM, SECRET_KEY
from app.core.calculadora import CalculadoraVidro
from app.core.gerador_pdf import GeradorContratoPDF
from app.database import get_db
from app.models.empresa import Empresa
from app.models.orcamento import Orcamento
from jose import jwt, JWTError
import os

router = APIRouter(prefix="/api/v1/orcamentos", tags=["Orcamentos B2B"])

class CriarOrcamentoSchema(BaseModel):
    nome_cliente: str
    whatsapp_cliente: str
    largura_vao_mm: float
    altura_vao_mm: float
    qtd_pecas: int
    cor_vidro: str = "Incolor"
    espessura_vidro: str = "10mm"
    cor_aluminio: str = "Preto"

def obter_empresa_logada(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Empresa:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        empresa_id = payload.get("empresa_id")
        if not empresa_id:
            raise HTTPException(status_code=401, detail="Token invalido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expirado ou invalido")
    empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa nao encontrada")
    return empresa

@router.post("/gerar-e-salvar", status_code=status.HTTP_201_CREATED)
def gerar_e_salvar_orcamento(dados: CriarOrcamentoSchema, empresa: Empresa = Depends(obter_empresa_logada), db: Session = Depends(get_db)):
    resultado = CalculadoraVidro.calcular_pecas_sacada_reta(
        largura_vao_mm=dados.largura_vao_mm, altura_vao_mm=dados.altura_vao_mm, qtd_pecas=dados.qtd_pecas
    )
    novo_orcamento = Orcamento(
        empresa_id=empresa.id,
        cliente_nome=dados.nome_cliente,
        cliente_whatsapp=dados.whatsapp_cliente,
        largura_mm=dados.largura_vao_mm,
        altura_mm=dados.altura_vao_mm,
        qtd_pecas=dados.qtd_pecas,
        cor_vidro=dados.cor_vidro,
        espessura_vidro=dados.espessura_vidro,
        cor_aluminio=dados.cor_aluminio,
        medida_corte_resumo=resultado.get("medida_corte_fabrica"),
    )
    db.add(novo_orcamento)
    db.commit()
    db.refresh(novo_orcamento)
    caminho_pdf = f"temp/contrato_orcamento_{novo_orcamento.id}.pdf"
    GeradorContratoPDF.gerar_pdf_orcamento(
        caminho_saida=caminho_pdf,
        dados_empresa={"nome_fantasia": empresa.nome_fantasia, "cnpj": empresa.cnpj},
        dados_cliente={"nome": dados.nome_cliente, "whatsapp": dados.whatsapp_cliente},
        especificacoes={"cor_vidro": dados.cor_vidro, "espessura": dados.espessura_vidro, "cor_aluminio": dados.cor_aluminio},
        resultado_corte=resultado,
    )
    return FileResponse(caminho_pdf, media_type="application/pdf", filename=f"contrato_{novo_orcamento.id}.pdf")

@router.get("/", status_code=status.HTTP_200_OK)
def listar_historico_orcamentos(empresa: Empresa = Depends(obter_empresa_logada), db: Session = Depends(get_db)):
    orcamentos = db.query(Orcamento).filter(Orcamento.empresa_id == empresa.id).order_by(Orcamento.criado_em.desc()).all()
    return [{"id": o.id, "cliente_nome": o.cliente_nome, "cliente_whatsapp": o.cliente_whatsapp, "medida_corte_resumo": o.medida_corte_resumo, "criado_em": o.criado_em} for o in orcamentos]

@router.get("/{orcamento_id}", status_code=status.HTTP_200_OK)
def buscar_orcamento_por_id(orcamento_id: int, empresa: Empresa = Depends(obter_empresa_logada), db: Session = Depends(get_db)):
    orcamento = db.query(Orcamento).filter(Orcamento.id == orcamento_id, Orcamento.empresa_id == empresa.id).first()
    if not orcamento:
        raise HTTPException(status_code=404, detail="Orcamento nao encontrado")
    return orcamento

@router.get("/{orcamento_id}/pdf", status_code=status.HTTP_200_OK)
def rebaixar_pdf_orcamento(orcamento_id: int, empresa: Empresa = Depends(obter_empresa_logada), db: Session = Depends(get_db)):
    orcamento = db.query(Orcamento).filter(Orcamento.id == orcamento_id, Orcamento.empresa_id == empresa.id).first()
    if not orcamento:
        raise HTTPException(status_code=404, detail="Orcamento nao encontrado")
    resultado = CalculadoraVidro.calcular_pecas_sacada_reta(
        largura_vao_mm=orcamento.largura_mm, altura_vao_mm=orcamento.altura_mm, qtd_pecas=orcamento.qtd_pecas
    )
    caminho_pdf = f"temp/contrato_orcamento_{orcamento.id}.pdf"
    GeradorContratoPDF.gerar_pdf_orcamento(
        caminho_saida=caminho_pdf,
        dados_empresa={"nome_fantasia": empresa.nome_fantasia, "cnpj": empresa.cnpj},
        dados_cliente={"nome": orcamento.cliente_nome, "whatsapp": orcamento.cliente_whatsapp},
        especificacoes={"cor_vidro": orcamento.cor_vidro, "espessura": orcamento.espessura_vidro, "cor_aluminio": orcamento.cor_aluminio},
        resultado_corte=resultado,
    )
    return FileResponse(caminho_pdf, media_type="application/pdf", filename=f"contrato_{orcamento.id}.pdf")
