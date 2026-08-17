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

    descontos = [10, 20, 30]

    # Guarda os resultados de cada cenário
    cenarios = []

    for desconto in descontos:

        cenario = produtos_promocao[
            [
                "codigo_produto",
                "produto",
                "categoria",
                "estoque_atual",
                "custo_unitario",
                "preco_venda",
                "dias_sem_venda"
            ]
        ].copy()

        # Calcula o preço promocional
        fator_desconto = 1 - (desconto / 100)

        cenario["preco_promocional"] = (
            cenario["preco_venda"] * fator_desconto
        )

        # Calcula o desconto em reais
        cenario["desconto_reais"] = (
            cenario["preco_venda"]
            - cenario["preco_promocional"]
        )

        # Calcula a margem após o desconto
        cenario["margem_promocional"] = (
            (
                cenario["preco_promocional"]
                - cenario["custo_unitario"]
            )
            / cenario["preco_promocional"]
            * 100
        )

        # Guarda o cenário
        cenario = cenario[
            [
                "codigo_produto",
                "preco_promocional",
                "desconto_reais",
                "margem_promocional"
            ]
        ]

        cenario = cenario.rename(
            columns={
                "preco_promocional": f"preco_{desconto}%",
                "desconto_reais": f"desconto_reais_{desconto}%",
                "margem_promocional": f"margem_{desconto}%"
            }
        )

        cenarios.append(cenario)

    # Começa com os dados básicos dos produtos
    resultado_final = produtos_promocao[
        [
            "codigo_produto",
            "produto",
            "categoria",
            "estoque_atual",
            "custo_unitario",
            "preco_venda",
            "dias_sem_venda"
        ]
    ].copy()

    # Adiciona os três cenários lado a lado
    for cenario in cenarios:
        resultado_final = resultado_final.merge(
            cenario,
            on="codigo_produto",
            how="left"
        )

    # Calcula o valor do estoque parado
    resultado_final["valor_estoque_parado"] = (
        resultado_final["estoque_atual"]
        * resultado_final["custo_unitario"]
    )

    # Classifica cada cenário de acordo com a margem
    def classificar_margem(margem):
        if margem >= 25:
            return "Promoção recomendada"
        elif margem >= 15:
            return "Promoção possível"
        else:
            return "Promoção não recomendada"

    resultado_final["classificacao_10%"] = (
        resultado_final["margem_10%"]
        .apply(classificar_margem)
    )

    resultado_final["classificacao_20%"] = (
        resultado_final["margem_20%"]
        .apply(classificar_margem)
    )

    resultado_final["classificacao_30%"] = (
        resultado_final["margem_30%"]
        .apply(classificar_margem)
    )

    # Organiza as colunas finais
    colunas_relevantes = [
        "codigo_produto",
        "produto",
        "categoria",
        "estoque_atual",
        "custo_unitario",
        "preco_venda",

        "preco_10%",
        "desconto_reais_10%",
        "margem_10%",
        "classificacao_10%",

        "preco_20%",
        "desconto_reais_20%",
        "margem_20%",
        "classificacao_20%",

        "preco_30%",
        "desconto_reais_30%",
        "margem_30%",
        "classificacao_30%",

        "dias_sem_venda",
        "valor_estoque_parado"
    ]

    return resultado_final[colunas_relevantes]

def analisar_orcamento(df, orcamento):
    # Seleciona produtos que estão abaixo do estoque mínimo
    produtos_reposicao = df[
        df["estoque_atual"] < df["estoque_minimo"]
    ].copy()

    # Calcula a quantidade necessária para atingir o estoque máximo
    produtos_reposicao["quantidade_sugerida"] = (
        produtos_reposicao["estoque_maximo"]
        - produtos_reposicao["estoque_atual"]
    )

    # Calcula o custo total da reposição de cada produto
    produtos_reposicao["custo_estimado"] = (
        produtos_reposicao["quantidade_sugerida"]
        * produtos_reposicao["custo_unitario"]
    )

    # Calcula quanto o estoque atual representa em relação ao estoque mínimo
    produtos_reposicao["nivel_estoque"] = (
        produtos_reposicao["estoque_atual"]
        / produtos_reposicao["estoque_minimo"]
    )

    # Ordena pelos produtos mais críticos primeiro
    produtos_reposicao = produtos_reposicao.sort_values(
        by="nivel_estoque"
    )

    selecionados = []
    valor_utilizado = 0

    # Percorre os produtos priorizados
    for _, produto in produtos_reposicao.iterrows():

        custo = produto["custo_estimado"]

        # Verifica se a compra cabe no orçamento
        if valor_utilizado + custo <= orcamento:

            selecionados.append(produto)
            valor_utilizado += custo

    # Converte a lista de produtos selecionados em DataFrame
    resultado = pd.DataFrame(selecionados)

    # Caso nenhum produto caiba no orçamento
    if resultado.empty:
        return {
            "produtos": resultado,
            "valor_utilizado": 0,
            "valor_disponivel": orcamento,
            "mensagem": "Nenhum produto para reposição cabe no orçamento informado."
        }

    # Calcula o saldo restante
    valor_disponivel = orcamento - valor_utilizado

    colunas_relevantes = [
        "codigo_produto",
        "produto",
        "estoque_atual",
        "estoque_minimo",
        "quantidade_sugerida",
        "custo_unitario",
        "custo_estimado",
        "nivel_estoque"
    ]

    return {
        "produtos": resultado[colunas_relevantes],
        "valor_utilizado": valor_utilizado,
        "valor_disponivel": valor_disponivel,
        "mensagem": "Produtos priorizados de acordo com o nível de estoque e o orçamento informado."
    }

def analisar_risco_ruptura(df):
    # Calcula o nível atual do estoque em relação ao estoque mínimo
    resultado = df.copy()

    resultado["nivel_estoque"] = (
        resultado["estoque_atual"] / resultado["estoque_minimo"]
    )

    # Classifica o risco de ruptura
    def classificar_risco(nivel):
        if nivel <= 0.5:
            return "Risco alto"
        elif nivel <= 0.8:
            return "Risco médio"
        else:
            return "Risco baixo"

    resultado["risco_ruptura"] = (
        resultado["nivel_estoque"].apply(classificar_risco)
    )

    # Seleciona apenas produtos com risco alto ou médio
    resultado = resultado[
        resultado["risco_ruptura"].isin(
            ["Risco alto", "Risco médio"]
        )
    ]

    # Ordena do maior risco para o menor
    resultado = resultado.sort_values(
        "nivel_estoque"
    )

    colunas_relevantes = [
        "codigo_produto",
        "produto",
        "categoria",
        "estoque_atual",
        "estoque_minimo",
        "nivel_estoque",
        "risco_ruptura"
    ]

    return resultado[colunas_relevantes]

def analisar_por_categoria(df):
    resultado = df.copy()

    # Identifica produtos abaixo do estoque mínimo
    resultado["abaixo_minimo"] = (
        resultado["estoque_atual"] < resultado["estoque_minimo"]
    )

    # Identifica produtos encalhados
    resultado["encalhado"] = (
        resultado["dias_sem_venda"] >= 30
    )

    # Calcula o nível de estoque
    resultado["nivel_estoque"] = (
        resultado["estoque_atual"] / resultado["estoque_minimo"]
    )

    # Identifica risco de ruptura
    resultado["risco_alto"] = (
        resultado["nivel_estoque"] <= 0.5
    )

    # Calcula o valor parado no estoque
    resultado["valor_estoque_parado"] = (
        resultado["estoque_atual"]
        * resultado["custo_unitario"]
    )

    # Agrupa os indicadores por categoria
    resumo = (
        resultado
        .groupby("categoria")
        .agg(
            total_produtos=("codigo_produto", "count"),
            produtos_abaixo_minimo=("abaixo_minimo", "sum"),
            produtos_encalhados=("encalhado", "sum"),
            produtos_risco_alto=("risco_alto", "sum"),
            valor_estoque_parado=("valor_estoque_parado", "sum")
        )
        .reset_index()
    )

    # Calcula o percentual de produtos abaixo do mínimo
    resumo["percentual_abaixo_minimo"] = (
        resumo["produtos_abaixo_minimo"]
        / resumo["total_produtos"]
        * 100
    )

    # Ordena pelas categorias com maior valor parado
    resumo = resumo.sort_values(
        "valor_estoque_parado",
        ascending=False
    )

    return resumo

def analisar_validade(df):
    # Cria uma cópia para não alterar o DataFrame original
    produtos = df.copy()

    # Converte a coluna de validade para data
    produtos["validade"] = pd.to_datetime(
        produtos["validade"],
        errors="coerce"
    )

    # Considera a data atual como referência
    hoje = pd.Timestamp.today().normalize()

    # Calcula quantos dias faltam para o vencimento
    produtos["dias_para_vencer"] = (
        produtos["validade"] - hoje
    ).dt.days

    # Classifica os produtos de acordo com a proximidade do vencimento
    def classificar_validade(dias):
        if pd.isna(dias):
            return "Data de validade inválida"
        elif dias < 0:
            return "Produto vencido"
        elif dias <= 30:
            return "Validade crítica"
        elif dias <= 60:
            return "Validade próxima"
        else:
            return "Validade normal"

    produtos["classificacao_validade"] = (
        produtos["dias_para_vencer"].apply(classificar_validade)
    )

    # Mantém somente produtos que precisam de atenção
    resultado = produtos[
        produtos["classificacao_validade"].isin([
            "Produto vencido",
            "Validade crítica",
            "Validade próxima"
        ])
    ].copy()

    # Ordena do mais urgente para o menos urgente
    resultado = resultado.sort_values(
        by="dias_para_vencer"
    )

    # Seleciona as informações relevantes
    colunas_relevantes = [
        "codigo_produto",
        "produto",
        "categoria",
        "estoque_atual",
        "validade",
        "dias_para_vencer",
        "classificacao_validade"
    ]

    return resultado[colunas_relevantes]