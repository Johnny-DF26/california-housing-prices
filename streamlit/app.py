import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==========================================
# CONFIGURAÇÃO DA PÁGINA (DESIGN MODERNO)
# ==========================================
st.set_page_config(
    page_title="Dashboard Strategic California Land Partners (SCLP) - California Prices",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS customizada para visual mais "clean"
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div[data-testid="stMetricValue"] { font-size: 2rem; font-weight: 700; color: #1E3A8A; }
    .stButton>button { background-color: #2563EB; color: white; border-radius: 8px; width: 100%; }
    .stButton>button:hover { background-color: #1D4ED8; color: white; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# CARREGAMENTO DE DADOS (CACHE)
# ==========================================
@st.cache_data
def load_data():
    
    df = pd.read_csv('../data/housing.csv')
    return df

df_raw = load_data()

st.dataframe(df_raw.head(), use_container_width=True)

# ==========================================
# NAVEGAÇÃO LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.image("https://flaticon.com", width=80)
    st.title("Menu do Projeto")
    st.markdown("Navegue pelas etapas do modelo de regressão.")
    
    # Sistema de abas no menu lateral
    page = st.radio(
        "Ir para:",
        ["📊 Dashboard Interativo", "📁 Dados Brutos & Filtros", "🔮 Simulador de Previsão"]
    )
    
    st.markdown("---")
    st.markdown("**Autor:** Johnny")
    st.markdown("**Modelo:** Dashboard Strategic California Land Partners (SCLP)")

# ==========================================
# PÁGINA 1: DASHBOARD INTERATIVO
# ==========================================
if page == "📊 Dashboard Interativo":
    st.title("📊  Dashboard Interativo", text_alignment='center')
    st.markdown("---")
    #st.subheader("Visão geral sobre as características e preços dos imóveis na Califórnia", text_alignment='center')
    
    # KPIs principais (Cards)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Preço Médio", value=f"${df_raw['median_house_value'].mean():,.2f}".replace('.','X').replace(',','.').replace('X',','))
    with col2:
        st.metric(label="Idade Média das Casas", value=f"{df_raw['housing_median_age'].mean():.0f} anos")
    with col3:
        st.metric(label="Renda Média da Região", value=f"${df_raw['median_income'].mean():.2f}Mil")
    with col4:
        st.metric(label="População Total Analisada", value=f"{int(df_raw['population'].sum()):,}".replace('.','X').replace(',','.').replace('X',','))

    st.markdown("---")

    # Layout de Gráficos (Grid)
    g1, g2 = st.columns(2)
    
    with g1:
        '''st.markdown("### Distribuição dos Preços dos Imóveis")
        fig_hist = px.histogram(df_raw, x="Preco_Mediano", nbins=50, 
                                color_discrete_sequence=['#2563EB'], template="plotly_white")
        st.plotly_chart(fig_hist, use_container_width=True)'''
        
    with g2:
        '''st.markdown("### Renda vs Preço do Imóvel")
        # Amostra de 1000 pontos apenas para manter o gráfico leve e interativo
        df_sample = df_raw.sample(1000, random_state=42)
        fig_scatter = px.scatter(df_sample, x="Renda_Mediana", y="Preco_Mediano", 
                                 trendline="ols", color="Idade_Casa", template="plotly_white")
        st.plotly_chart(fig_scatter, use_container_width=True)'''

# ==========================================
# PÁGINA 2: DADOS BRUTOS & FILTROS
# ==========================================
elif page == "📁 Dados Brutos & Filtros":
    st.title("📁 Exploração de Dados")
    st.subheader("Filtre e exporte os dados utilizados no desenvolvimento do modelo")
    
    # Container para filtros dinâmicos na barra superior
    st.markdown("#### Ajuste os filtros abaixo para refinar a tabela:")
    f_col1, f_col2 = st.columns(2)
    
    with f_col1:
        # Filtro por Idade da Casa
        min_age, max_age = int(df_raw['Idade_Casa'].min()), int(df_raw['Idade_Casa'].max())
        idade_selecionada = st.slider("Idade da Casa (Anos):", min_age, max_age, (min_age, max_age))
        
    with f_col2:
        # Filtro por Faixa de Preço
        min_p, max_p = float(df_raw['Preco_Mediano'].min()), float(df_raw['Preco_Mediano'].max())
        preco_selecionado = st.slider("Preço Máximo/Mínimo ($):", min_p, max_p, (min_p, max_p))
        
    # Aplicando os filtros ao dataframe
    df_filtrado = df_raw[
        (df_raw['Idade_Casa'] >= idade_selecionada[0]) & (df_raw['Idade_Casa'] <= idade_selecionada[1]) &
        (df_raw['Preco_Mediano'] >= preco_selecionado[0]) & (df_raw['Preco_Mediano'] <= preco_selecionado[1])
    ]
    
    # Exibição do Dataframe interativo
    st.markdown(f"Exibindo **{df_filtrado.shape[0]}** registros encontrados:")
    st.dataframe(df_filtrado, use_container_width=True, height=400)
    
    # Botão de download
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar Dados Filtrados (CSV)", data=csv, file_name="dados_california_filtrados.csv", mime="text/csv")

# ==========================================
# PÁGINA 3: SIMULADOR DE PREVISÃO
# ==========================================
elif page == "🔮 Simulador de Previsão":
    st.title("🔮 Preditor de Preço de Casas")
    st.subheader("Insira as características do imóvel para simular o valor de venda estimado")
    
    # Layout em duas colunas para o formulário de inputs
    with st.form("form_previsao"):
        st.markdown("### 🏠 Características do Imóvel")
        c1, c2 = st.columns(2)
        
        with c1:
            renda = st.number_input("Renda Mediana da Região (em dezenas de milhares de $)", min_value=0.5, max_value=15.0, value=3.5, step=0.1)
            idade = st.slider("Idade do Imóvel (Anos)", min_value=1, max_value=52, value=25)
            comodos = st.number_input("Média de Cômodos por Residência", min_value=1.0, max_value=10.0, value=5.0, step=0.5)
            quartos = st.number_input("Média de Quartos por Residência", min_value=0.5, max_value=5.0, value=1.0, step=0.1)
            
        with c2:
            populacao = st.number_input("População do Bloco/Bairro", min_value=3, max_value=35000, value=1400)
            ocupacao = st.number_input("Média de Moradores por Casa", min_value=1.0, max_value=6.0, value=3.0, step=0.1)
            latitude = st.number_input("Latitude da Localização", value=35.6)
            longitude = st.number_input("Longitude da Localização", value=-119.5)
            
        # Botão de submissão do formulário
        submetido = st.form_submit_button("Calcular Preço Estimado")
        
    # Lógica de cálculo após clicar no botão
    if submetido:
        # ----------------------------------------------------
        # NOTA: Insira a chamada do seu modelo treinado aqui!
        # Exemplo: dados_novos = [[renda, idade, comodos, quartos, populacao, ocupacao, latitude, longitude]]
        #          preco_predito = seu_modelo.predict(dados_novos)
        # ----------------------------------------------------
        
        # Simulação matemática fictícia enquanto você não pluga o seu modelo
        preco_simulado = (renda * 45000) + (idade * 1200) + (comodos * 8000) - (ocupacao * 5000) + 100000
        
        # Exibição do resultado estilizado com um box de sucesso
        st.markdown("---")
        st.success("🎉 Previsão realizada com sucesso!")
        
        r_col1, r_col2 = st.columns([1, 2])
        with r_col1:
            st.metric(label="Valor Estimado do Imóvel", value=f"${preco_simulado:,.2f}")
        with r_col2:
            st.info("💡 **Dica de Negócio:** Esta estimativa foi gerada considerando a localização geográfica exata informada através das coordenadas de Latitude e Longitude.")
