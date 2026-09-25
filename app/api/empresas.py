from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.api.auth import gerar_hash_senha
from app.database import get_db
from app.models.empresa import Empresa
from app.models.usuario import TipoUsuario, Usuario

router = APIRouter(prefix="/api/v1/empresas", tags=["Empresas B2B"])


class RegistroEmpresaSchema(BaseModel):
  nome_fantasia: str
  cnpj: str
  email_admin: EmailStr
  senha_admin: str
  nome_admin: str


@router.post("/cadastrar", status_code=status.HTTP_201_CREATED)
def cadastrar_empresa(dados: RegistroEmpresaSchema, db: Session = Depends(get_db)):
  # Verificar se CNPJ já existe
  if db.query(Empresa).filter(Empresa.cnpj == dados.cnpj).first():
    raise HTTPException(
        status_code=400, detail="CNPJ já cadastrado no Mede.ai"
    )

  # Criar a Vidraçaria
  nova_empresa = Empresa(
      nome_fantasia=dados.nome_fantasia,
      cnpj=dados.cnpj,
  )
  db.add(nova_empresa)
  db.commit()
  db.refresh(nova_empresa)

  # Criar o Usuário Administrador vinculado a ela
  admin_user = Usuario(
      empresa_id=nova_empresa.id,
      nome=dados.nome_admin,
      email=dados.email_admin,
      senha_hash=gerar_hash_senha(dados.senha_admin),
      cargo=TipoUsuario.ADMIN,
  )
  db.add(admin_user)
  db.commit()

  return {
      "mensagem": "Empresa e Administrador cadastrados com sucesso!",
      "empresa_id": nova_empresa.id,
      "nome_fantasia": nova_empresa.nome_fantasia,
  }
