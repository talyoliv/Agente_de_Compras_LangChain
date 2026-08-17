from langchain_core.tools import Tool

from analises import (
    analisar_reposicao,
    analisar_encalhados,
    analisar_promocoes,
    analisar_orcamento,
    analisar_risco_ruptura
)


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


def criar_tool_encalhados(df):
    return Tool(
        name="analisar_encalhados",
        func=lambda _: analisar_encalhados(df),
        description=(
            "Analise os produtos que estão encalhados no estoque, "
            "considerando produtos sem venda há 30 dias ou mais, "
            "e informe o valor investido no estoque parado."
        )
    )

def criar_tool_promocoes(df):
    return Tool(
        name="analisar_promocoes",
        func=lambda _: analisar_promocoes(df),
        description=(
            "Analise os produtos encalhados e avalie diferentes "
            "percentuais de desconto, calculando o preço promocional, "
            "o desconto em reais, a margem promocional e classificando "
            "as oportunidades de promoção."
        )
    )

def criar_tool_orcamento(df):
    return Tool(
        name="analisar_orcamento",
        func=lambda orcamento: analisar_orcamento(
            df,
            float(orcamento)
        ),
        description=(
            "Analise quais produtos devem ser priorizados para reposição "
            "considerando um orçamento informado pelo usuário. "
            "Informe os produtos selecionados, a quantidade sugerida, "
            "o custo estimado, o valor utilizado e o saldo disponível."
        )
    )

def criar_tool_risco_ruptura(df):
    return Tool(
        name="analisar_risco_ruptura",
        func=lambda _: analisar_risco_ruptura(df),
        description=(
            "Analise os produtos que estão próximos de uma ruptura de estoque, "
            "considerando o nível de estoque atual em relação ao estoque mínimo. "
            "Classifique os produtos em risco alto ou risco médio e mostre "
            "quais produtos precisam de atenção."
        )
    )