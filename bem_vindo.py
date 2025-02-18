import os
import pandas as pd

def boas_vindas():
    print("\n\033[1m=== SISTEMA DE GESTÃO ZOOTÉCNICA ===")
    print("===      IATF - Controle Total      ===\033[0m\n")
    
def buscar_cliente():
    nome = input("Digite o nome do cliente: ").strip()
    clientes_dir = os.path.join(os.path.dirname(__file__), 'clientes')
    cliente_pasta = os.path.join(clientes_dir, nome)
    
    # Verificar se o diretório do cliente existe
    if os.path.exists(cliente_pasta):
        arquivo_dados = os.path.join(cliente_pasta, 'dados_cliente.csv')
        
        # Verificar se o arquivo de dados existe
        if os.path.exists(arquivo_dados):
            df = pd.read_csv(arquivo_dados)
            print("\n\033[92mCliente encontrado:\033[0m")
            print(df.to_string(index=False))
            return True, cliente_pasta
        else:
            print(f"O arquivo 'dados_cliente.csv' não foi encontrado na pasta do cliente {nome}.")
    else:
        print(f"O cliente {nome} não foi encontrado.")
    
    return False, cliente_pasta


def criar_cliente():
    nome = input("Nome do novo cliente: ").strip()
    clientes_dir = os.path.join(os.path.dirname(__file__), 'clientes')
    cliente_pasta = os.path.join(clientes_dir, nome)
    
    if not os.path.exists(cliente_pasta):
        os.makedirs(cliente_pasta)
        dados = {
            'Nome': nome,
            'Endereço': input("Endereço: "),
            'Contato': input("Telefone: "),
            'Tipo': input("Atividade (Corte/Leite/Esporte): "),
            'Cadastro': pd.Timestamp.now().strftime("%d/%m/%Y")
        }
        pd.DataFrame([dados]).to_csv(os.path.join(cliente_pasta, 'dados_cliente.csv'), index=False)
        print("\n\033[92mCliente cadastrado com sucesso!\033[0m")
        return True, cliente_pasta
    print("\033[91mCliente já existe!\033[0m")
    return False, cliente_pasta