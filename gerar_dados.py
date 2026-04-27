import random
import os
import pandas as pd
from datetime import datetime, timedelta
import numpy as np



QTDE_PEDIDOS = 2000
QTDE_CLIENTES = 400

DIRETORIO_FONTE = "data/fonte"
os.makedirs(DIRETORIO_FONTE, exist_ok=True)


def data_aleatoria(data_Inicio: datetime, data_termino: datetime ):
  periodo = (data_termino - data_Inicio).days
  return (data_Inicio + timedelta(days=random.randint(0, periodo))).strftime("%Y-%m-%d")


PRODUTOS_POR_CATEGORIA = {
    "Eletrônicos":    ["Smartphone", "Notebook", "Tablet", "Fone Bluetooth",
                       "Smartwatch", "Carregador Portátil", "Cabo USB-C"],
    "Vestuário":      ["Camiseta", "Calça Jeans", "Tênis Casual", "Jaqueta",
                       "Moletom", "Vestido", "Sandália"],
    "Casa & Cozinha": ["Panela Antiaderente", "Jogo de Cama", "Toalha",
                       "Liquidificador", "Cafeteira", "Travesseiro"],
    "Esportes":       ["Bicicleta", "Halteres", "Tapete de Yoga", "Mochila Esportiva",
                       "Garrafa Térmica", "Corda de Pular"],
    "Livros":         ["Romance Nacional", "Autoajuda Bestseller", "Livro Técnico Python",
                       "HQ Marvel", "Mangá Demon Slayer", "Atlas Histórico"],
}

REGIOES = ["Sul", "Sudeste", "Centro-Oeste", "Norte", "Nordeste"] #Regioes comuns do Brasil.

STATUS = ["processando", "enviado", "cancelado", "entregue", "entregue", "entregue"]


# gera clientes 
def gerar_clientes():
  # modelo: id, nome, email, regiao, isVip, ano_cadastro
  clientes = []

  NOMES = ["Ana", "Carlos", "Maria", "João", "Fernanda", "Lucas","Juliana", "Pedro", "Beatriz", "Rafael", "Camila", "Diego", "Larissa", "Thiago", "Aline", "Rodrigo", "Natalia", "Bruno", "Gabriela", "Felipe"]
  SOBRENOMES = ["Silva", "Santos", "Oliveira", "Souza", "Costa", "Ferreira", "Alves", "Pereira", "Lima", "Gomes", "Ribeiro", "Carvalho", "Melo", "Araújo", "Rocha", "Mendes", "Nunes", "Martins"]

  for i in range(1, QTDE_CLIENTES, +1):
    nome = f"{random.choice(NOMES)} {random.choice(SOBRENOMES)}"
  
    #5% de chance de nomes com espaços
    if random.random() < 0.05:
      nome = "  " + nome + "  "
    clientes.append({
      "cliente_id": i,
      "nome": nome,
      "email": f"{nome.split()[0]}{i}@cliente.com",
      "regiao": random.choice(REGIOES) if random.random() < 0.90 else "", #10% de chance de não ter a região
      "is_vip": random.random() < 0.20, #20% de chance de ser vip
      "ano_cadastro": random.randint(2000,2026)
    })

  return pd.DataFrame(clientes)

# gera produtos
def gerar_produtos():
 #modelo: id, nome, categoria, preco, marca.
 produtos = []
 contador_id= 1
 for categoria, itens in PRODUTOS_POR_CATEGORIA.items():
   for item in itens:
     preco= {
       "Eletrônicos": random.uniform(80,3500),
       "Vestuário": random.uniform(40,400),
       "Casa & Cozinha": random.uniform(30,600),
       "Esportes": random.uniform(25,1500),
       "Livros": random.uniform(20,120),
     }[categoria]

     produtos.append({
       "produto_id": contador_id,
       "nome": item,
       "categoria": categoria if random.random() > 0.03 else None, #Deve gerar 3% de campos em branco.
       "preco": round(preco, 2),
       "marca": f"Marca {random.choice(["A","B","C","D"])}"
     })
     contador_id += 1

 return  pd.DataFrame(produtos)

# gera pedidos
def gerar_pedidos(id_maximo_cliente: int, id_maximo_produto: int):
  inicio = datetime(2024,1,1)
  termino = datetime(2026,4,30)

  pedidos = []
  for i in range(1,QTDE_PEDIDOS + 1):
    qtde = random.randint(1,10)
    preco = round(random.uniform(15, 4000), 2) # vou ter que por um valor aleatorio (sujo), considere proposital kkk 

    # 3% de quantidades negativas
    if random.random() < 0.03:
      qtde = -qtde

    # 2% de precos nogativos
    if random.random() < 0.02:
      preco = -preco

    status = random.choice(STATUS)
    # 2% de status sujos
    if random.random() < 0.02:
      status = " " + status.upper() + " "

    pedidos.append({
      "pedido_id": i,
      "cliente_id": random.randint(0, id_maximo_cliente),
      "produto_id": random.randint(1, id_maximo_produto),
      "data_compra": data_aleatoria(inicio, termino),
      "quantidade": qtde,
      "preco": preco,
      "status": status
    })
  
  # 1% de cliente_id em branco,tbm vai fazer o id virar float.
  id_null = random.sample(range(QTDE_PEDIDOS), int(QTDE_PEDIDOS * 0.01))
  r_pedidos = pd.DataFrame(pedidos)
  r_pedidos.loc[id_null, "cliente_id"] = np.nan

  return r_pedidos


def main():
  print("Gerando clientes", end="...\n")
  clientes = gerar_clientes()
  clientes.to_csv(f"{DIRETORIO_FONTE}/clientes.csv", index=False)
  print(f"criado | clientes.csv | com {len(clientes)} clientes")

  print("Gerando produtos", end="...\n")
  produtos = gerar_produtos()
  produtos.to_csv(f"{DIRETORIO_FONTE}/produtos.csv", index=False)
  print(f"criado | produtos.csv | com {len(produtos)} produtos")

  print("Gerando pedidos", end="...\n")
  pedidos = gerar_pedidos(len(clientes), len(produtos))
  pedidos.to_csv(f"{DIRETORIO_FONTE}/pedidos.csv", index=False)
  print(f"criado | pedidos.csv | com {len(pedidos)} pedidos")

  print(f"\n Arquivos salver em: {DIRETORIO_FONTE}/")

if __name__ == "__main__":
  main()