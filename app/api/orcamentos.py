from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from typing import List
from sqlalchemy.orm import Session
from app.api.auth import oauth2_scheme, ALGORITHM, SECRET_KEY
from app.core.calculadora import CalculadoraVidro
from app.core.gerador_pdf import GeradorContratoPDF
from app.database import get_db
from app.models.empresa import Empresa
from app.models.orcamento import Orcamento
from app.schemas.orcamento import EntradasMedicaoSchema
from jose import jwt, JWTError
import os

router = APIRouter(prefix="/api/v1/orcamentos", tags=["Orcamentos B2B"])

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
def gerar_e_salvar_orcamento(dados: EntradasMedicaoSchema, empresa: Empresa = Depends(obter_empresa_logada), db: Session = Depends(get_db)):
    if dados.tipo_calculo == "box_padrao":
        resultado = CalculadoraVidro.calcular_box_padrao(dados.largura_vao_mm, dados.altura_vao_mm)
    elif dados.tipo_calculo == "sacada_l":
        resultado = CalculadoraVidro.calcular_sacada_em_l(dados.largura_vao_mm, dados.largura_lado_b_mm, dados.altura_vao_mm, dados.qtd_pecas, dados.qtd_pecas_lado_b)
    else:
        resultado = CalculadoraVidro.calcular_pecas_sacada_reta(dados.largura_vao_mm, dados.altura_vao_mm, dados.qtd_pecas)

    novo_orcamento = Orcamento(
        empresa_id=empresa.id,
        cliente_nome="Cliente Exemplo",
        cliente_whatsapp="(11) 99999-9999",
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
        dados_cliente={"nome": "Cliente Exemplo", "whatsapp": "(11) 99999-9999"},
        especificacoes={"cor_vidro": dados.cor_vidro, "espessura": dados.espessura_vidro, "cor_aluminio": dados.cor_aluminio},
        resultado_corte=resultado,
    )
    return FileResponse(caminho_pdf, media_type="application/pdf", filename=f"contrato_{novo_orcamento.id}.pdf")

@router.get("/", status_code=status.HTTP_200_OK)
def listar_historico_orcamentos(empresa: Empresa = Depends(obter_empresa_logada), db: Session = Depends(get_db)):
    orcamentos = db.query(Orcamento).filter(Orcamento.empresa_id == empresa.id).order_by(Orcamento.criado_em.desc()).all()
    return [{"id": o.id, "cliente_nome": o.cliente_nome, "medida_corte_resumo": o.medida_corte_resumo, "criado_em": o.criado_em} for o in orcamentos]
