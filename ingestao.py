import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

def importar_para_categoria(df: pd.DataFrame, categoria: str):
    """Insere os dados da planilha no banco de dados na tabela da categoria"""
    db_url = os.getenv("DB_URL")
    engine = create_engine(db_url)
    
    nome_tabela = categoria.lower()
    df.to_sql(nome_tabela, con=engine, if_exists='append', index=False)
    print(f"✅ Dados inseridos na tabela '{nome_tabela}' com sucesso!")
