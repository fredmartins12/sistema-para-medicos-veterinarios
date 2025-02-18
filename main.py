import os
from analise_grafica import analisar_etapas
from bem_vindo import boas_vindas, buscar_cliente, criar_cliente
from diagnostico_gestacional import diagnostico_gestacional
from buscar_relatorios import buscar_relatorios
from meu_caixa import meu_caixa
from realizacao_iatf import realizar_iatf

def menu():
    print("\nEscolha uma opção:")
    print("1 - Diagnóstico Gestacional")
    print("2 - Realizar IATF")
    print("3 - Buscar Relatórios")
    print("4 - Meu Caixa")
    print("5 - Analisar Etapas (Gráficos)")
    print("6 - Sair")
    return input("Opção: ").strip()

def main():
    boas_vindas()  # Chama a função de boas-vindas
    cliente_encontrado, cliente_pasta = buscar_cliente()  # Busca o cliente e pasta

    if not cliente_encontrado:  # Caso o cliente não seja encontrado, pergunta se deseja criar um novo
        criar_novo_cliente = input("O cliente não foi encontrado. Criar novo? (sim/não): ").strip().lower()
        if criar_novo_cliente == 'sim':
            _, cliente_pasta = criar_cliente()  # Cria o novo cliente
        else:
            print("Operação cancelada. Encerrando o programa.")
            return

    # Garante a criação da estrutura básica de pastas
    pastas_necessarias = ['IATF', 'Diagnosticos', 'Financeiro']
    for pasta in pastas_necessarias:
        caminho = os.path.join(cliente_pasta, pasta)
        os.makedirs(caminho, exist_ok=True)

    while True:
        opcao = menu()  # Exibe o menu e captura a opção do usuário
        
        if opcao == '1':  # Chamando a função de diagnóstico gestacional
            diagnostico_gestacional(cliente_pasta)
        elif opcao == '2':  # Chamando a função de realizar IATF
            realizar_iatf(cliente_pasta)
        elif opcao == '3':  # Chamando a função de buscar relatórios
            buscar_relatorios(cliente_pasta)
        elif opcao == '4':  # Chamando a função de meu caixa
            meu_caixa(cliente_pasta)
        elif opcao == '5':  # Chamando a função para analisar etapas (gráficos)
            analisar_etapas(cliente_pasta)
        elif opcao == '6':  # Encerra o programa
            print("Encerrando o programa. Até mais!")
            break
        else:
            print("Opção inválida, tente novamente.")  # Caso a opção seja inválida

if __name__ == "__main__":
    main()
