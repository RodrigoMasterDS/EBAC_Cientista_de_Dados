# Imports
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

# Configuração inicial do Matplotlib
plt.rcParams.update({'figure.autolayout': True})

# Título da aplicação
st.title("Análise de Marketing")

############## CARREGANDO A BASE DE DADOS ########################################################
# Sidebar para upload do arquivo CSV
uploaded_file = st.sidebar.file_uploader("Faça o upload do arquivo CSV", type=["csv"])

@st.cache_data
def carregar_dados(uploaded_file):
    if uploaded_file is not None:
        try:
            return pd.read_csv(uploaded_file, delimiter=';')
        except Exception as e:
            st.error(f"Erro ao carregar o arquivo: {e}")
            return None
    return None

df = carregar_dados(uploaded_file)

# Verificar se o arquivo foi carregado
if df is None:
    st.info("Por favor, faça o upload de um arquivo CSV.")
    st.stop()

###################################################################################################

##################### FILTRANDO OS DADOS ##########################################################
st.sidebar.header("Filtros")
valores_filtros = {}
for coluna in ['job', 'marital', 'education', 'housing', 'loan', 'contact', 'month']:
    if coluna in df.columns:
        valores_filtros[coluna] = st.sidebar.multiselect(f"Selecione valores para {coluna}", df[coluna].unique())

if 'age' in df.columns:
    min_age = int(df['age'].min())
    max_age = int(df['age'].max())
    idades = st.sidebar.slider("Idade", min_value=min_age, max_value=max_age, value=(min_age, max_age))
else:
    idades = None

@st.cache_data
def filtrar_dados(df, valores_filtros, idades):
    df_filtrado = df.copy()
    for coluna, valores in valores_filtros.items():
        if valores:
            df_filtrado = df_filtrado[df_filtrado[coluna].isin(valores)]
    if idades:
        df_filtrado = df_filtrado[(df_filtrado['age'] >= idades[0]) & (df_filtrado['age'] <= idades[1])]
    return df_filtrado

df_filtrado = filtrar_dados(df, valores_filtros, idades)

st.subheader("Dados Filtrados")
st.write(df_filtrado)
st.write(f"Total de {df_filtrado.shape[0]} pessoas selecionadas.")

###################################################################################################

##################### GRÁFICOS ####################################################################

st.header("Gráficos")
if 'y' in df_filtrado.columns:
    tipo_grafico = st.selectbox("Escolha o tipo de gráfico", ["Gráfico de Barras", "Gráfico de Pizza"])
    if tipo_grafico == "Gráfico de Barras":
        # Gráfico de barras
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(data=df_filtrado, x='y', ax=ax)
        ax.set_title("Distribuição de 'y'")
        st.pyplot(fig)
    else:
        # Gráfico de pizza
        fig, ax = plt.subplots(figsize=(6, 6))
        df_filtrado['y'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
        ax.set_ylabel('')
        st.pyplot(fig)
else:
    st.warning("A coluna 'y' não foi encontrada no DataFrame.")

###################################################################################################

##################### SALVANDO OS DADOS ###########################################################
def salvar_arquivo(dataframe, formato):
    buffer = BytesIO()
    if formato == 'csv':
        dataframe.to_csv(buffer, index=False)
    elif formato == 'xlsx':
        dataframe.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)
    return buffer

col1, col2 = st.columns(2)
with col1:
    if st.button('Salvar como CSV'):
        arquivo_csv = salvar_arquivo(df_filtrado, 'csv')
        st.download_button("Download CSV", arquivo_csv, "dados_filtrados.csv", "text/csv")
with col2:
    if st.button('Salvar como XLSX'):
        arquivo_xlsx = salvar_arquivo(df_filtrado, 'xlsx')
        st.download_button("Download XLSX", arquivo_xlsx, "dados_filtrados.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
