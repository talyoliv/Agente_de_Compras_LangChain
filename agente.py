import os
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

from tools import (
    criar_tool_reposicao,
    criar_tool_encalhados,
    criar_tool_promocoes,
    criar_tool_orcamento,
    criar_tool_risco_ruptura,
    criar_tool_categoria
)

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=api_key
)

df = pd.read_csv("dados/estoque_produtos_limpeza_challenge.csv")

tool_reposicao = criar_tool_reposicao(df)
tool_encalhados = criar_tool_encalhados(df)
tool_promocoes = criar_tool_promocoes(df)
tool_orcamento = criar_tool_orcamento(df)
tool_risco_ruptura = criar_tool_risco_ruptura(df)
tool_categoria = criar_tool_categoria(df)

tools = [
    tool_reposicao,
    tool_encalhados,
    tool_promocoes,
    tool_orcamento,
    tool_risco_ruptura,
    tool_categoria
]

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        Você é um agente especialista em compras e gestão de estoque.

        Sua função é analisar os dados do estoque de produtos de limpeza
        e auxiliar o comprador na tomada de decisões.

        Utilize as ferramentas disponíveis sempre que a pergunta
        depender dos dados do estoque.

        Para perguntas que envolvam um orçamento disponível para compras,
        utilize a ferramenta analisar_orcamento.

        Quando o usuário informar um valor de orçamento, considere esse
        valor como limite máximo para a análise e priorize os produtos
        mais críticos de acordo com o nível de estoque.

        Para análises por categoria, compare os indicadores de estoque
        e destaque as categorias mais críticas, considerando conjuntamente
        ruptura, produtos abaixo do mínimo e estoque parado.

        Não recomende descarte de produtos apenas porque estão encalhados.
        Quando houver estoque parado, priorize sugestões como promoção,
        desconto, aumento de giro ou outras estratégias comerciais.

        Responda de forma clara, objetiva e em português.
        """
    ),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

pergunta = input("\nDigite sua pergunta sobre o estoque: ")

resposta = agent_executor.invoke({
    "input": pergunta
})

print("\n=== RESPOSTA DO AGENTE ===")
print(resposta["output"])