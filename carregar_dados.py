import pandas as pd

from analises import criar_tool_reposicao


df = pd.read_csv("dados/estoque_produtos_limpeza_challenge.csv")

tool_reposicao = criar_tool_reposicao(df)

resultado = tool_reposicao.invoke("")

print(resultado)