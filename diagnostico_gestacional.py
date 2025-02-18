import os
import pandas as pd
from datetime import datetime, timedelta

# Dicionário com o período de gestação para diferentes animais (em dias)
gestacao_dias = {
    'vaca': 283,
    'cavalo': 340,
    'ovelha': 152,
    'cabra': 150,
    'porca': 115
}

# Lista para armazenar os dados dos animais
relatorio = []

# Função para calcular a data de parição
def calcular_paricao(data_hoje, tempo_gestacao):
    return data_hoje + timedelta(days=tempo_gestacao)

# Função para verificar se já existe um relatório na pasta e gerar um novo nome
def obter_nome_arquivo(cliente_pasta):
    # Verifica se o arquivo já existe
    caminho_base = os.path.join(cliente_pasta, 'relatorio_gestacional')
    num = 1  # Número inicial para o arquivo

    while os.path.exists(f"{caminho_base}_{num}.xlsx"):  # Se o arquivo existe
        num += 1  # Incrementa o número do arquivo

    # Retorna o caminho final do arquivo
    return f"{caminho_base}_{num}.xlsx"

# Função para salvar o relatório em um arquivo Excel
def finalizar_relatorio(cliente_pasta):
    # Verifica se a pasta do cliente existe
    if not os.path.exists(cliente_pasta):
        print(f"ERRO: A pasta do cliente {cliente_pasta} não foi encontrada!")
        return

    # Verifica se há dados para salvar no relatório
    if not relatorio:
        print("ERRO: Nenhum dado para salvar no relatório!")
        return
    
    # Cria a pasta, caso ela não exista
    os.makedirs(cliente_pasta, exist_ok=True)
    
    # Cria um DataFrame com os dados do relatório
    df = pd.DataFrame(relatorio)
    
    # Obtém o nome do arquivo com base na existência de arquivos anteriores
    caminho_arquivo = obter_nome_arquivo(cliente_pasta)
    
    # Salva o DataFrame no arquivo Excel
    df.to_excel(caminho_arquivo, index=False)
    print(f"Relatório gerado com sucesso em: {caminho_arquivo}")

# Função para realizar o diagnóstico gestacional
def diagnostico_gestacional(cliente_pasta):
    print("Cadastro de Diagnóstico Gestacional")
    data_hoje = datetime.now().date()  # Data atual
    animal = input("Digite o tipo de animal: ").strip().lower()
    
    # Verifica se o tipo de animal está no dicionário, se não, solicita o tempo de gestação
    if animal not in gestacao_dias:
        dias_gestacao = int(input(f"Digite o número de dias de gestação para {animal}: "))
        gestacao_dias[animal] = dias_gestacao
    else:
        dias_gestacao = gestacao_dias[animal]
    
    while True:
        print("\nPara finalizar o registro, digite 'finalizar' na identificação do animal.")
        identificacao = input("Digite a identificação do animal: ").strip()
        
        if identificacao.lower() == 'finalizar':  # Finaliza o registro
            finalizar_relatorio(cliente_pasta)
            break
        
        condicao = input("Digite a condição do animal (ex: prenha, vazia, etc.): ").strip().lower()
        classificacao = input("Digite a classificação do animal (ex: leiteiro, corte, etc.): ").strip().lower()
        
        # Verifica se o animal está prenha e calcula a data de parição
        if condicao == 'prenha':
            tempo_gestacao = int(input("Digite o tempo de gestação atual em dias: "))
            data_paricao = calcular_paricao(data_hoje, dias_gestacao - tempo_gestacao)
            dias_restantes = (data_paricao - data_hoje).days
        else:
            tempo_gestacao = 'N/A'
            data_paricao = 'N/A'
            dias_restantes = 'N/A'
        
        # Adiciona as informações do animal no relatório
        relatorio.append({
            'Data do Diagnóstico': data_hoje,
            'Animal': animal,
            'Identificação': identificacao,
            'Condição': condicao,
            'Classificação': classificacao,
            'Tempo de Gestação Atual (dias)': tempo_gestacao,
            'Data Provável de Parição': data_paricao,
            'Dias Restantes para Parição': dias_restantes
        })
