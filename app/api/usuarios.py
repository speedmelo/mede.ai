from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List
from sqlalchemy.orm import Session
from app.api.auth import oauth2_scheme, gerar_hash_senha, ALGORITHM, SECRET_KEY
from app.database import get_db
from app.models.empresa import Empresa
from app.models.usuario import Usuario, TipoUsuario
from jose import jwt, JWTError

router = APIRouter(prefix="/api/v1/usuarios", tags=["Equipe e Tecnicos B2B"])

class CadastrarTecnicoSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str

def obter_admin_logado(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_email = payload.get("sub")
        if not usuario_email:
            raise HTTPException(status_code=401, detail="Token invalido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expirado ou invalido")
    usuario = db.query(Usuario).filter(Usuario.email == usuario_email).first()
    if not usuario or usuario.cargo != TipoUsuario.ADMIN:
        raise HTTPException(status_code=403, detail="Acesso permitido apenas para Administradores da vidracaria")
    return usuario

@router.post("/tecnicos", status_code=status.HTTP_201_CREATED)
def cadastrar_tecnico(dados: CadastrarTecnicoSchema, admin: Usuario = Depends(obter_admin_logado), db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.email == dados.email).first():
        raise HTTPException(status_code=400, detail="E-mail ja cadastrado no sistema")
    novo_tecnico = Usuario(
        empresa_id=admin.empresa_id,
        nome=dados.nome,
        email=dados.email,
        senha_hash=gerar_hash_senha(dados.senha),
        cargo=TipoUsuario.TECNICO
    )
    db.add(novo_tecnico)
    db.commit()
    db.refresh(novo_tecnico)
    return {"mensagem": "Tecnico cadastrado com sucesso!", "id": novo_tecnico.id, "nome": novo_tecnico.nome, "email": novo_tecnico.email}

@router.get("/", status_code=status.HTTP_200_OK)
def listar_equipe(admin: Usuario = Depends(obter_admin_logado), db: Session = Depends(get_db)):
    equipe = db.query(Usuario).filter(Usuario.empresa_id == admin.empresa_id).all()
    return [{"id": u.id, "nome": u.nome, "email": u.email, "cargo": u.cargo, "criado_em": u.criado_em} for u in equipe]
