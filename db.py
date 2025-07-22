from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from sqlalchemy.sql import func
import os
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

Base = declarative_base()

class Usuario(Base):
    """Modelo de usuário do sistema."""
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    abas = relationship("Aba", back_populates="dono")

class Aba(Base):
    """Modelo de aba (planilha) associada a um usuário."""
    __tablename__ = 'abas'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String)
    estrutura = Column(String)  # JSON com a estrutura esperada
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    dono = relationship("Usuario", back_populates="abas")

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///dashboard.db')
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if 'sqlite' in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db() -> Session:
    """Context manager para obter uma sessão do banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def criar_tabelas():
    """Cria todas as tabelas no banco de dados."""
    Base.metadata.create_all(bind=engine)

# Garante que as tabelas existam ao importar o módulo
def _garante_tabelas():
    criar_tabelas()
_garante_tabelas()