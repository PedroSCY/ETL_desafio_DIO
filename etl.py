import pandas as pd
import numpy as np
import os
from datetime import datetime

DIRETORIO_FONTE = "data/fonte"
DIRETORIO_SAIDA = "data/resultado"

os.makedirs(DIRETORIO_FONTE, exist_ok=True)
os.makedirs(DIRETORIO_SAIDA, exist_ok=True)


def extracao():

  print("\n [EXTRACT] Lendo arquivos brutos...")

  pedidos = pd.read_csv(f"{DIRETORIO_FONTE}/pedidos.csv")
  clientes = pd.read_csv(f"{DIRETORIO_FONTE}/clientes.csv")
  produtos = pd.read_csv(f"{DIRETORIO_FONTE}/produtos.csv")

  print(f"orders.csv    -> {len(pedidos):,} linhas")
  print(f"customers.csv -> {len(clientes):,} linhas")
  print(f"products.csv  -> {len(produtos):,} linhas")

  return clientes, produtos, pedidos

def transformacao(clientes: pd.DataFrame, produtos: pd.DataFrame, pedidos: pd.DataFrame):

  print("\n [TRANSFORM] Iniciando transformações...")

  print("\n 1/4 Limpeza de dados")

  # converte datas
  pedidos["data_compra"] = pd.to_datetime(pedidos["data_compra"])

  # remove valores negativos e na de clientes
  antes = len(pedidos)
  pedidos = pedidos[pedidos["quantidade"]>0]
  pedidos = pedidos[pedidos["preco"]>0]
  pedidos = pedidos.dropna(subset=["cliente_id", "produto_id"])
  depois = len(pedidos)
  print(f"Linhas removidas (dados inválidos): {antes - depois}")

  # padroniza os status do pedido
  pedidos["status"] = pedidos["status"].str.strip().str.lower()

  # padroniza nome do cliente
  clientes["nome"] = clientes["nome"].str.strip().str.title()

  # preenche categorias em branco
  produtos["categoria"] = produtos['categoria'].fillna("Indefinido")

  # renomea coluna de preco do pedido
  pedidos = pedidos.rename(columns={"preco": "valor_total"})

  # renomea coluna de preco do produto
  produtos = produtos.rename(columns={"preco": "preco_und"})

  print("2/4 join de tabelas")

  # join clientes - pedidos
  df = pedidos.merge(clientes, on="cliente_id", how="left")
  
  # join clientes/pedidos - produtos
  df = df.merge(produtos, on="produto_id", how="left")

  print("3/4 Criando novas colunas")

  # corrije o valor do pedido de acordo com o valor do produto
  df["valor_total"] = df["quantidade"] * df["preco_und"]

  # aplica 10% de desconto pra clientes vip
  df["desconto"] = np.where(df["is_vip"] == True, df["valor_total"] * 0.10, 0.0)
  df["valor_final"] = df["valor_total"] - df["desconto"]

  # extrai dados da data da compra
  df["ano"] = df["data_compra"].dt.year
  df["mes"] = df["data_compra"].dt.month
  df["mes_ext"] = df["data_compra"].dt.strftime("%b")
  df["dia_ext"] = df["data_compra"].dt.day_name()

  # Classifica os pedidos
  faixas_pedidos = [0, 100, 500, 1000, np.inf]
  faixas = ["Baixa", "Média", "Alta", "Premium"]
  df["classe_pedido"] = pd.cut(df["valor_final"], bins=faixas_pedidos, labels=faixas)

  print("4/4 Gerando tabela analítica consolidada")

  sumario = (
     df.groupby(["ano", "mes", "mes_ext", "categoria", "regiao"])
     .agg(
        total_pedidos = ("pedido_id", "count"),
        total_items = ("quantidade", "sum"),
        total_vendido = ("valor_total", "sum"),
        total_desconto = ("desconto", "sum"),
        total_final = ("valor_final", "sum"),
        avg_ticket = ("valor_final", "mean"),
        unique_clientes = ("cliente_id", "nunique")
     ).reset_index().sort_values(["ano", "mes"])
  )

  colunas_valores = ["total_vendido", "total_desconto", "total_final", "avg_ticket"]
  sumario[colunas_valores] = sumario[colunas_valores].round(2)

  print(f"\n Tabela analítica gerada: {sumario.shape[0]} linhas x {sumario.shape[1]} colunas")

  return df, sumario 


def load(df_detalhado: pd.DataFrame, df_sumario: pd.DataFrame):
   
  print("\n [LOAD] Salvando resultados...")

  excel_path = f"{DIRETORIO_SAIDA}/etl_vendas.xlsx"

  with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
     df_sumario.to_excel(writer, sheet_name="Resumo Mensal", index=False)
     df_detalhado.to_excel(writer, sheet_name="Detalhado", index=False)

  print(f" V {excel_path} :)")

def run_etl():
    inicio = datetime.now()
    print("=" * 50)
    print("ETL — E-COMMERCE VENDAS")
    print(f" Início: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # clientes, produtos e pedidos
    cli, pro , ped = extracao()
    df_detalhado, df_sumario = transformacao(cli, pro, ped)
    load(df_detalhado, df_sumario)

    encerramento = (datetime.now() - inicio).total_seconds()
    print(f"\n ETL concluído em {encerramento:.2f}s\n")


if __name__ == "__main__":
    run_etl()