import pandas as pd

from tools import (
    criar_tool_reposicao,
    criar_tool_encalhados,
    criar_tool_promocoes
)


df = pd.read_csv("dados/estoque_produtos_limpeza_challenge.csv")

tool_reposicao = criar_tool_reposicao(df)
tool_encalhados = criar_tool_encalhados(df)
tool_promocoes = criar_tool_promocoes(df)


resultado_reposicao = tool_reposicao.invoke("")

print("=== PRODUTOS PARA REPOSIÇÃO ===")
print(resultado_reposicao)


resultado_encalhados = tool_encalhados.invoke("")

print("\n=== PRODUTOS ENCALHADOS ===")
print(resultado_encalhados)


resultado_promocoes = tool_promocoes.invoke("")

print("\n=== OPORTUNIDADES DE PROMOÇÃO ===")
print(resultado_promocoes)