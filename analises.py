import pandas as pd

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

def analisar_promocoes(df):
    # Filtra produtos sem venda há 30 dias ou mais
    produtos_promocao = df[
        df["dias_sem_venda"] >= 30
    ].copy()

    # Define os cenários de desconto que serão analisados
    descontos = [10, 20, 30]

    resultados = []

    # Define a classificação de acordo com a margem
    def classificar_margem(margem):
        if margem >= 25:
            return "Promoção recomendada"
        elif margem >= 15:
            return "Promoção possível"
        else:
            return "Promoção não recomendada"

    # Executa a análise para cada percentual de desconto
    for desconto in descontos:

        # Cria uma cópia dos produtos para este cenário
        cenario = produtos_promocao.copy()

        # Calcula o fator que representa o preço após o desconto
        fator_desconto = 1 - (desconto / 100)

        # Calcula o preço promocional
        cenario["preco_promocional"] = (
            cenario["preco_venda"] * fator_desconto
        )

        # Calcula o desconto em reais
        cenario["desconto_reais"] = (
            cenario["preco_venda"]
            - cenario["preco_promocional"]
        )

        # Calcula a margem percentual após o desconto
        cenario["margem_promocional"] = (
            (
                cenario["preco_promocional"]
                - cenario["custo_unitario"]
            )
            / cenario["preco_promocional"]
            * 100
        )

        cenario["valor_estoque_parado"] = (
            cenario["estoque_atual"]
            * cenario["custo_unitario"]
        )

        # Registra o percentual de desconto utilizado
        cenario["desconto_percentual"] = desconto

        # Classifica o cenário de promoção
        cenario["classificacao"] = (
            cenario["margem_promocional"].apply(classificar_margem)
        )

        # Adiciona o cenário à lista de resultados
        resultados.append(cenario)

    # Junta todos os cenários em um único DataFrame
    resultado_final = pd.concat(
        resultados,
        ignore_index=True
    )

    # Seleciona colunas relevantes
    colunas_relevantes = [
        "codigo_produto",
        "produto",
        "categoria",
        "estoque_atual",
        "custo_unitario",
        "preco_venda",
        "desconto_percentual",
        "preco_promocional",
        "desconto_reais",
        "dias_sem_venda",
        "valor_estoque_parado",
        "margem_promocional",
        "classificacao"
    ]

    return resultado_final[colunas_relevantes]