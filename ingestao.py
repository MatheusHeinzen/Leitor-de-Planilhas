import pandas as pd
from sqlalchemy import create_engine
from db import Base, get_db, Aba  # Importa Aba
import os
from datetime import datetime
import json  # Importa json


def processar_planilha(aba_id: int, caminho_arquivo: str, usuario_id: int):
    # Carregar planilha
    try:
        df = pd.read_excel(caminho_arquivo) if caminho_arquivo.endswith('.xlsx') else pd.read_csv(caminho_arquivo)
    except Exception as e:
        raise ValueError(f"Erro ao ler arquivo: {str(e)}")
    
    # Buscar estrutura da aba no banco
    with get_db() as db:
        aba = db.query(Aba).filter(Aba.id == aba_id).first()
        if not aba:
            raise ValueError("Aba não encontrada")
        try:
            estrutura = json.loads(aba.estrutura)
            colunas_esperadas = estrutura.get("colunas", [])
        except Exception as e:
            raise ValueError(f"Estrutura da aba inválida: {e}")
    
    # Validar estrutura
    if not all(col in df.columns for col in colunas_esperadas):
        raise ValueError(f"Estrutura da planilha incompatível com a aba. Esperado: {colunas_esperadas}, encontrado: {list(df.columns)}")
    
    # Adicionar metadados
    df['aba_id'] = aba_id
    df['usuario_id'] = usuario_id
    df['importado_em'] = datetime.now()
    
    # Salvar no banco de dados
    engine = create_engine('sqlite:///dashboard.db')
    nome_tabela = f"dados_{aba_id}"
    df.to_sql(nome_tabela, engine, if_exists='append', index=False)
    
    return {"mensagem": f"Dados importados com sucesso para a aba {aba_id}", "registros": len(df)}