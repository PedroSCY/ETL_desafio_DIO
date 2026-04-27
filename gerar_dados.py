import random
import os
import pandas as pd

os.makedirs("data", exist_ok=True)

# gera clientes 
def gerar_clientes():
  # modelo: id, nome, email, regiao, isVip, ano_cadastro
  clientes = []

  NOMES = ["Ana", "Carlos", "Maria", "João", "Fernanda", "Lucas","Juliana", "Pedro", "Beatriz", "Rafael", "Camila", "Diego", "Larissa", "Thiago", "Aline", "Rodrigo", "Natalia", "Bruno", "Gabriela", "Felipe"]
  SOBRENOMES = ["Silva", "Santos", "Oliveira", "Souza", "Costa", "Ferreira", "Alves", "Pereira", "Lima", "Gomes", "Ribeiro", "Carvalho", "Melo", "Araújo", "Rocha", "Mendes", "Nunes", "Martins"]
  REGIOES = ["Sul", "Sudeste", "Centro-Oeste", "Norte", "Nordeste"] #Regioes comuns do Brasil.

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
  
def main():
  print("Gerando clientes", end="...\n")
  
  clientes = gerar_clientes()
  #print(clientes)

  clientes.to_csv("data/clientes.csv", index=False)

  print(f"criado | clientes.csv | com {len(clientes)} clientes")

if __name__ == "__main__":
  main()