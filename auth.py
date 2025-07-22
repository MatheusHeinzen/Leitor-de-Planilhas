from db import get_db, Usuario
from sqlalchemy.exc import IntegrityError
import bcrypt
from sqlalchemy.orm import Session
from typing import Optional

def criar_usuario(username: str, email: str, senha: str) -> Usuario:
    """Cria um novo usuário no banco de dados."""
    try:
        hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        with get_db() as db:
            db_user = Usuario(username=username, email=email, hashed_password=hashed_password)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
    except IntegrityError:
        raise ValueError("Usuário ou email já existe")
    except Exception as e:
        raise RuntimeError(f"Erro ao criar usuário: {e}")

def autenticar_usuario(username: str, senha: str) -> Optional[Usuario]:
    """Autentica um usuário pelo username e senha."""
    with get_db() as db:
        usuario = db.query(Usuario).filter(Usuario.username == username).first()
        if not usuario or not bcrypt.checkpw(senha.encode('utf-8'), usuario.hashed_password.encode('utf-8')):
            return None
        return usuario

def get_usuario(usuario_id: int) -> Optional[Usuario]:
    """Obtém um usuário pelo ID."""
    with get_db() as db:
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def main():
    """Função principal do app Streamlit."""
    try:
        if 'usuario' not in st.session_state:
            if 'criar_conta' in st.session_state:
                mostrar_criar_conta()
            else:
                mostrar_login()
        else:
            mostrar_dashboard()
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    if not os.path.exists("dados"):
        os.makedirs("dados")
    main()