from langchain_core.tools import Tool


def analisar_reposicao(df):
    # Filtra produtos abaixo do mínimo
    produtos_criticos = df[
        df["estoque_atual"] < df["estoque_minimo"]
    ].copy()

    # Calcula quantidade sugerida
    produtos_criticos["quantidade_sugerida"] = (
        produtos_criticos["estoque_maximo"]
        - produtos_criticos["estoque_atual"]
    )

    # Calcula custo estimado
    produtos_criticos["custo_estimado"] = (
        produtos_criticos["quantidade_sugerida"]
        * produtos_criticos["custo_unitario"]
    )
    
    # Seleciona colunas relevantes
    colunas_relevantes = [
        "codigo_produto",
        "produto",
        "estoque_atual",
        "estoque_minimo",
        "estoque_maximo",
        "custo_unitario",
        "quantidade_sugerida",
        "custo_estimado"
    ]

    return produtos_criticos[colunas_relevantes]

def criar_tool_reposicao(df):
    return Tool(
        name="analisar_reposicao",
        func=lambda _: analisar_reposicao(df),
        description=(
            "Analise os produtos que estão abaixo do estoque mínimo "
            "e calcule a quantidade sugerida para reposição e o "
            "custo estimado da compra."
        )
    )