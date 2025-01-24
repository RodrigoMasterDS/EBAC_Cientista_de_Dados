import streamlit as st
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve, confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression

# Adicionar estilo CSS para cabeçalhos
st.markdown("""
    <style>
        h1 {
            color: #ff4b4b;
        }
        h2 {
            color: #97ffff;
        }
        h3 {
            color: #00ffff;
        }
    </style>
    """, unsafe_allow_html=True)

# Carregar os dados e exibir as primeiras linhas
st.title("Análise de Credit Scoring")
st.write("Neste projeto, estamos construindo um credit scoring para cartão de crédito, em um desenho amostral com 15 safras, e utilizando 12 meses de performance.")

df = pd.read_feather('/users/rodri/documents/Github/EBAC_Cientista_de_Dados/Modulo_37_Regressao_Logistica_II/credit_scoring.ftr')

caminho = '/users/rodri/documents/Github/EBAC_Cientista_de_Dados/Modulo_37_Regressao_Logistica_II/credit_scoring.ftr'

if os.path.exists(caminho):
    print("Arquivo encontrado!")
else:
    print(f"O arquivo não foi encontrado no caminho: {caminho}")
st.write("Primeiras linhas do dataset:")
st.write(df.head())

def carregar_dados():
    df = pd.read_feather('./credit_scoring.ftr')
    return df

# Carregar os dados
df = carregar_dados()


st.markdown("## Parte I - Exploratória dos Dados")

# Identificar os três últimos meses de data_ref
ultimos_meses = df['data_ref'].sort_values().unique()[-3:]

# Separar os dados em treino e validação OOT
df_treino = df[~df['data_ref'].isin(ultimos_meses)].copy()
df_oot = df[df['data_ref'].isin(ultimos_meses)].copy()

# Remover as colunas data_ref e index
df_treino = df_treino.drop(columns=['data_ref', 'index'])
df_oot = df_oot.drop(columns=['data_ref', 'index'])

# Exibir as dimensões dos DataFrames
st.write(f"Tamanho do conjunto de treino: {df_treino.shape}")
st.write(f"Tamanho do conjunto de validação OOT: {df_oot.shape}")

# Número total de linhas e linhas por mês em data_ref
total_linhas = df.shape[0]
linhas_por_mes = df['data_ref'].value_counts().sort_index()
st.write(f"Número total de linhas: {total_linhas}")
st.write("Número de linhas por mês em data_ref:")
st.write(linhas_por_mes.head())

# ------------------VARIAVEIS QUALITATIVAS E QUANTITATIVAS--------------------------

# Separando as variáveis qualitativas
qualitativas = ['sexo', 'posse_de_veiculo', 'posse_de_imovel', 'tipo_renda',
                'educacao', 'estado_civil', 'tipo_residencia']

# Separando as variáveis quantitativas
quantitativas = ['qtd_filhos', 'idade', 'tempo_emprego', 'qt_pessoas_residencia', 'renda']

# Descritiva para variáveis qualitativas
st.markdown("### Descritiva das variáveis qualitativas:")
selected_var = st.selectbox("Selecione uma variável:", qualitativas)
st.write(f"**{selected_var}:**")
st.write(df[selected_var].value_counts())

# Descritiva para variáveis quantitativas
st.markdown("### Descritiva das variáveis quantitativas:")
st.write(df[quantitativas].describe().T)

# Exibir distribuição da variável target 'mau'
st.write("Distribuição da variável 'mau':")
st.write(df['mau'].value_counts())

# --------------PLOTS UNIVARIADA LONGITUDINAL-------------------

st.markdown("### Distribuição das variáveis qualitativas ao longo do tempo:")
# Adicionar seletor de variável qualitativa
# Adicionar seletor de variável qualitativa
var_qualitativa_selecionada = st.selectbox(
    'Selecione a variável qualitativa para visualizar sua distribuição ao longo do tempo:',
    qualitativas
)
fig, ax = plt.subplots(figsize=(10, 6)) 
data = df.groupby(['data_ref', var_qualitativa_selecionada]).size().unstack()
data.plot(marker='o', linestyle='-', ax=ax)
ax.set_title(f'Distribuição de {var_qualitativa_selecionada} ao Longo do Tempo')
ax.set_xlabel('Mês de Referência (data_ref)')
ax.set_ylabel(f'Contagem de {var_qualitativa_selecionada}')
ax.legend(title=var_qualitativa_selecionada, bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True)
plt.tight_layout()
st.pyplot(fig)


st.markdown("### Evolução da Média das Variáveis Quantitativas ao longo do tempo:")
# Adicionar seletor de variável
var_quantitativa_selecionada = st.selectbox(
    'Selecione a variável quantitativa para visualizar a evolução da média ao longo do tempo:',
    quantitativas
)
fig, ax = plt.subplots(figsize=(10, 6))  
df.groupby('data_ref')[var_quantitativa_selecionada].mean().plot(marker='o', linestyle='-', ax=ax)
ax.set_title(f'Evolução da Média de {var_quantitativa_selecionada} ao Longo do Tempo')
ax.set_xlabel('Mês de Referência (data_ref)')
ax.set_ylabel(f'Média de {var_quantitativa_selecionada}')
ax.grid(True)
plt.tight_layout()
st.pyplot(fig)

# ----------------------------------------------------------------

# Evolução da Taxa de Inadimplência ao longo do tempo
st.markdown("### Evolução da Taxa de Inadimplência ao longo do tempo:")
inadimplencia_por_mes = df.groupby('data_ref')['mau'].mean()

plt.figure(figsize=(10, 6))
plt.plot(inadimplencia_por_mes.index, inadimplencia_por_mes.values, marker='o', color='red')
plt.title('Evolução da Taxa de Inadimplência ao Longo do Tempo')
plt.xlabel('Mês de Referência')
plt.ylabel('Taxa de Inadimplência')
plt.grid(True)
st.pyplot(plt)


# -----------------BIVARIADAS------------------------------
# Configuração do Streamlit
st.markdown("### Análise de Proporção de Inadimplência por Variável Qualitativa")

# Criar um seletor de variáveis qualitativas
variavel_selecionada1 = st.selectbox("Selecione uma variável qualitativa para análise:", qualitativas)

# Filtrar e plotar os dados para a variável selecionada
fig, ax = plt.subplots(figsize=(10, 6))

# Calcular a proporção de inadimplência por data_ref e variável qualitativa
data = df.groupby(['data_ref', variavel_selecionada1])['mau'].mean().unstack()

# Plotar o gráfico
data.plot(marker='o', linestyle='-', ax=ax)

# Configurações do gráfico
ax.set_title(f'Proporção de Inadimplência por {variavel_selecionada1} ao Longo do Tempo')
ax.set_xlabel('Mês de Referência (data_ref)')
ax.set_ylabel('Proporção de Inadimplência')
ax.legend(title=variavel_selecionada1, bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True)
plt.tight_layout()
st.pyplot(fig)

# Configuração do Streamlit
st.markdown("### Análise de Proporção de Inadimplência por Faixas de Variável Quantitativa")

# Criar um seletor de variáveis quantitativas
variavel_selecionada2 = st.selectbox("Selecione uma variável quantitativa para análise:", quantitativas)

# Configuração dos subplots: 2 linhas e 2 colunas
fig, axes = plt.subplots(figsize=(14, 10)) 

# Calcular a proporção de inadimplência por faixas da variável quantitativa ao longo do tempo
data = df.groupby(['data_ref', pd.cut(df[variavel_selecionada2], bins=5)], observed=False)['mau'].mean().unstack()

# Plotar o gráfico no primeiro subplot
data.plot(marker='o', linestyle='-', ax=axes)
axes.set_title(f'Proporção de Inadimplência por {variavel_selecionada2} ao Longo do Tempo')
axes.set_xlabel('Mês de Referência (data_ref)')
axes.set_ylabel('Proporção de Inadimplência')
axes.grid(True)
plt.tight_layout()
st.pyplot(fig)

#----------------------------TRATAMENTO DOS DADOS --------------------------------
st.markdown("## Parte II - Tratamento dos Dados e Modelagem")
st.write('Exibir os dados faltantes:')
st.write(df.isna().sum())

st.write("Uma breve discussão sobre as variáveis.")
st.markdown("""
- **Sexo:** A distribuição está ok, e parece ser uma boa variável para o modelo.
- **Posse de veículo:** Será removida, pois não há discriminação.
- **Posse de imóvel:** Está ok.
- **Qtd de Filhos:** Apresenta boa distribuição até 5, acima disso se apresenta muito irregular na bivariada. Os valores serão agrupados acima de 5.
- **Tipo de Renda:** Removeremos pensionistas, que correspondem aos dados faltantes, e também removeremos bolsista devido à grande irregularidade.
- **Educação:** Será agrupada acima de Superior, devido à irregularidade.
- **Estado Civil:** Está ok.
- **Idade:** Devido à tendência do gráfico da bivariada, será agrupada em menor e maior que 30.
- **Tempo de Emprego:** Agruparemos a partir de 25.
- **Qtd Pessoas na Residencia:** Será removida, pois existe alta correlação com a quantidade de filhos, sendo redundante.
- **Renda:** Removeremos os valores acima de 800.000, que são outliers.
""", unsafe_allow_html=True)


st.markdown('#### Dataset após tratamento das variaveis:')
# Excluir a variável 'posse_de_veiculo' (não discrimina)
df = df.drop(columns=['posse_de_veiculo'])
# Agrupar quantidade de filhos acima de 5 em uma única categoria "5+"
df['qtd_filhos'] = df['qtd_filhos'].apply(lambda x: '<6' if x <= 5 else '6+')
# Remover categorias 'Pensionista' e 'Bolsista' da variável 'tipo_renda'
df = df[~df['tipo_renda'].isin(['Pensionista', 'Bolsista'])]
# Agrupar "Pós-graduação" em "Superior ou mais" na variável 'educacao'
df['educacao'] = df['educacao'].replace({'Pós-graduação': 'Superior ou mais'})
# Criar nova variável 'faixa_idade', categorizando como "<30" e "30+"
df['faixa_idade'] = df['idade'].apply(lambda x: '<30' if x < 30 else '30+')
# Agrupar tempo de emprego acima de 25 anos em "25+ anos"
df['tempo_emprego'] = df['tempo_emprego'].apply(lambda x: "<25" if x < 25 else '25+ anos')
# Agrupar quantidade de pessoas na residência acima de 6 em "6+"
df = df.drop(columns=['qt_pessoas_residencia'])
# Limitar a renda a valores de até 800.000 para tratar outliers
df = df[df['renda'] <= 800000]
st.write(df.head())


# Dividindo os dados em treino e teste com base na data
df_sorted = df.sort_values(by='data_ref')
cutoff_date = df_sorted['data_ref'].max() - pd.DateOffset(months=3)
train_df = df_sorted[df_sorted['data_ref'] <= cutoff_date]
test_df = df_sorted[df_sorted['data_ref'] > cutoff_date]

# Criando variáveis dummy
X_train = pd.get_dummies(train_df.drop(columns=['mau', 'data_ref', 'index']))
X_test = pd.get_dummies(test_df.drop(columns=['mau', 'data_ref', 'index']))
X_train, X_test = X_train.align(X_test, join='left', axis=1, fill_value=0)
y_train = train_df['mau']
y_test = test_df['mau']

# Ajustando o modelo de Regressão Logística com class_weight='balanced'
@st.cache_resource
def train_model(X_train, y_train):
    model = LogisticRegression(max_iter=3000, class_weight='balanced', random_state=66)
    model.fit(X_train, y_train)
    return model

model = train_model(X_train, y_train)    

# Ajustando o limiar para a classificação
st.markdown('#### Limiar de Classificação:')
st.write("O limiar da classificação por padrão seria 0.5 - 50% - representando a distribuição binária. Porém, podemos alterar o limiar a fim de aumentar a precisão de classificação, diminuindo o número de falsos positivos e falsos negativos.")
st.write("Dependendo do caso, é mais importante ter uma proporção menor de falsos positivos, do que de negativos, ou vice-versa. No caso desses dados, falsos positivos prejudicam o cliente, enquanto falsos negativos podem prejudicar o banco.")
st.write("Então, é uma questão de avaliar o impacto das decisões do modelo no negócio.")
threshold = st.slider(
    "Escolha o limiar para a classificação:",
    min_value=0.5,
    max_value=0.75,
    value=0.69,
    step=0.01
)

# Avaliação na base de treino
y_prob_train = model.predict_proba(X_train)[:, 1]  # Probabilidades para a classe positiva na base de treino
y_pred_train_adjusted = (y_prob_train > threshold).astype(int)  # Aplicando o limiar ajustado

# Avaliação na base de teste
y_prob_test = model.predict_proba(X_test)[:, 1]  # Probabilidades para a classe positiva na base de teste
y_pred_test_adjusted = (y_prob_test > threshold).astype(int)  # Aplicando o limiar ajustado

# Matriz de Confusão e Relatório de Classificação para a base de treino
st.markdown("### Matriz de Confusão e Relatório de Classificação na Base de Treino:")
conf_matrix_train = confusion_matrix(y_train, y_pred_train_adjusted)
class_report_train = classification_report(y_train, y_pred_train_adjusted)

# Criar duas colunas
col1, col2 = st.columns([1,2])

# Exibir a matriz de confusão na coluna da esquerda
with col1:
    st.write("Matriz de Confusão:")
    st.table(conf_matrix_train)  # Use st.table para exibir a matriz de confusão

# Exibir o relatório de classificação na coluna da direita
with col2:
    st.write("Relatório de Classificação:")
    st.text(class_report_train)  # Use st.text para exibir o relatório de classificação

# Matriz de Confusão e Relatório de Classificação para a base de teste
st.markdown("### Matriz de Confusão e Relatório de Classificação na Base de Teste:")
conf_matrix_test = confusion_matrix(y_test, y_pred_test_adjusted)
class_report_test = classification_report(y_test, y_pred_test_adjusted)

# Criar duas colunas
col3, col4 = st.columns([1,2])

# Exibir a matriz de confusão na coluna da esquerda
with col3:
    st.write("Matriz de Confusão:")
    st.table(conf_matrix_test)  # Use st.table para exibir a matriz de confusão

# Exibir o relatório de classificação na coluna da direita
with col4:
    st.write("Relatório de Classificação:")
    st.text(class_report_test)  # Use st.text para exibir o relatório de classificação


def ks_statistic(y_true, y_prob):
    """Calcula a estatística KS"""
    fpr, tpr, thresholds = roc_curve(y_true, y_prob)
    return max(tpr - fpr)

def gini_coefficient(y_true, y_prob):
    """Calcula o coeficiente Gini"""
    return 2 * roc_auc_score(y_true, y_prob) - 1


# Métricas na base de treino
accuracy_train = accuracy_score(y_train, y_pred_train_adjusted)
ks_train = ks_statistic(y_train, y_prob_train)
gini_train = gini_coefficient(y_train, y_prob_train)

# Métricas na base de teste (OOT)
accuracy_test = accuracy_score(y_test, y_pred_test_adjusted)
ks_test = ks_statistic(y_test, y_prob_test)
gini_test = gini_coefficient(y_test, y_prob_test)

# Exibindo os resultados
# Criar um DataFrame com os resultados
data = {
    "Métrica": ["Acurácia", "KS", "Gini"],
    "Base de Treino": [f"{accuracy_train:.4f}", f"{ks_train:.4f}", f"{gini_train:.4f}"],
    "Base Out-of-Time (Teste)": [f"{accuracy_test:.4f}", f"{ks_test:.4f}", f"{gini_test:.4f}"]
}

df_results = pd.DataFrame(data)

# Exibir a tabela no Streamlit
st.markdown("### Avaliação do Modelo:")
st.table(df_results)

st.write("Para o limiar de classificação em 0.69, obtemos esses valores de acurácia, sendo mais altos para a base de treino, mas ainda bons para a base de teste. Esses valores indicam que o modelo está bem ajustado - apesar de ainda haver uma grande quantidade de falsos negativos - o modelo está prevendo bem os resultados.")
st.write("O gráfico abaixo mostra como o modelo está classificando de acordo com a probabilidade. O limiar pode ser ajustado acima para verificar diferentes configurações do modelo.")

# Gráfico de Dispersão para Probabilidades Preditas e Decisões Binárias
fig, ax = plt.subplots(figsize=(10, 6))

# Plotar as probabilidades versus as previsões
ax.scatter(y_prob_test, y_pred_test_adjusted, alpha=0.5, label='Predição Binária')
ax.axvline(x=threshold, color='red', linestyle='--', label='Limiar Atual')

# Adicionar títulos e rótulos
ax.set_title('Distribuição das Probabilidades Preditas e Decisões Binárias')
ax.set_xlabel('Probabilidade Predita')
ax.set_ylabel('Decisão Binária')
ax.legend()
ax.grid(True)

st.pyplot(fig)