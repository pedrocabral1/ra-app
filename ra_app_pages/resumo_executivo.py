import streamlit as st
import pandas as pd

# Função para exibir a página de Resumo Executivo com ajustes no layout
def show_resumo_executivo():
    st.title("Resumo Executivo das Reclamações 📋")

    # Certifique-se de que os dados foram carregados no `st.session_state`
    if 'data' in st.session_state:
        df = st.session_state['data']

        # Verificar se as colunas esperadas existem no DataFrame
        colunas_necessarias = ['empresa', 'estado', 'cidade', 'status', 'casos', 'bandeira', 'logo']
        for coluna in colunas_necessarias:
            if coluna not in df.columns:
                st.error(f"Coluna esperada '{coluna}' não encontrada nos dados. Verifique a estrutura dos dados carregados.")
                st.stop()

        # Adicionar a opção "Todos" para as seleções de estado e cidade
        df['estado'] = df['estado'].fillna('Todos')
        df['cidade'] = df['cidade'].fillna('Todos')

        # Acrescentar "Todos" no início das listas de seleção
        empresas = ['Todos'] + sorted(df['empresa'].unique().tolist())
        estados = ['Todos'] + sorted(df['estado'].unique().tolist())
        cidades = ['Todos'] + sorted(df['cidade'].unique().tolist())

        # Calcular totalizadores gerais, que não são influenciados pelos filtros
        total_reclamacoes_geral = df['casos'].sum()
        total_status = df['status'].value_counts()

        st.markdown("---")

        # Layout dos filtros lado a lado (Empresa, Estado, Cidade)
        col4, col5, col6 = st.columns([1, 1, 1])
        with col4:
            empresa = st.selectbox("Selecione a Empresa", empresas, index=0)
        with col5:
            estado = st.selectbox("Selecione o Estado", estados, index=0)
        with col6:
            cidade = st.selectbox("Selecione a Cidade", cidades, index=0)

        # Filtragem dos dados conforme a seleção (empresa, estado, cidade)
        df_filtered = df.copy()
        if empresa != 'Todos':
            df_filtered = df_filtered[df_filtered['empresa'] == empresa]
        if estado != 'Todos':
            df_filtered = df_filtered[df_filtered['estado'] == estado]
        if cidade != 'Todos':
            df_filtered = df_filtered[df_filtered['cidade'] == cidade]

        # Calcular total de reclamações apenas para a empresa selecionada (não influenciado por estado e cidade)
        total_reclamacoes_empresa = df[df['empresa'] == empresa]['casos'].sum() if empresa != 'Todos' else total_reclamacoes_geral

        # Exibir total de reclamações filtradas por empresa em uma caixa de texto entre bandeira e logo
        st.markdown(f"<div style='text-align: center; background-color: #f0f0f0; padding: 10px; font-size: 20px;'><strong>Total de Reclamações para {empresa}: {total_reclamacoes_empresa}</strong></div>", unsafe_allow_html=True)

        st.markdown("---")

        # Calcular o total por status
        ranking_status = pd.DataFrame(total_status).reset_index()
        ranking_status.columns = ['Status', 'Número de Casos']

        # Ranking de estados e cidades
        ranking_estados = df['estado'].value_counts().reset_index()
        ranking_estados.columns = ['Estado', 'Número de Reclamações']

        ranking_cidades = df_filtered['cidade'].value_counts().reset_index()
        ranking_cidades.columns = ['Cidade', 'Número de Reclamações']

        # Exibição dos Rankings e Total por Status lado a lado
        col7, col8, col9 = st.columns([1, 1, 1])
        with col7:
            st.subheader("Ranking por Estado")
            st.dataframe(ranking_estados, height=300)

        with col8:
            st.subheader("Ranking por Cidade")
            st.dataframe(ranking_cidades, height=300)

        with col9:
            st.subheader("Total por Status")
            st.dataframe(ranking_status, height=300)

    else:
        st.warning("Dados não carregados. Por favor, carregue os dados antes de acessar esta página.")

