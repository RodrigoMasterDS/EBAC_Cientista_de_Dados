#import timeit
import pandas            as pd
import streamlit         as st
from matplotlib.colors import ListedColormap
from PIL                 import Image
from io                  import BytesIO

# Set no tema do seaborn para melhorar o visual dos plots
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
#sns.set_theme(style="ticks", rc=custom_params)

# Função para converter o df para excel 
@st.cache_data
def to_excel(df, file_name):
    file_path = file_name + '.xlsx'
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()  # Close the ExcelWriter to save the file
    return file_path

# Criando os segmentos
def recencia_class(x, r, q_dict):
    """Classifica como melhor o menor quartil 
    x = valor da linha,
    r = recencia,
    q_dict = quartil dicionario   
    """
    if x <= q_dict[r][0.25]:
        return 'A'
    elif x <= q_dict[r][0.50]:
        return 'B'
    elif x <= q_dict[r][0.75]:
        return 'C'
    else:
        return 'D'


def freq_val_class(x, fv, q_dict):
    """Classifica como melhor o maior quartil 
       x = valor da linha,
       fv = frequencia ou valor,
       q_dict = quartil dicionario   
    """
    if x <= q_dict[fv][0.25]:
        return 'D'
    elif x <= q_dict[fv][0.50]:
        return 'C'
    elif x <= q_dict[fv][0.75]:
        return 'B'
    else:
        return 'A'

    
# Configuração para evitar que o Streamlit ajuste automaticamente o tamanho dos gráficos
st.set_option('deprecation.showPyplotGlobalUse', False)


# Função principal da aplicação
def main():
    st.set_page_config(page_title = 'RFV Analysis', \
        page_icon = 'img/page_icon.png',
        #layout="wide",
        initial_sidebar_state='expanded'
    )

    # Estilo da página
    st.markdown("""
<style>
    h1 {
        color: #26547C;
        text-align: left;
    }
    h2 {
        color: #407FB7;
        border-bottom: 1px solid #407FB7;
    }
    h3 {
        color: #4A90E2;
        text-align: center;    
    }
    p {
        color: #333333;
    }
</style>
""", unsafe_allow_html=True)

    # Título principal da aplicação
    st.write('# RFV - Análise de Recência, Frequência e Valor de Clientes')
    st.markdown("---")

    # Apresenta a imagem na barra lateral da aplicação
    image = Image.open("img/side-image.jpg")
    st.sidebar.image(image)

    # Botão para carregar arquivo na aplicação 
    st.sidebar.write("## Upload File")
    data_file_1 = st.sidebar.file_uploader("RFV data", type = ['csv','xlsx'])

    # Verifica se há conteúdo carregado na aplicação
    if data_file_1 is not None:
    # Verifica o tipo do arquivo e carrega os dados adequadamente
        if data_file_1.type == 'text/csv':
            df_compras = pd.read_csv(data_file_1, infer_datetime_format=True, parse_dates=['DiaCompra'])
        elif data_file_1.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            df_compras = pd.read_excel(data_file_1, infer_datetime_format=True, parse_dates=['DiaCompra'])

        #------RECÊNCIA-----
        st.write('## Recência (R)')

        dia_atual = df_compras['DiaCompra'].max()
        st.write('Dia máximo na base de dados: ', dia_atual)

        st.write('Há quantos dias o cliente realizou a sua última compra?')

        df_recencia = df_compras.groupby(by='ID_cliente',
                                as_index=False)['DiaCompra'].max()
        df_recencia.columns = ['ID_cliente', 'DiaUltimaCompra']
        df_recencia['Recencia'] = df_recencia['DiaUltimaCompra'].apply(lambda x: (dia_atual-x).days)
        st.write(df_recencia.head())

        df_recencia.drop('DiaUltimaCompra', axis=1, inplace=True)
        #-------------------

        #------FREQUÊNCIA------
        st.write('## Frequência (F)')
        st.write('Quantas vezes cada cliente realizou uma compra?')
        df_frequencia = df_compras[['ID_cliente', 'CodigoCompra'
                            ]].groupby('ID_cliente').count().reset_index()
        df_frequencia.columns = ['ID_cliente', 'Frequencia']
        st.write(df_frequencia.head())
        #-----------------------

        #---------VALOR---------
        st.write('## Valor(V)')
        st.write('Qual o valor total gasto por cada cliente no período?')
        df_valor = df_compras[['ID_cliente', 'ValorTotal'
                    ]].groupby('ID_cliente').sum().reset_index()
        df_valor.columns = ['ID_cliente', 'Valor']
        st.write(df_valor.head())
        #------------------------


        st.write('## Tabela RFV final')
        df_RF = df_recencia.merge(df_frequencia, on='ID_cliente')
        df_RFV = df_RF.merge(df_valor, on='ID_cliente')
        df_RFV.set_index('ID_cliente', inplace=True)
        st.write(df_RFV.head())

        st.write('## Segmentação utilizando o RFV')
        st.write("A segmentação dos clientes é feita criando quartis para cada componente do RFV, sendo que o melhor quartil é chamado de 'A', o segundo melhor quartil é chamado de 'B', o terceiro melhor 'C', e o pior 'D'. O melhor e o pior possuem diferentes interpretações de acordo com a componente.") 
        st.write("No caso da recência, quanto menor o valor, melhor é o cliente (pois ele comprou há pouco tempo). Logo o menor quartil seria classificado como 'A'.")
        st.write("No caso da frêquencia, a lógica se inverte, ou seja, quanto maior a frêquencia de compras do cliente, melhor é. Logo, o maior quartil recebe a letra 'A'.")
        st.write('Se há interesse em mais ou menos classes, basta segmentar cada componente em um diferente número de partes.')

        st.write('### Quartis para o RFV')
        quartis = df_RFV.quantile(q=[0.25, 0.5, 0.75])
        st.write(quartis)

        st.write('Tabela com a classificação dos clientes após a segmentação')
        df_RFV['R_quartil'] = df_RFV['Recencia'].apply(recencia_class,
                                                args=('Recencia', quartis))
        df_RFV['F_quartil'] = df_RFV['Frequencia'].apply(freq_val_class,
                                                args=('Frequencia', quartis))
        df_RFV['V_quartil'] = df_RFV['Valor'].apply(freq_val_class,
                                            args=('Valor', quartis))
        df_RFV['RFV_Score'] = (df_RFV.R_quartil + df_RFV.F_quartil +
                    df_RFV.V_quartil)
        st.write(df_RFV.head())


        st.write('Quantidade de clientes por grupos')
        st.write(df_RFV['RFV_Score'].value_counts())

        st.write('#### Clientes com menor recência, maior frequência e maior valor gasto')
        st.write(df_RFV[df_RFV['RFV_Score'] == 'AAA'].sort_values('Valor',
                                                ascending=False).head(10))

        st.write('### Ações de marketing/CRM')
        dict_acoes = {
        'AAA':
        'Enviar cupons de desconto, Pedir para indicar nosso produto pra algum amigo, Ao lançar um novo produto enviar amostras grátis pra esses.',
        'DDD':
        'Churn! clientes que gastaram bem pouco e fizeram poucas compras, fazer nada',
        'DAA':
        'Churn! clientes que gastaram bastante e fizeram muitas compras, enviar cupons de desconto para tentar recuperar',
        'CAA':
        'Churn! clientes que gastaram bastante e fizeram muitas compras, enviar cupons de desconto para tentar recuperar'
        }

        df_RFV['acoes de marketing/crm'] = df_RFV['RFV_Score'].map(dict_acoes)
        st.write(df_RFV.head())
        
        #df_RFV.to_excel('./output/RFV.xlsx')   

        #df_xlsx = to_excel(df_RFV)
        #st.download_button(label='Download', data=df_xlsx, file_name='RFV_.xlsx')

        file_name = 'RFV_'
        excel_file_path = to_excel(df_RFV, file_name)
        st.download_button(label='📥 Download data in EXCEL', 
                    data=open(excel_file_path, 'rb'), 
                    file_name=file_name + '.xlsx')


        st.write('Quantidade de clientes por tipo de ação')
        st.write(df_RFV['acoes de marketing/crm'].value_counts(dropna=False))



if __name__ == '__main__':
	main()