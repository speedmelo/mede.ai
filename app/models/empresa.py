from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nome_fantasia = Column(String(150), nullable=False)
    cnpj = Column(String(20), unique=True, index=True, nullable=False)
    preco_m2_base = Column(Float, default=350.0)
    desconto_altura_padrao_cm = Column(Float, default=16.0)
    caminho_contrato_pdf = Column(String(255), nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)

    usuarios = relationship("Usuario", back_populates="empresa")
    orcamentos = relationship("Orcamento", back_populates="empresa")
