import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv
import json
import os
from ingestao import importar_para_categoria

# Carrega variáveis do .env
load_dotenv()
db_url = os.getenv("DB_URL")
engine = create_engine(db_url)

# Carrega categorias e colunas esperadas
with open("categorias.json", "r", encoding="utf-8") as f:
    categorias = json.load(f)

# Sidebar para escolher categoria
categoria = st.sidebar.selectbox("📁 Escolha uma categoria de planilha", list(categorias.keys()))
st.title(f"📊 Dashboard - Categoria: {categoria}")

# Upload da planilha
uploaded_file = st.file_uploader("📂 Envie uma planilha para essa categoria", type=["xlsx", "csv"], key=categoria)

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("📋 Prévia dos Dados")
        st.dataframe(df)

        # Validação simples de colunas
        colunas_esperadas = categorias[categoria]
        if all(col in df.columns for col in colunas_esperadas):
            importar_para_categoria(df, categoria)
            st.success("✅ Dados enviados ao banco com sucesso!")
        else:
            st.error(f"❌ Colunas esperadas: {colunas_esperadas}. Corrija a planilha e envie novamente.")

    except Exception as e:
        st.error(f"Erro ao processar planilha: {e}")

# Mostrar dados e gráfico
try:
    df = pd.read_sql(f"SELECT * FROM {categoria.lower()}", con=engine)
    
    if not df.empty:
        st.subheader("📈 Gerar Gráficos")
        col_x = st.selectbox("Eixo X", df.columns)
        col_y = st.selectbox("Eixo Y", df.columns)
        tipo = st.selectbox("Tipo de Gráfico", ["Barra", "Pizza", "Linha"])

        if tipo == "Barra":
            fig = px.bar(df, x=col_x, y=col_y)
        elif tipo == "Pizza":
            fig = px.pie(df, names=col_x, values=col_y)
        elif tipo == "Linha":
            fig = px.line(df, x=col_x, y=col_y)

        st.plotly_chart(fig)
except Exception as e:
    st.warning("⚠️ Nenhum dado disponível para esta categoria ainda.")
