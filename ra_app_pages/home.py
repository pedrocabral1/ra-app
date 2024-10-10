# ra_app_pages/home.py
import streamlit as st

def show_home():
    st.title("Bem-vindo ao Projeto Dashboard Reclame Aqui 📊")

    st.markdown("""
        ### Sobre o Projeto
        O projeto visa a criação de um dashboard interativo para visualização e análise das reclamações registradas pelas empresas no Reclame Aqui.

        ### Navegação
        - **Página Inicial**: Apresenta o propósito do projeto e informações gerais.
        - **Resumo Executivo**: Resumo geral das reclamações com totalizadores e filtros por empresa, estado e cidade.
        - **Dashboard**: Gráficos interativos para análise detalhada dos dados.

        ### Objetivo
        Facilitar a visualização das reclamações e permitir um entendimento mais profundo do comportamento dos clientes e das áreas de melhoria para as empresas.
    """)