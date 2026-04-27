## 📋 Sobre o Projeto

| Item | Detalhe |
|------|---------|
| **Cenário** | E-commerce com pedidos, clientes e produtos |
| **Volume** | 2.000 pedidos · 400 clientes · 60 produtos |
| **Período** | 2024 – 2026 |
| **Stack** | Python · Pandas · NumPy · OpenPyXL |

### EXTRACT
- Lê três arquivos CSV que simulam fontes de dados distintas

### TRANSFORM
1. **Limpeza** — remove linhas inválidas (quantidade/preço negativos), padroniza textos com `str.strip()` e `str.title()`, preenche nulos
2. **Joins** — enriquece pedidos com nome, região e VIP do cliente + categoria, preço e marca do produto
3. **Colunas derivadas** — `valor_total`, `desconto` (10% para VIPs), `valor_final`, `ano`, `mes`, `classe_pedido`
4. **Agregação** — tabela mensal por categoria e região com 7 métricas de negócio

### LOAD
- `etl_vendas.xlsx` — arquivo Excel com duas abas (Resumo + Detalhado)

*Projeto desenvolvido para desafio de codigo em Python da DIO.*
