from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Orcamento(Base):
    __tablename__ = "orcamentos"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cliente_nome = Column(String(100), nullable=False)
    cliente_whatsapp = Column(String(20), nullable=True)
    largura_vao_mm = Column(Float, nullable=False)
    altura_vao_mm = Column(Float, nullable=False)
    qtd_pecas = Column(Integer, nullable=False)
    cor_vidro = Column(String(50), default="Incolor")
    espessura_vidro = Column(String(50), default="10mm Laminado")
    cor_aluminio = Column(String(50), default="RAL 9007")
    valor_total = Column(Float, nullable=False)
    detalhes_corte_json = Column(JSON, nullable=True)
    url_contrato_assinado = Column(String(255), nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)

    empresa = relationship("Empresa", back_populates="orcamentos")
    usuario = relationship("Usuario", back_populates="orcamentos")
