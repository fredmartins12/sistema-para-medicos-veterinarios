import os
import pandas as pd

def buscar_relatorios(cliente_pasta):
    print("\nBuscando Relatórios...")
    
    if not os.path.exists(cliente_pasta):
        print(f"A pasta do cliente {cliente_pasta} não foi encontrada!")
        return
    
    relatorios = [f for f in os.listdir(cliente_pasta) if f.endswith('.pdf') or f.endswith('.xlsx') or f.endswith('.txt')]
    
    if not relatorios:
        print("Nenhum relatório encontrado na pasta do cliente.")
        return
    
    print("Relatórios encontrados:")
    for i, relatorio in enumerate(relatorios, 1):
        print(f"{i} - {relatorio}")
    
    escolha = input("Digite o número do relatório que deseja visualizar (ou 0 para cancelar): ")
    
    if escolha == '0':
        print("Operação cancelada.")
        return
    
    try:
        escolha = int(escolha)
        if 1 <= escolha <= len(relatorios):
            relatorio_escolhido = relatorios[escolha - 1]
            caminho_relatorio = os.path.join(cliente_pasta, relatorio_escolhido)
            
            if relatorio_escolhido.endswith('.txt'):
                with open(caminho_relatorio, 'r') as file:
                    print("\nConteúdo do relatório:")
                    print(file.read())
            elif relatorio_escolhido.endswith('.pdf'):
                print(f"O relatório PDF {relatorio_escolhido} foi selecionado.")
            elif relatorio_escolhido.endswith('.xlsx'):
                df = pd.read_excel(caminho_relatorio)
                print(f"\nConteúdo do relatório Excel {relatorio_escolhido}:")
                print(df.head())
        else:
            print("Opção inválida. Tente novamente.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")
