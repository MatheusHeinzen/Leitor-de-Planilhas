from sqlalchemy import create_engine
import streamlit as st
from db import criar_tabelas, get_db, Usuario, Aba
from auth import criar_usuario, autenticar_usuario, get_usuario
from ingestao import processar_planilha
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
from sqlalchemy.orm import Session

# Configuração inicial
st.set_page_config(page_title="Meu Dashboard", layout="wide")
criar_tabelas()

# Funções auxiliares
def mostrar_login():
    st.title("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    
    if st.button("Entrar"):
        # db = get_db()
        # try:
        #     usuario = autenticar_usuario(username, password)
        #     if usuario:
        #         st.session_state['usuario'] = usuario
        #         st.rerun()
        #     else:
        #         st.error("Usuário ou senha incorretos")
        # finally:
        #     db.close()
        usuario = autenticar_usuario(username, password)
        if usuario:
            st.session_state['usuario'] = usuario
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos")
    
    if st.button("Criar conta"):
        st.session_state['criar_conta'] = True
        st.rerun()

def mostrar_criar_conta():
    st.title("Criar Conta")
    username = st.text_input("Usuário")
    email = st.text_input("Email")
    password = st.text_input("Senha", type="password")
    confirm_password = st.text_input("Confirmar Senha", type="password")
    
    if st.button("Registrar"):
        if password != confirm_password:
            st.error("As senhas não coincidem")
        else:
            # db = get_db()
            # try:
            #     try:
            #         criar_usuario(username, email, password)
            #         st.success("Conta criada com sucesso! Faça login.")
            #         del st.session_state['criar_conta']
            #         st.rerun()
            #     except ValueError as e:
            #         st.error(str(e))
            # finally:
            #     db.close()
            try:
                criar_usuario(username, email, password)
                st.success("Conta criada com sucesso! Faça login.")
                del st.session_state['criar_conta']
                st.rerun()
            except ValueError as e:
                st.error(str(e))
    
    if st.button("Voltar para login"):
        del st.session_state['criar_conta']
        st.rerun()

def mostrar_dashboard():
    usuario = st.session_state['usuario']
    st.sidebar.title(f"Bem-vindo, {usuario.username}")
    
    # Menu lateral
    opcao = st.sidebar.radio(
        "Menu",
        ["Minhas Abas", "Nova Aba", "Upload de Dados", "Visualização", "Configurações"]
    )
    
    # db = get_db()
    # try:
    with get_db() as db:
        if opcao == "Minhas Abas":
            st.title("Minhas Abas")
            abas = db.query(Aba).filter(Aba.usuario_id == usuario.id).all()
            
            for aba in abas:
                with st.expander(f"{aba.nome} - {aba.descricao}"):
                    st.write(f"Estrutura: {aba.estrutura}")
                    if st.button(f"Excluir {aba.nome}", key=f"del_{aba.id}"):
                        db.delete(aba)
                        db.commit()
                        st.rerun()
        
        elif opcao == "Nova Aba":
            st.title("Criar Nova Aba")
            nome = st.text_input("Nome da Aba")
            descricao = st.text_area("Descrição")
            estrutura = st.text_area("Estrutura (JSON)", value='{"colunas": ["data", "valor", "categoria"]}')
            
            if st.button("Criar Aba"):
                nova_aba = Aba(
                    nome=nome,
                    descricao=descricao,
                    estrutura=estrutura,
                    usuario_id=usuario.id
                )
                db.add(nova_aba)
                db.commit()
                st.success("Aba criada com sucesso!")
                st.rerun()
        
        elif opcao == "Upload de Dados":
            st.title("Upload de Dados")
            abas = db.query(Aba).filter(Aba.usuario_id == usuario.id).all()
            
            if not abas:
                st.warning("Crie uma aba primeiro!")
                return
                
            aba_selecionada = st.selectbox("Selecione a aba", abas, format_func=lambda x: x.nome)
            arquivo = st.file_uploader("Selecione a planilha", type=["xlsx", "csv"])
            
            if arquivo and aba_selecionada:
                # Salvar arquivo temporariamente
                caminho = os.path.join("dados", arquivo.name)
                with open(caminho, "wb") as f:
                    f.write(arquivo.getbuffer())
                
                try:
                    resultado = processar_planilha(aba_selecionada.id, caminho, usuario.id)
                    st.success(resultado["mensagem"])
                except ValueError as e:
                    st.error(str(e))
                finally:
                    os.remove(caminho)
        
        elif opcao == "Visualização":
            st.title("Visualização de Dados")
            abas = db.query(Aba).filter(Aba.usuario_id == usuario.id).all()
            
            if not abas:
                st.warning("Nenhuma aba disponível para visualização")
                return
                
            aba_selecionada = st.selectbox("Selecione a aba", abas, format_func=lambda x: x.nome)
            
            # Carregar dados
            engine = create_engine('sqlite:///dashboard.db')
            df = pd.read_sql_table(f"dados_{aba_selecionada.id}", engine)
            
            if not df.empty:
                st.dataframe(df)
                # Gráficos dinâmicos se houver pelo menos uma coluna numérica e uma categórica
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                date_cols = df.select_dtypes(include=['datetime', 'datetimetz']).columns.tolist()
                # Detecta colunas de data que são string, tenta converter
                for col in df.columns:
                    if col not in date_cols and df[col].dtype == 'object':
                        try:
                            converted = pd.to_datetime(df[col], errors='raise')
                            df[col] = converted
                            date_cols.append(col)
                        except Exception:
                            pass
                if numeric_cols and categorical_cols:
                    st.markdown('---')
                    st.subheader('Gráfico dinâmico')
                    tipo_grafico = st.selectbox('Tipo de gráfico', ['Barras', 'Pizza', 'Linha'], key='tipo_grafico')
                    if tipo_grafico == 'Barras':
                        x_col = st.selectbox('Coluna categórica (Eixo X)', categorical_cols, key='x_col_bar')
                        y_col = st.selectbox('Coluna numérica (Eixo Y)', numeric_cols, key='y_col_bar')
                        fig = px.bar(df, x=x_col, y=y_col, title=f'Gráfico de {y_col} por {x_col}')
                        st.plotly_chart(fig, use_container_width=True)
                    elif tipo_grafico == 'Pizza':
                        cat_col = st.selectbox('Coluna categórica (Rótulo)', categorical_cols, key='cat_col_pie')
                        val_col = st.selectbox('Coluna numérica (Valor)', numeric_cols, key='val_col_pie')
                        fig = px.pie(df, names=cat_col, values=val_col, title=f'Gráfico de Pizza: {val_col} por {cat_col}')
                        st.plotly_chart(fig, use_container_width=True)
                    elif tipo_grafico == 'Linha':
                        if date_cols:
                            x_col = st.selectbox('Coluna de data (Eixo X)', date_cols, key='x_col_line')
                            y_col = st.selectbox('Coluna numérica (Eixo Y)', numeric_cols, key='y_col_line')
                            fig = px.line(df.sort_values(x_col), x=x_col, y=y_col, title=f'Gráfico de Linha: {y_col} ao longo de {x_col}')
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning('Nenhuma coluna de data reconhecida para gráfico de linha.')
                else:
                    st.info("Apenas visualização de tabela disponível para esta aba.")
            else:
                st.warning("Nenhum dado disponível nesta aba")
        
        elif opcao == "Configurações":
            st.title("Configurações da Conta")
            st.write(f"Usuário: {usuario.username}")
            st.write(f"Email: {usuario.email}")
            
            if st.button("Sair"):
                del st.session_state['usuario']
                st.rerun()

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