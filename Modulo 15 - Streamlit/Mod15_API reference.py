import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import pydeck as pdk


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

st.markdown("# API reference")
st.sidebar.markdown("# API reference")


# 01 Display almost anything

# st.write('Hello **world**!')
# 'Hello **world**!'


# 02 Text elements

'## -Markdown:'
st.markdown('Olá **mundo**!')
st.markdown(
    'This text is :red[colored red], and this is **:blue[colored]** and bold.')
st.markdown(':green[$\sqrt{x^2+y^2}=1$] is a Pythagorean identity. :pencil:')


'## -Title:'
st.title('Título do app')

'## -Header:'
st.header('Este é um cabeçalho')

'## -Subheader:'
st.header('Este é um subtítulo')

'## -Caption:'
st.caption('Este é um pequeno texto de legenda escrito')

'## -Code block:'
code = '''def hello():
    print("Hello, Streamlit!")'''
st.code(code, language='python')

'## -Preformatted text:'
st.text('Olá mundo')

'## -LaTeX:'
st.latex('\int a x^2 \,dx')


# 03 Data display elements

'## -Dataframes:'
df = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
st.dataframe(df.style.highlight_max(axis=0))

'## -Static tables:'
df = pd.DataFrame(
    np.random.randn(10, 5),
    columns=('col %d' % i for i in range(5)))
st.table(df)

'## -Metrics:'
st.metric(label="Temperatura", value="32 °C", delta="1.2 °C")

'## -Dicts and JSON:'
st.json({
    'foo': 'bar',
    'baz': 'boz',
    'stuff': [
        'stuff 1',
        'stuff 2',
        'stuff 3',
        'stuff 5',
    ],
})


# 04 Chart elements

'## -Simple line charts:'
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])
st.line_chart(chart_data)

'## -Simple area charts:'
st.area_chart(chart_data)

'## -Simple bar charts:'
st.bar_chart(chart_data)

'## -Scatterplots on maps:'
df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [-20.3222, -40.3381],
    columns=['lat', 'lon'])
st.map(df)

'## -Matplotlib:'
arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)
st.pyplot(fig)

'## -Altair:'
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])
c = alt.Chart(chart_data).mark_circle().encode(
    x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
st.altair_chart(c, use_container_width=True)

'## -Vega-Lite:'
chart_data = pd.DataFrame(
    np.random.randn(200, 3),
    columns=['a', 'b', 'c'])
st.vega_lite_chart(chart_data, {
    'mark': {'type': 'circle', 'tooltip': True},
    'encoding': {
        'x': {'field': 'a', 'type': 'quantitative'},
        'y': {'field': 'b', 'type': 'quantitative'},
        'size': {'field': 'c', 'type': 'quantitative'},
        'color': {'field': 'c', 'type': 'quantitative'},
    },
})



'## -GraphViz:'
st.graphviz_chart('''
    digraph {
        run -> intr
        intr -> runbl
        runbl -> run
        run -> kernel
        kernel -> zombie
        kernel -> sleep
        kernel -> runmem
        sleep -> swap
        swap -> runswap
        runswap -> new
        runswap -> runmem
        new -> runmem
        sleep -> runmem
    }
''')


# 05 Input widgets

'## -Button:'
clicked = st.button('Click me')

'## -Data editor:'
df = pd.DataFrame(
    [
        {"command": "st.selectbox", "rating": 4, "is_widget": True},
        {"command": "st.balloons", "rating": 5, "is_widget": False},
        {"command": "st.time_input", "rating": 3, "is_widget": True},
    ]
)
# Replace st.experimental_data_editor with st.data_editor
edited_df = st.data_editor(df, key="my_data", num_rows="dynamic")

# Use edited_rows to access the edited data
if "edited_rows" in st.session_state:
    edited_rows = st.session_state.edited_rows
else:
    edited_rows = {}

# Find the row with the highest rating
if not edited_df.empty:
    favorite_command = df.loc[df["rating"].idxmax()]["command"]
    st.markdown(f"Your favorite command is **{favorite_command}**")

'## -Download button:'
text_contents = '''This is some text'''
st.download_button('Download some text', text_contents)

'## -Checkbox:'
selected = st.checkbox('Concordo')

'## -Animal:'
choice = st.radio('Escolha um', ['gatos', 'cachorros'])

'## -Selectbox:'
choice = st.selectbox('Escolha um', ['gatos', 'cachorros'])

'## -Multiselect'
choices = st.multiselect('Comprar', ['leite', 'maçãs', 'batatas'])

'## -Slider:'
number = st.slider('Escolha um número', 0, 100)

'## -Select-slider:'
st.select_slider('Escolha um tamanho', ['S', 'M', 'L'])

'## -Text input:'
name = st.text_input('Primeiro nome')

'## -Number input:'
choice = st.number_input('Escolha um número', 0, 10)

'## -Text-area:'
text = st.text_area('Texto para traduzir')

'## -Date input:'
date = st.date_input('Seu aniversário')

'## -Time input:'
time = st.time_input('Hora do encontro')

'## -File uploader:'
data = st.file_uploader('Upload um arquivo')

'## -Camera input:'
image = st.camera_input('Tire uma foto', disabled=True)

'## -Color picker:'
color = st.color_picker('Escolha uma cor')

'---'