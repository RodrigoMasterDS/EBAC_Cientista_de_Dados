import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="EBAC | Módulo 15 | Streamlit I | Exercício",
    # page_icon="https://ebaconline.com.br/favicon.ico",
    page_icon="https://github.com/RodrigoMasterDS/Rodrigo-EBAC-DS/blob/main/newebac_logo_black_half.png?raw=true",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown('''
<img src="https://github.com/RodrigoMasterDS/Rodrigo-EBAC-DS/blob/main/newebac_logo_black_half.png?raw=true" alt="ebac-logo">

---

# **Profissão: Cientista de Dados**
### **Módulo 15** | Streamlit I | Exercício

Aluno [Rodrigo Pacheco](https://www.linkedin.com/in/rodrigodatascience/)<br>
Data: 17 de outubro de 2023.

---
            ''', unsafe_allow_html=True)

st.markdown("# Caching ❄️")
st.sidebar.markdown("# Caching ❄️")

'---'


@st.cache_data  # 👈 Add the caching decorator
def load_data(url):
    df = pd.read_csv(url)  # 👈 Download the data
    return df


df = load_data(
    "https://github.com/plotly/datasets/raw/master/uber-rides-data1.csv")
st.dataframe(df)

st.button("Rerun")

'---'