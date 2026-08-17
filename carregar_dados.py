import pandas as pd

from tools import (
    criar_tool_reposicao,
    criar_tool_encalhados,
    criar_tool_promocoes,
    criar_tool_orcamento,
    criar_tool_risco_ruptura
)


df = pd.read_csv("dados/estoque_produtos_limpeza_challenge.csv")

tool_reposicao = criar_tool_reposicao(df)
tool_encalhados = criar_tool_encalhados(df)
tool_promocoes = criar_tool_promocoes(df)
tool_orcamento = criar_tool_orcamento(df)
tool_risco_ruptura = criar_tool_risco_ruptura(df)


resultado_reposicao = tool_reposicao.invoke("")

print("=== PRODUTOS PARA REPOSIÇÃO ===")
print(resultado_reposicao)


resultado_encalhados = tool_encalhados.invoke("")

print("\n=== PRODUTOS ENCALHADOS ===")
print(resultado_encalhados)


resultado_promocoes = tool_promocoes.invoke("")

print("\n=== OPORTUNIDADES DE PROMOÇÃO ===")
print(resultado_promocoes)


print("\n=== ORÇAMENTO DE COMPRA ===")

orcamento = 5000

resultado_orcamento = tool_orcamento.invoke(str(orcamento))

print(resultado_orcamento)


resultado_risco = tool_risco_ruptura.invoke("")

print("\n=== RISCO DE RUPTURA ===")
print(resultado_risco)