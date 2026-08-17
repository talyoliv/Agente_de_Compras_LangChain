import streamlit as st

from agente import agent_executor


st.set_page_config(
    page_title="Agente de Compras",
    page_icon="📦",
    layout="wide"
)


st.title("📦 Agente de Compras")
st.write(
    "Assistente inteligente para análise de estoque "
    "e apoio à decisão de compras."
)


pergunta = st.text_input(
    "Digite sua pergunta sobre o estoque:"
)


if st.button("Analisar"):
    if pergunta:
        with st.spinner("Analisando o estoque..."):

            resposta = agent_executor.invoke({
                "input": pergunta
            })

        st.subheader("💡 Resposta do agente")
        st.markdown(resposta["output"])

    else:
        st.warning("Digite uma pergunta para realizar a análise.")