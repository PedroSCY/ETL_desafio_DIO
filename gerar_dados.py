import random
import os
import pandas as pd

os.makedirs("data", exist_ok=True)


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


# gera clientes 
def gerar_clientes():
  # modelo: id, nome, email, regiao, isVip, ano_cadastro
  clientes = []

  NOMES = ["Ana", "Carlos", "Maria", "João", "Fernanda", "Lucas","Juliana", "Pedro", "Beatriz", "Rafael", "Camila", "Diego", "Larissa", "Thiago", "Aline", "Rodrigo", "Natalia", "Bruno", "Gabriela", "Felipe"]
  SOBRENOMES = ["Silva", "Santos", "Oliveira", "Souza", "Costa", "Ferreira", "Alves", "Pereira", "Lima", "Gomes", "Ribeiro", "Carvalho", "Melo", "Araújo", "Rocha", "Mendes", "Nunes", "Martins"]

  for i in range(50):
    nome = f"{random.choice(NOMES)} {random.choice(SOBRENOMES)}"
  
    #5% de chance de nomes com espaços
    if random.random() < 0.05:
      nome = "  " + nome + "  "
    clientes.append({
      "cliente_id": i,
      "nome": nome,
      "email": f"{nome.split()[0]}{i}@cliente.com",
      "regiao": random.choice(REGIOES) if random.random() < 0.90 else "", #10% de chance de não ter a região
      "idVip": random.random() < 0.20, #20% de chance de ser vip
      "ano_cadastro": random.randint(2000,2026)
    })

  return pd.DataFrame(clientes)

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



def main():
  print("Gerando clientes", end="...\n")
  clientes = gerar_clientes()
  clientes.to_csv("data/clientes.csv", index=False)
  print(f"criado | clientes.csv | com {len(clientes)} clientes")

  print("Gerando produtos", end="...\n")
  produtos = gerar_produtos()
  produtos.to_csv("data/produtos.csv", index=False)
  print(f"criado | produtos.csv | com {len(produtos)} produtos")

if __name__ == "__main__":
  main()