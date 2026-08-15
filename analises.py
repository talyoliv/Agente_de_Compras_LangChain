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

def analisar_encalhados(df):
    # Filtra produtos sem venda há 30 dias ou mais
    produtos_encalhados = df[
        df["dias_sem_venda"] >= 30
    ].copy()

    # Calcula o valor investido no estoque parado
    produtos_encalhados["valor_estoque_parado"] = (
        produtos_encalhados["estoque_atual"]
        * produtos_encalhados["custo_unitario"]
    )

    # Seleciona colunas relevantes
    colunas_relevantes = [
        "codigo_produto",
        "produto",
        "categoria",
        "estoque_atual",
        "custo_unitario",
        "preco_venda",
        "dias_sem_venda",
        "valor_estoque_parado"
    ]

    return produtos_encalhados[colunas_relevantes]