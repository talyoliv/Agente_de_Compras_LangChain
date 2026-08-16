import os
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

from tools import (
    criar_tool_reposicao,
    criar_tool_encalhados,
    criar_tool_promocoes
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

tools = [
    tool_reposicao,
    tool_encalhados,
    tool_promocoes
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