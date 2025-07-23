# 📊 Leitor de Planilhas Interativo

Um dashboard web dinâmico para importar, visualizar e analisar planilhas de qualquer estrutura, com gráficos automáticos e filtros inteligentes.  
Ideal para explorar dados de Excel/CSV de forma simples e visual!

---

## ✨ Funcionalidades

- **Cadastro e login de usuários**
- **Criação de abas personalizadas**: defina as colunas que sua planilha deve ter
- **Upload de planilhas** (`.xlsx` ou `.csv`) para cada aba
- **Validação automática da estrutura** da planilha
- **Visualização de dados em tabela**
- **Gráficos dinâmicos**: barras, pizza e linha, escolhendo as colunas na interface
- **Reconhecimento automático de colunas de data** para gráficos de linha
- **Multiusuário**: cada usuário vê apenas suas abas e dados

---

## 🚀 Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/Leitor-de-Planilhas.git
cd Leitor-de-Planilhas
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
# Ative no Windows:
venv\Scripts\activate
# Ou no Linux/Mac:
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Rode a aplicação

```bash
streamlit run app.py
```

Acesse no navegador: [http://localhost:8501](http://localhost:8501)

---

## 📝 Como usar

1. **Crie uma conta** na tela inicial.
2. **Crie uma nova aba**: dê um nome, descrição e defina a estrutura das colunas em JSON.  
   Exemplo para clientes:
   ```json
   {"colunas": ["Nome", "Email", "DataCadastro"]}
   ```
   Exemplo para financeiro:
   ```json
   {"colunas": ["Data", "Categoria", "Valor"]}
   ```
3. **Faça upload de uma planilha** com as colunas exatamente como definidas na aba.
4. **Visualize os dados**: veja a tabela e escolha o tipo de gráfico (barras, pizza, linha).  
   - Para gráfico de linha, basta ter uma coluna de data (ex: `Data` ou `DataCadastro`).
   - Para pizza e barras, escolha as colunas desejadas na interface.
5. **Explore!** Filtros e gráficos são dinâmicos conforme sua planilha.

---

## 📂 Exemplos de estrutura de colunas

Veja o arquivo `categorias.json` para exemplos prontos:

```json
{
  "Financeiro": ["Data", "Categoria", "Valor"],
  "Clientes": ["Nome", "Email", "DataCadastro"]
}
```

---

## 🛠️ Tecnologias

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Plotly](https://plotly.com/python/)
- [SQLite](https://www.sqlite.org/index.html)
- [bcrypt](https://pypi.org/project/bcrypt/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 🤝 Contribuição

Sinta-se à vontade para abrir issues ou pull requests!

---
