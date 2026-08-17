import streamlit as st
import pandas as pd

from agente import agent_executor


st.set_page_config(
    page_title="Agente de Compras",
    page_icon="📦",
    layout="wide"
)


# =========================
# CARREGAMENTO DOS DADOS
# =========================

df = pd.read_csv(
    "dados/estoque_produtos_limpeza_challenge.csv"
)


# =========================
# TÍTULO
# =========================

st.title("📦 Agente de Compras")

st.write(
    "Assistente inteligente para análise de estoque "
    "e apoio à decisão de compras."
)


# =========================
# INDICADORES
# =========================

produtos = len(df)

produtos_abaixo_minimo = (
    df["estoque_atual"] < df["estoque_minimo"]
).sum()

produtos_encalhados = (
    df["dias_sem_venda"] >= 30
).sum()

produtos_risco_alto = (
    df["estoque_atual"] / df["estoque_minimo"] < 0.5
).sum()


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "📦 Produtos",
        produtos
    )


with col2:
    st.metric(
        "🔴 Abaixo do mínimo",
        produtos_abaixo_minimo
    )


with col3:
    st.metric(
        "🐌 Encalhados",
        produtos_encalhados
    )


with col4:
    st.metric(
        "⚠️ Risco alto",
        produtos_risco_alto
    )


st.divider()


# =========================
# PERGUNTA AO AGENTE
# =========================

st.subheader("💬 Pergunte ao agente")


pergunta = st.text_input(
    "Digite sua pergunta sobre o estoque:",
    placeholder="Ex.: Tenho R$ 5.000 para comprar. O que devo priorizar?"
)


if st.button("🔎 Analisar"):

    if pergunta:

        with st.spinner("Analisando o estoque..."):

            resposta = agent_executor.invoke({
                "input": pergunta
            })

        st.subheader("🤖 Resposta do agente")

        st.markdown(
            resposta["output"]
        )

    else:

        st.warning(
            "Digite uma pergunta para realizar a análise."
        )