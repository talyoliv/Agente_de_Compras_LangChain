# 🧹 Agente de Compras — LangChain

Agente inteligente para análise de estoque e apoio à tomada de decisões na área de compras.

## 📌 Sobre o projeto

O **Agente de Compras** é uma aplicação desenvolvida em Python que utiliza Inteligência Artificial para analisar dados de estoque de produtos de limpeza e auxiliar o comprador na identificação de problemas e oportunidades.

A aplicação permite realizar perguntas em linguagem natural, como:

> "Tenho R$ 5.000 para comprar. O que devo priorizar?"

A partir da pergunta, o agente identifica qual ferramenta de análise deve ser utilizada, processa os dados do estoque e apresenta uma resposta contextualizada.

O projeto foi desenvolvido como parte do desafio **ONE AI FOR TECH**, utilizando LangChain para construção do agente e ferramentas especializadas para as diferentes análises.

---

## 🎯 Objetivo

O objetivo do projeto é transformar dados de estoque em informações úteis para tomada de decisão, reduzindo a necessidade de análises manuais e permitindo que o comprador consulte os dados utilizando linguagem natural.

O agente foi desenvolvido para apoiar decisões relacionadas a:

- 📦 Reposição de estoque
- 🐌 Produtos encalhados
- 🏷️ Oportunidades de promoção
- 💰 Priorização de compras conforme orçamento
- ⚠️ Risco de ruptura
- 📊 Análise por categoria
- 📅 Produtos próximos do vencimento

---

## 🏗️ Arquitetura da solução

A aplicação possui uma arquitetura baseada em um agente de IA com ferramentas especializadas.

```text
                    ┌─────────────────────┐
                    │      Usuário        │
                    │ Pergunta em texto   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Interface        │
                    │     Streamlit       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Agente LangChain  │
                    │                     │
                    │     ChatGroq        │
                    └──────────┬──────────┘
                               │
                 Escolhe a ferramenta adequada
                               │
        ┌──────────┬───────────┼───────────┬───────────┐
        ▼          ▼           ▼           ▼           ▼
   Reposição  Encalhados  Promoções   Orçamento   Ruptura
        │          │           │           │           │
        └──────────┴───────────┼───────────┴───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
          Análise por categoria          Validade
                 │                           │
                 └─────────────┬─────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Dados do estoque    │
                    │       CSV           │
                    └─────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Resposta ao usuário │
                    └─────────────────────┘
```

## Fluxo da aplicação
1. O usuário envia uma pergunta pela interface.
2. O agente recebe a pergunta.
3. O modelo de linguagem interpreta a intenção.
4. O agente seleciona a ferramenta de análise adequada.
5. A ferramenta processa os dados do arquivo CSV utilizando Pandas.
6. O resultado da análise retorna para o agente.
7. O modelo interpreta os resultados e gera uma resposta em linguagem natural.
8. A resposta é apresentada na interface.

## 🧰 Tecnologias utilizadas

### Linguagem
- Python

### Inteligência Artificial
- LangChain — construção do agente e gerenciamento das ferramentas.
- Groq — execução do modelo de linguagem.
- ChatGroq — integração do modelo com o LangChain.
- OpenAI GPT-OSS 120B — modelo utilizado pelo agente.

### Processamento de dados
- Pandas — leitura e análise dos dados do estoque.

### Interface
- Streamlit — construção da interface web da aplicação.

### Gerenciamento de configuração
- python-dotenv — carregamento da chave da API através de variável de ambiente.


## 📁 Estrutura do projeto
```
Agente_de_Compras_LangChain/
│
├── dados/
│   └── estoque_produtos_limpeza_challenge.csv
│
├── analises.py
├── tools.py
├── agente.py
├── app.py
├── carregar_dados.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Principais arquivos

```analises.py```

Contém as funções responsáveis pelos cálculos e análises dos dados de estoque.

Entre elas:

- ```analisar_reposicao()```
- ```analisar_encalhados()```
- ```analisar_promocoes()```
- ```analisar_orcamento()```
- ```analisar_risco_ruptura()```
- ```analisar_por_categoria()```
- ```analisar_validade()```

```tools.py```

Transforma as funções de análise em ferramentas que podem ser utilizadas pelo agente LangChain.

```agente.py```

Configura o modelo de linguagem, carrega as ferramentas e cria o agente responsável por interpretar as perguntas do usuário.

```app.py```

Contém a interface Streamlit utilizada para interação com o agente.

```carregar_dados.py```

Utilizado para carregar os dados e testar individualmente as análises antes da integração com o agente.

## 🔎 Análises disponíveis

### 📦 Reposição

Identifica produtos abaixo do estoque mínimo e calcula:

- quantidade sugerida para compra;
- custo unitário;
- custo estimado da reposição;
- nível de estoque.

### Exemplo de pergunta

> **"Quais produtos precisam de reposição?"**

### 🐌 Produtos encalhados

Identifica produtos sem venda há 30 dias ou mais e calcula o valor investido no estoque parado.

### Exemplo de pergunta

> **"Quais produtos estão encalhados?"**
 
### 🏷️ Promoções

Analisa produtos encalhados e simula diferentes percentuais de desconto.

A análise considera:

- preço promocional;
- desconto em reais;
- margem após o desconto;
- classificação da oportunidade.

O objetivo é permitir que o comprador compare cenários antes de definir uma promoção.

### Exemplo de pergunta

> **"Quais produtos têm oportunidade de promoção?"**

### 💰 Orçamento de compra

Permite informar um orçamento máximo e identificar quais produtos devem ser priorizados.

### Exemplo

> **"Tenho R$ 5.000 para comprar. O que devo priorizar?"**

A ferramenta considera o nível de estoque e seleciona produtos dentro do limite informado.

### Exemplo de resultado
```
Valor total utilizado: R$ 4.985,90
Saldo disponível: R$ 14,10
```

### ⚠️ Risco de ruptura

Avalia o nível atual do estoque em relação ao estoque mínimo e classifica os produtos de acordo com o risco de ruptura.

### Exemplo de pergunta

> **"Quais produtos estão em risco de ruptura?"**

O agente pode identificar, por exemplo:

```
Água Sanitária 1L — Risco alto
Luva de Limpeza M — Risco alto
Saco para Lixo 100L c/25 — Risco alto
```

### 📊 Análise por categoria

Agrupa os indicadores por categoria para identificar onde estão concentrados os principais problemas.

A análise considera:

- quantidade total de produtos;
- produtos abaixo do mínimo;
- produtos encalhados;
- produtos em risco alto de ruptura;
- valor de estoque parado;
- percentual abaixo do estoque mínimo.
- Exemplo de pergunta

> **"Quais categorias têm os maiores problemas?"**

A análise pode revelar, por exemplo, categorias com 100% dos produtos abaixo do estoque mínimo, indicando necessidade de atenção imediata.

### 📅 Validade

Identifica produtos próximos do vencimento e classifica a situação de acordo com os dias restantes.

### Exemplo de pergunta

> **"Quais produtos estão próximos do vencimento e quais precisam de ação imediata?"**

A ferramenta apresenta:

- produto;
- categoria;
- estoque atual;
- data de validade;
- dias para vencer;
- classificação da validade.

Produtos com prazo mais curto são destacados como validade crítica, permitindo que o comprador priorize ações comerciais antes que ocorram perdas.

## 💬 Exemplos de perguntas

O agente consegue interpretar perguntas como:

- ```Quais produtos precisam de reposição?```
- ```Quais produtos estão encalhados?```
- ```Quais produtos têm oportunidade de promoção?```
- ```Tenho R$ 5.000 para comprar. O que devo priorizar?```
- ```Quais produtos estão em risco de ruptura?```
- ```Quais categorias têm os maiores problemas?```
- ```Quais produtos estão próximos do vencimento?```
- ```Quais produtos estão próximos do vencimento e quais precisam de ação imediata?```

## 📊 Exemplos de respostas geradas
### Exemplo 1 — Risco de ruptura

Pergunta:

> **"Quais produtos estão em risco de ruptura?"**

Resposta resumida:

| Produto              	   | Nível de estoque | Risco   |
| :----------------------- | ---------------: | :-----: |
| Água Sanitária 1L        |	         0,34 | 🔴 Alto |
| Luva de Limpeza M	       |             0,37 | 🔴 Alto |
| Saco para Lixo 100L c/25 |	         0,40 | 🔴 Alto |
| Desengraxante 1L         |	         0,47 | 🔴 Alto |
| Álcool 70% 1L            |	         0,48 | 🔴 Alto |

O agente recomenda priorizar a reposição dos produtos classificados como risco alto.

### Exemplo 2 — Orçamento

Pergunta:

> **"Tenho R$ 5.000 para comprar. O que devo priorizar?"**

Resultado obtido no teste:

```
Valor utilizado: R$ 4.985,90
Saldo disponível: R$ 14,10
```

A análise prioriza os produtos com menor nível de estoque dentro do orçamento disponível.

### Exemplo 3 — Validade

Pergunta:

> **"Quais produtos estão próximos do vencimento e quais precisam de ação imediata?"**

Entre os produtos classificados como validade crítica estão:

| Produto                | Estoque | Dias para vencer |
| ---------------------- | ------: | ---------------: |
| Luva de Limpeza M      |      11 |               17 |
| Água Sanitária 1L      |      12 |               19 |
| Álcool 70% 1L          |      19 |               20 |
| Sabão em Pó 1kg        |     125 |               22 |
| Detergente Limão 500ml |      75 |               24 |

O agente recomenda ações comerciais para acelerar o giro dos produtos com menor prazo de validade.

## 🚀 Como executar o projeto
1. **Clone o repositório**

```
git clone https://github.com/talyoliv/Agente_de_Compras_LangChain.git
cd Agente_de_Compras_LangChain
```

2. **Crie o ambiente virtual**
```
python -m venv .venv
```

3. **Ative o ambiente virtual**

No Windows PowerShell:
```
.venv\Scripts\Activate.ps1
```

4. **Instale as dependências**
```
pip install -r requirements.txt
```

5. **Configure a chave da API**

Crie um arquivo .env na raiz do projeto:
```
GROQ_API_KEY=sua_chave_aqui
```

6. **Execute a aplicação**

Com o ambiente virtual ativado:
```
streamlit run app.py
```
A aplicação será disponibilizada pelo Streamlit no navegador.


## 🧪 Testando as análises

Antes de utilizar a interface, também é possível testar as análises diretamente através do arquivo:
```
python carregar_dados.py
```

Esse arquivo permite verificar os resultados das ferramentas individualmente.

Para testar o agente diretamente pelo terminal:
```
python agente.py
```

## 🔐 Segurança

O projeto utiliza uma variável de ambiente para armazenar a chave da API.

O arquivo .env deve permanecer fora do controle de versão e ser incluído no .gitignore.

Exemplo:
```
.env
.venv/
__pycache__/
```

## 📚 Aprendizados

Durante o desenvolvimento do projeto foram trabalhados conceitos de:

- construção de agentes com LangChain;
- criação e integração de ferramentas;
- function/tool calling;
- integração com modelos de linguagem;
- processamento de dados com Pandas;
- análise de estoque;
- construção de interfaces com Streamlit;
- gerenciamento de variáveis de ambiente;
- testes e depuração de aplicações com IA;
- interação entre código determinístico e IA generativa.

##👩‍💻 Projeto

### Agente de Compras — LangChain

Projeto desenvolvido para o desafio **ONE AI FOR TECH**, com foco na aplicação de Inteligência Artificial para análise de estoque e apoio à tomada de decisão em compras.

## ☁️ Cloud Computing Service

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://seu-app.streamlit.app)


**Deploy:**  
👉 [Acesse o Agente de Compras aqui](https://agentedecompraslangchaintalita.streamlit.app/)


