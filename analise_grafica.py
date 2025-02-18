import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Função principal para gerenciar todo o processo
def main():
    cliente_pasta = input("Digite o nome da pasta do cliente: ")
    analisar_etapas(cliente_pasta)

# Função para buscar processos existentes
def buscar_processos_existentes(cliente_pasta):
    existing = [d for d in os.listdir(cliente_pasta)
                if d.startswith("IATF_") and os.path.isdir(os.path.join(cliente_pasta, d))]
    
    if existing:
        print("\nProcessos IATF existentes:")
        for i, folder in enumerate(existing):
            print(f"{i+1} - {folder}")
        choice = input("Escolha um processo existente para retomar: ")
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(existing):
                current_folder = os.path.join(cliente_pasta, existing[idx])
                print(f"Processo '{existing[idx]}' selecionado.")
                return current_folder
            else:
                print("Escolha inválida. Iniciando novo processo.")
                return None
        except ValueError:
            print("Entrada inválida. Iniciando novo processo.")
            return None
    else:
        print("Nenhum processo IATF encontrado. Crie um novo primeiro.")
        return None

# Função principal de análise
def analisar_etapas(cliente_pasta):
    diretorio_atual = os.path.dirname(os.path.realpath(__file__))
    cliente_pasta = os.path.join(diretorio_atual, cliente_pasta)

    if not os.path.exists(cliente_pasta):
        os.makedirs(cliente_pasta)
        print(f"Pasta '{cliente_pasta}' criada.")

    current_folder = buscar_processos_existentes(cliente_pasta)
    
    if not current_folder:
        print("Encerrando o programa.")
        return
    
    etapas = ["etapa_1.xlsx", "etapa_2.xlsx", "etapa_3.xlsx", "etapa_4.xlsx"]
    etapas_presentes = []

    for etapa in etapas:
        etapa_path = os.path.join(current_folder, etapa)
        if os.path.exists(etapa_path):
            etapas_presentes.append(etapa)

    if not etapas_presentes:
        print("Nenhuma etapa encontrada. Encerrando.")
        return

    print(f"\nEtapas encontradas: {', '.join(etapas_presentes)}")
    
    graficos_path = os.path.join(current_folder, 'Graficos')
    os.makedirs(graficos_path, exist_ok=True)

    dados_combinados = pd.DataFrame()

    for etapa in etapas_presentes:
        etapa_nome = etapa.replace(".xlsx", "").replace("_", " ").capitalize()
        print(f"\nProcessando {etapa_nome}...")

        df = carregar_dados(os.path.join(current_folder, etapa))
        if df is not None:
            if 'Tipo' not in df.columns and etapa != "etapa_1.xlsx":
                df['Tipo'] = "Não informado"

            if dados_combinados.empty:
                dados_combinados = df
            else:
                dados_combinados = pd.merge(
                    dados_combinados, df, on="ID Animal", how="outer", suffixes=('', '_DROP')
                ).filter(regex='^(?!.*_DROP)')

            if etapa == "etapa_1.xlsx":
                analisar_etapa_1(df, graficos_path)
            elif etapa == "etapa_2.xlsx":
                analisar_etapa_2(df, graficos_path)
            elif etapa == "etapa_3.xlsx":
                analisar_etapa_3(df, graficos_path)
            elif etapa == "etapa_4.xlsx":
                analisar_etapa_4(df, graficos_path)

    if not dados_combinados.empty:
        gerar_relatorio_final(dados_combinados, current_folder)
        print("\nProcesso concluído com sucesso!")

# Funções de análise específicas por etapa
def analisar_etapa_1(df, graficos_path):
    gerar_grafico_pizza(df, 'Status', 'Distribuição de Status', graficos_path)
    gerar_grafico_barras(df, 'Ciclo Estral', 'Distribuição de Ciclos Estrais', graficos_path)

def analisar_etapa_2(df, graficos_path):
    if 'Dose Hormonal (ml)' in df.columns:
        plt.figure(figsize=(10,6))
        sns.histplot(df['Dose Hormonal (ml)'], bins=5, kde=True, color='skyblue')
        plt.title('Distribuição de Doses Hormonais')
        plt.savefig(os.path.join(graficos_path, 'doses_hormonais.png'))
        plt.close()

def analisar_etapa_3(df, graficos_path):
    if 'Método' in df.columns:
        contagem = df['Método'].value_counts()
        plt.figure(figsize=(10,6))
        sns.barplot(x=contagem.index, y=contagem.values, palette='viridis')
        plt.title('Métodos de Inseminação Utilizados')
        plt.xticks(rotation=45)
        plt.savefig(os.path.join(graficos_path, 'metodos_inseminacao.png'))
        plt.close()

def analisar_etapa_4(df, graficos_path):
    if 'Resultado' in df.columns:
        plt.figure(figsize=(8,8))
        df['Resultado'].value_counts().plot.pie(autopct='%1.1f%%', colors=['#66b3ff','#99ff99','#ffcc99'])
        plt.title('Resultados de Diagnóstico')
        plt.ylabel('')
        plt.savefig(os.path.join(graficos_path, 'resultados_diagnostico.png'))
        plt.close()

# Funções auxiliares
def carregar_dados(path):
    try:
        return pd.read_excel(path)
    except Exception as e:
        print(f"Erro ao carregar {path}: {str(e)}")
        return None

def gerar_relatorio_final(df, pasta):
    caminho = os.path.join(pasta, 'Relatorio_Consolidado_IATF.xlsx')
    df.to_excel(caminho, index=False)
    print(f"\nRelatório consolidado salvo em: {caminho}")

def gerar_grafico_pizza(df, coluna, titulo, pasta):
    if coluna in df.columns:
        contagem = df[coluna].value_counts()
        plt.figure(figsize=(8,8))
        plt.pie(contagem, labels=contagem.index, autopct='%1.1f%%', startangle=90)
        plt.title(titulo)
        plt.savefig(os.path.join(pasta, f'{coluna}_pizza.png'))
        plt.close()

def gerar_grafico_barras(df, coluna, titulo, pasta):
    if coluna in df.columns:
        contagem = df[coluna].value_counts()
        plt.figure(figsize=(10,6))
        sns.barplot(x=contagem.index, y=contagem.values, palette='coolwarm')
        plt.title(titulo)
        plt.xticks(rotation=45)
        plt.savefig(os.path.join(pasta, f'{coluna}_barras.png'))
        plt.close()

if __name__ == "__main__":
    main()
