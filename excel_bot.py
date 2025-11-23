import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

# Configuração da página Streamlit
st.set_page_config(page_title="bot exel", page_icon="🤖")
st.title("🤖 converse com seu agente para mais informações da sua tabela")

# Carregar arquivo Excel e chave API
uploaded_file = st.file_uploader("Escolha um arquivo Excel (xlsx) ou Csv (csv)", type=["xlsx", "csv"])
api_key = st.text_input("Insira sua chave API da OpenAI", type="password")

# Processar o arquivo carregado
if uploaded_file is not None and api_key:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Mostra uma prévia da tabela para o usuário
        st.write("### Visualização dos dados")
        st.dataframe(df.head())

        # Cria o agente LangChain com o modelo GPT-4o
        llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=api_key)
        agent = create_pandas_dataframe_agent(llm, df, verbose=True, agent_type="openai-tools", allow_dangerous_code=True)

        # Interface de conversa
        st.divider()
        pergunta = st.text_input("O que você quer saber ou fazer com a tabela?:")

        if st.button("Consultar / Organizar"):
            if pergunta:
                with st.spinner("Analisando a tabela..."):
                    try:
                        resposta = agent.invoke(pergunta)
                        st.success("Consulta concluída!")
                        st.write("### Resposta do agente:")
                        st.write(resposta['output'])
                    except Exception as e:
                        st.error(f"Ocorreu um erro: {e}")
            else:
                st.warning("Por favor, insira uma pergunta.")
    except Exception as e:
        st.error(f"Ocorreu um erro ao ler o arquivo: {e}")
else:
    if not api_key:
        st.warning("Por favor, insira sua chave API da OpenAI.")



