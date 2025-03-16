import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração inicial do Streamlit
st.set_page_config(page_title="Gerenciador de Estoque Automático", layout="wide")

# Função para calcular previsão de estoque
def prever_estoque(df):
    alertas = []
    for index, row in df.iterrows():
        dias_restantes = row['quantidade_atual'] / row['consumo_medio_diario']
        if dias_restantes <= 2:
            alertas.append(f"ALERTA: {row['ingrediente']} precisa ser reabastecido em {dias_restantes:.1f} dias.")
        elif row['quantidade_atual'] > row['limite_minimo'] * 3:
            alertas.append(f"EXCESSO: {row['ingrediente']} está em excesso.")
    return alertas

# Tela Principal (Dashboard)
st.title("Gerenciador de Estoque Automático")

# Upload do Arquivo (Aceita Excel e CSV)
st.header("Carregar Planilha de Estoque")
uploaded_file = st.file_uploader(
    "Faça upload de um arquivo Excel (.xlsx) ou CSV (.csv)", 
    type=["xlsx", "csv"]
)

df_estoque = None  # Inicializa o DataFrame

if uploaded_file is not None:
    try:
        # Verifica o tipo de arquivo e carrega os dados
        if uploaded_file.name.endswith(".csv"):
            df_estoque = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df_estoque = pd.read_excel(uploaded_file)
        
        # Verifica se as colunas esperadas estão presentes
        expected_columns = {"ingrediente", "quantidade_atual", "consumo_medio_diario", "limite_minimo"}
        if not expected_columns.issubset(df_estoque.columns):
            st.error("O arquivo não contém as colunas esperadas: 'ingrediente', 'quantidade_atual', 'consumo_medio_diario', 'limite_minimo'.")
            st.stop()
        
        st.success("Planilha carregada com sucesso!")
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        st.stop()
else:
    st.warning("Por favor, faça o upload de um arquivo Excel (.xlsx) ou CSV (.csv) para continuar.")
    st.stop()

# Seção de Alertas
if df_estoque is not None:
    st.header("Alertas de Estoque")
    alertas = prever_estoque(df_estoque)
    if alertas:
        for alerta in alertas:
            st.warning(alerta)
    else:
        st.success("Nenhum alerta no momento.")

    # Seção de Status do Estoque
    st.header("Status do Estoque")
    st.dataframe(df_estoque)

    # Gráfico de Barras para Visualização do Estoque
    st.header("Visualização do Estoque")
    fig, ax = plt.subplots()
    ax.bar(df_estoque["ingrediente"], df_estoque["quantidade_atual"], color='skyblue')
    ax.set_ylabel("Quantidade Atual")
    ax.set_title("Estoque Atual por Ingrediente")
    st.pyplot(fig)

    # Tela de Cadastro de Ingredientes
    with st.expander("Adicionar/Editar Ingredientes"):
        ingrediente = st.text_input("Nome do Ingrediente")
        quantidade = st.number_input("Quantidade Atual", min_value=0)
        consumo_medio = st.number_input("Consumo Médio Diário", min_value=0.0, step=0.1)
        limite_minimo = st.number_input("Limite Mínimo", min_value=0)
        
        if st.button("Salvar"):
            novo_ingrediente = {
                "ingrediente": ingrediente,
                "quantidade_atual": quantidade,
                "consumo_medio_diario": consumo_medio,
                "limite_minimo": limite_minimo
            }
            df_estoque = df_estoque.append(novo_ingrediente, ignore_index=True)
            st.success(f"{ingrediente} adicionado/editado com sucesso!")

    # Tela de Relatórios
    st.header("Relatórios")
    if st.button("Gerar Relatório"):
        st.write("Relatório gerado com sucesso!")
        # Exportação para CSV (padrão)
        df_estoque.to_csv("relatorio_estoque.csv", index=False)
        st.markdown("Relatório salvo como `relatorio_estoque.csv`.")
