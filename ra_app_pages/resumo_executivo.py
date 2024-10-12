import streamlit as st
import pandas as pd
import plotly.express as px

# Função para verificar se todas as colunas necessárias estão no DataFrame
def verificar_colunas(df, colunas_necessarias):
    colunas_faltando = [col for col in colunas_necessarias if col not in df.columns]
    if colunas_faltando:
        st.error(f"Colunas faltando nos dados: {', '.join(colunas_faltando)}. Verifique a estrutura dos dados.")
        st.stop()

# Função para filtragem dos dados
def filtrar_dados(df, empresa='Todos', estado='Todos', cidade='Todos', status='Todos', tamanho_min=0):
    df_filtered = df.copy()
    if empresa != 'Todos':
        df_filtered = df_filtered[df_filtered['empresa'] == empresa]
    if estado != 'Todos':
        df_filtered = df_filtered[df_filtered['estado'] == estado]
    if cidade != 'Todos':
        df_filtered = df_filtered[df_filtered['cidade'] == cidade]
    if status != 'Todos':
        df_filtered = df_filtered[df_filtered['status'] == status]
    df_filtered = df_filtered[df_filtered['descrição'].str.len() >= tamanho_min]
    return df_filtered

# Função para exibir a página de Resumo Executivo
def show_resumo_executivo():
    st.title("Resumo Executivo das Reclamações 📋")

    if 'data' in st.session_state:
        df = st.session_state['data']

        colunas_necessarias = ['empresa', 'estado', 'cidade', 'status', 'casos', 'bandeira', 'logo']
        verificar_colunas(df, colunas_necessarias)

        df['estado'] = df['estado'].fillna('Todos')
        df['cidade'] = df['cidade'].fillna('Todos')

        empresas = ['Todos'] + sorted(df['empresa'].unique().tolist())
        estados = ['Todos'] + sorted(df['estado'].unique().tolist())
        cidades = ['Todos'] + sorted(df['cidade'].unique().tolist())

        total_reclamacoes_geral = df['casos'].sum()

        col4, col5, col6 = st.columns(3)
        with col4:
            empresa = st.selectbox("Selecione a Empresa", empresas)
        with col5:
            estado = st.selectbox("Selecione o Estado", estados)
        with col6:
            cidade = st.selectbox("Selecione a Cidade", cidades)

        df_filtered = filtrar_dados(df, empresa, estado, cidade)

        total_reclamacoes_empresa = df[df['empresa'] == empresa]['casos'].sum() if empresa != 'Todos' else total_reclamacoes_geral
        st.markdown(f"<div style='text-align: center; background-color: #f0f0f0; padding: 10px; font-size: 20px;'>"
                    f"<strong>Total de Reclamações para {empresa}: {total_reclamacoes_empresa}</strong></div>",
                    unsafe_allow_html=True)

        st.markdown("---")

        total_status = df['status'].value_counts().reset_index()
        total_status.columns = ['Status', 'Número de Casos']

        ranking_estados = df['estado'].value_counts().reset_index()
        ranking_estados.columns = ['Estado', 'Número de Reclamações']

        ranking_cidades = df_filtered['cidade'].value_counts().reset_index()
        ranking_cidades.columns = ['Cidade', 'Número de Reclamações']

        col7, col8, col9 = st.columns(3)
        with col7:
            st.subheader("Ranking por Estado")
            st.dataframe(ranking_estados, height=300)
        with col8:
            st.subheader("Ranking por Cidade")
            st.dataframe(ranking_cidades, height=300)
        with col9:
            st.subheader("Total por Status")
            st.dataframe(total_status, height=300)
    else:
        st.warning("Dados não carregados. Por favor, carregue os dados antes de acessar esta página.")

# Função para exibir a página do Dashboard
def show_dashboard():
    st.title("Dashboard Interativo 🗂️")

    if 'data' in st.session_state:
        df = st.session_state['data']

        colunas_necessarias = ['empresa', 'estado', 'data', 'casos', 'descrição', 'status']
        verificar_colunas(df, colunas_necessarias)

        empresas = ['Todos'] + sorted(df['empresa'].unique().tolist())
        estados = ['Todos'] + sorted(df['estado'].unique().tolist())
        status_options = ['Todos'] + sorted(df['status'].unique().tolist())

        col1, col2, col3 = st.columns(3)
        with col1:
            empresa = st.selectbox("Selecione a Empresa", empresas)
        with col2:
            estado = st.selectbox("Selecione o Estado", estados)
        with col3:
            status = st.selectbox("Selecione o Status", status_options)

        tamanho_min = st.slider("Selecione o Tamanho Mínimo do Texto das Descrições", min_value=0, 
                                max_value=int(df['descrição'].str.len().max()), value=0)

        df_filtered = filtrar_dados(df, empresa, estado, status=status, tamanho_min=tamanho_min)

        if empresa == 'Todos':
            empresas_unicas = df['empresa'].unique().tolist()
            col4, col5, col6 = st.columns(3)
            for idx, emp in enumerate(empresas_unicas):
                emp_data = df_filtered[df_filtered['empresa'] == emp]
                fig = px.line(emp_data, x='data', y='casos', title=f'Série Temporal - Reclamações de {emp}')
                [col4, col5, col6][idx % 3].plotly_chart(fig, use_container_width=True)
        else:
            fig_tempo = px.line(df_filtered, x='data', y='casos', 
                                title=f'Série Temporal - Reclamações de {empresa} em {estado if estado != "Todos" else "Todos os Estados"}')
            st.plotly_chart(fig_tempo, use_container_width=True)

        col7, col8 = st.columns(2)
        with col7:
            fig_status = px.histogram(df_filtered, x='status', y='casos', 
                                      title=f'Frequência de Reclamações por Status - {empresa}')
            st.plotly_chart(fig_status)
        with col8:
            df_filtered['tamanho_descricao'] = df_filtered['descrição'].apply(len)
            fig_tamanho = px.histogram(df_filtered, x='tamanho_descricao', nbins=50, 
                                       title=f'Distribuição do Tamanho das Descrições - {empresa}')
            st.plotly_chart(fig_tamanho)

        fig_estado = px.histogram(df_filtered, x='estado', y='casos', 
                                  title=f'Frequência de Reclamações por Estado - {empresa}')
        st.plotly_chart(fig_estado, use_container_width=True)
    else:
        st.warning("Dados não carregados. Por favor, carregue os dados antes de acessar esta página.")


