# Instala o plotly manualmente se não estiver disponível
import streamlit as st
import sys
import pandas as pd
from pathlib import Path

# Verifica se os dados já foram carregados no estado da sessão
if "data" not in st.session_state:
    # Carrega o arquivo `dados_processados.csv` utilizando caminho relativo
    df_data = pd.read_csv("ra_app_dataset/dados_processados.csv", sep=";")
    
    # Armazena os dados no estado da sessão
    st.session_state["data"] = df_data

# Acessa os dados armazenados na sessão
df_data = st.session_state["data"]

# Adiciona o diretório 'ra_app_pages' ao sys.path para garantir que o Python consiga encontrar os módulos.
sys.path.append(str(Path(__file__).resolve().parent / 'ra_app_pages'))

# Definição das configurações iniciais da página
st.set_page_config(
    page_title="Projeto Reclame Aqui",
    page_icon="📊",
    layout="wide"
)

# Controle de navegação entre as páginas usando a barra lateral
page = st.sidebar.radio("Navegação", ["Página Inicial", "Resumo Executivo", "Dashboard"])

# Importar os módulos de cada página e exibir conforme a navegação
if page == "Página Inicial":
    # Importa o módulo 'home' e chama a função 'show_home()'
    from home import show_home
    show_home()

elif page == "Resumo Executivo":
    # Importa o módulo 'resumo_executivo' e chama a função 'show_resumo_executivo()'
    from resumo_executivo import show_resumo_executivo
    show_resumo_executivo()

elif page == "Dashboard":
    # Importa o módulo 'dashboard' e chama a função 'show_dashboard()'
    from dashboard import show_dashboard
    show_dashboard()
