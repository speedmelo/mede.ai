from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticação"])

SECRET_KEY = "mede_ai_secret_key_super_segura_melo_ai"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
  return pwd_context.verify(senha_pura, senha_hash)


def gerar_hash_senha(senha: str) -> str:
  return pwd_context.hash(senha)


def criar_token_acesso(dados: dict) -> str:
  to_encode = dados.copy()
  expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expira})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
  usuario = (
      db.query(Usuario).filter(Usuario.email == form_data.username).first()
  )
  if not usuario or not verificar_senha(
      form_data.password, usuario.senha_hash
  ):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="E-mail ou senha incorretos",
    )

  access_token = criar_token_acesso(
      dados={
          "sub": usuario.email,
          "empresa_id": usuario.empresa_id,
          "cargo": usuario.cargo,
      }
  )

  return {
      "access_token": access_token,
      "token_type": "bearer",
      "empresa_id": usuario.empresa_id,
      "nome": usuario.nome,
  }