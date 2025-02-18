import os
import datetime
import pandas as pd
from pandas.io.excel import ExcelWriter

# Períodos padrão para cálculo (base para bovinos; para equinos/ovinos, ajustar se necessário)
gestation_times = {
    'bovinos': 280,
    'equinos': 340,
    'ovinos': 150
}

def realizar_iatf(cliente_pasta):
    current_folder = None

    def create_folder():
        nonlocal current_folder
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        iatf_folder = f"IATF_{timestamp}"
        current_folder = os.path.join(cliente_pasta, iatf_folder)
        os.makedirs(current_folder, exist_ok=True)
        return current_folder

    def choose_or_create_process():
        nonlocal current_folder
        # Procura por processos IATF já existentes na pasta do cliente
        existing = [d for d in os.listdir(cliente_pasta)
                    if d.startswith("IATF_") and os.path.isdir(os.path.join(cliente_pasta, d))]
        if existing:
            print("\nProcessos IATF existentes:")
            for i, folder in enumerate(existing):
                print(f"{i+1} - {folder}")
            print("0 - Iniciar novo processo")
            choice = input("Escolha um processo existente para retomar ou 0 para criar um novo: ")
            if choice == "0":
                create_folder()
            else:
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(existing):
                        current_folder = os.path.join(cliente_pasta, existing[idx])
                        print(f"Processo '{existing[idx]}' selecionado.")
                    else:
                        print("Escolha inválida. Iniciando novo processo.")
                        create_folder()
                except ValueError:
                    print("Entrada inválida. Iniciando novo processo.")
                    create_folder()
        else:
            create_folder()

    # Ao iniciar o IATF, escolhe ou cria o processo
    choose_or_create_process()

    def validate_input(value, valid_options, field_name):
        while value.lower() not in valid_options:
            print(f"Valor inválido para {field_name}! Opções válidas: {', '.join(valid_options)}")
            value = input(f"{field_name}: ").lower()
        return value.capitalize()

    def check_previous_etapa(etapa):
        if etapa == 1:
            return True
        elif etapa == 2:
            return os.path.exists(os.path.join(current_folder, "etapa_1.xlsx"))
        elif etapa == 3:
            return os.path.exists(os.path.join(current_folder, "etapa_2.xlsx"))
        elif etapa == 4:
            return os.path.exists(os.path.join(current_folder, "etapa_3.xlsx"))
        return False

    def format_excel_report(df, filename, sheet_name):
        with ExcelWriter(filename, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            
            # Formatação profissional do cabeçalho
            header_format = workbook.add_format({
                'bold': True,
                'border': 1,
                'bg_color': '#002060',
                'font_color': 'white'
            })
            
            for col_num, value in enumerate(df.columns):
                worksheet.write(0, col_num, value, header_format)
                col_width = max(len(str(value)) * 1.3, 12)
                worksheet.set_column(col_num, col_num, col_width)
                
            if 'Resultado' in df.columns:
                worksheet.conditional_format('D2:D1000', {
                    'type': 'cell',
                    'criteria': 'equal to',
                    'value': '"Positivo"',
                    'format': workbook.add_format({'bg_color': '#C6EFCE'})
                })
            
            worksheet.autofilter(0, 0, 0, len(df.columns)-1)
            worksheet.freeze_panes(1, 0)
            
            if sheet_name == 'Acompanhamento':
                chart = workbook.add_chart({'type': 'column'})
                chart.add_series({
                    'categories': f'={sheet_name}!$D$2:$D${len(df)+1}',
                    'values':     f'={sheet_name}!$E$2:$E${len(df)+1}',
                })
                worksheet.insert_chart('H2', chart)

    def etapa_1():
        print("\n\033[1m=== ETAPA 1 - CADASTRO DE ANIMAIS ===\033[0m")
        
        # Solicita o tipo de animal apenas uma vez para o processo
        animal_type_global = validate_input(
            input("Tipo de Animal para este processo (Bovinos/Equinos/Ovinos): ").lower(),
            ['bovinos', 'equinos', 'ovinos'],
            'Tipo Animal'
        )
        
        records = []
        while True:
            print("\n\033[94mNovo Animal\033[0m")
            identificacao = input("Identificação única: ")
            if identificacao.lower() == 'sair':
                break
            
            status = validate_input(
                input("Status (Solteira/Gestante/Parida): ").lower(),
                ['solteira', 'gestante', 'parida'],
                'Status'
            )
            
            ciclo = validate_input(
                input("Ciclo Estral (Ciclando/Não ciclando): ").lower(),
                ['ciclando', 'não ciclando'],
                'Ciclo Estral'
            )
            
            records.append({
                'ID Animal': identificacao,
                'Tipo': animal_type_global,
                'Status': status,
                'Ciclo Estral': ciclo,
                'Data Cadastro': datetime.datetime.now().strftime("%d/%m/%Y"),
                'Responsável': os.getlogin()
            })
            
            if input("\nAdicionar outro animal? (S/N): ").lower() != 's':
                break
        
        df = pd.DataFrame(records)
        filename = os.path.join(current_folder, "etapa_1.xlsx")
        format_excel_report(df, filename, 'Cadastro')
        print(f"\n\033[92mRelatório gerado: {filename}\033[0m")

    def etapa_2():
        if not check_previous_etapa(2):
            print("Execute a Etapa 1 primeiro!")
            return
            
        print("\n\033[1m=== ETAPA 2 - SINCRONIZAÇÃO ===\033[0m")
        # Garante que a coluna "ID Animal" seja lida como string
        df = pd.read_excel(os.path.join(current_folder, "etapa_1.xlsx"), dtype={'ID Animal': str})
        
        # Solicita a data de início apenas uma vez
        data_inicio = validate_date("Data de início (DD/MM/AAAA): ")
        protocolos = []
        while True:
            animal_id = input("Digite a identificação do animal para sincronização (ou 'sair' para encerrar): ")
            if animal_id.lower() == 'sair':
                break
            if animal_id not in df['ID Animal'].values:
                print("Animal não encontrado no cadastro.")
                continue
            protocolo = input("Protocolo utilizado: ")
            dose = float(input("Dose hormonal aplicada (ml): "))
            reacao = validate_input(
                input("Reação (Excelente/Boa/Regular/Fraca): ").lower(),
                ['excelente', 'boa', 'regular', 'fraca'],
                'Reação'
            )
            protocolos.append({
                'ID Animal': animal_id,
                'Data Início': data_inicio.strftime("%d/%m/%Y"),
                'Protocolo': protocolo,
                'Dose Hormonal (ml)': dose,
                'Reação': reacao
            })
        
        if protocolos:
            df_protocol = pd.DataFrame(protocolos)
            filename = os.path.join(current_folder, "etapa_2.xlsx")
            format_excel_report(df_protocol, filename, 'Sincronização')
            print(f"\n\033[92mRelatório gerado: {filename}\033[0m")
        else:
            print("Nenhuma sincronização realizada.")

    def etapa_3():
        if not check_previous_etapa(3):
            print("Execute a Etapa 2 primeiro!")
            return
            
        print("\n\033[1m=== ETAPA 3 - INSEMINAÇÃO ===\033[0m")
        # Garante a leitura da coluna "ID Animal" como string no arquivo da etapa 2
        df = pd.read_excel(os.path.join(current_folder, "etapa_2.xlsx"), dtype={'ID Animal': str})
        
        # Solicita o nome do técnico/veterinário e o método apenas uma vez
        tecnico = input("Nome do técnico/veterinário responsável: ")
        metodo = validate_input(
            input("Método (Convencional/Sexado): ").lower(),
            ['convencional', 'sexado'],
            'Método'
        )
        
        inseminacoes = []
        while True:
            animal_id = input("Digite a identificação do animal para inseminação (ou 'sair' para encerrar): ")
            if animal_id.lower() == 'sair':
                break
            if animal_id not in df['ID Animal'].values:
                print("Animal não encontrado na etapa de Sincronização.")
                continue

            data_inseminacao = validate_date("Data da inseminação (DD/MM/AAAA): ")
            codigo_semen = input("Código do material genético: ")
            observacoes = input("Observações técnicas: ")
            inseminacoes.append({
                'ID Animal': animal_id,
                'Data Inseminação': data_inseminacao.strftime("%d/%m/%Y"),
                'Técnico': tecnico,
                'Código Semen': codigo_semen,
                'Método': metodo,
                'Observações': observacoes
            })
        
        if inseminacoes:
            df_ins = pd.DataFrame(inseminacoes)
            filename = os.path.join(current_folder, "etapa_3.xlsx")
            format_excel_report(df_ins, filename, 'Inseminação')
            print(f"\n\033[92mRelatório gerado: {filename}\033[0m")
        else:
            print("Nenhuma inseminação registrada.")

    def etapa_4():
        if not check_previous_etapa(4):
            print("Execute a Etapa 3 primeiro!")
            return
            
        print("\n\033[1m=== ETAPA 4 - ACOMPANHAMENTO ===\033[0m")
        # Garante a leitura da coluna "ID Animal" como string para ambos os arquivos
        df_ins = pd.read_excel(os.path.join(current_folder, "etapa_3.xlsx"), dtype={'ID Animal': str})
        df_cad = pd.read_excel(os.path.join(current_folder, "etapa_1.xlsx"), dtype={'ID Animal': str})
        
        acompanhamentos = []
        # Itera sobre todos os animais que passaram pela inseminação
        for idx, row in df_ins.iterrows():
            animal_id = row['ID Animal']
            print(f"\n\033[94mAnimal {animal_id}\033[0m")
            data_diagnostico = validate_date("Data do diagnóstico (DD/MM/AAAA): ")
            resultado = validate_input(
                input("Resultado (Positivo/Negativo): ").lower(),
                ['positivo', 'negativo'],
                'Resultado'
            )
            veterinario = input("Veterinário responsável: ")
            # Obtém os dados do cadastro do animal
            cad_info = df_cad[df_cad['ID Animal'] == animal_id].iloc[0]
            # Calcula a previsão de parto com base na data da inseminação e no período de gestação
            previsao_str = calcular_previsao_parto(row, cad_info)
            
            # Se o resultado for "Positivo", calcula automaticamente:
            # - Próximo IATF: 60 dias após o parto
            # - Data provável do desmame: 210 dias após o parto
            if resultado.lower() == "positivo":
                previsao_dt = datetime.datetime.strptime(previsao_str, "%d/%m/%Y")
                proximo_iatf_dt = previsao_dt + datetime.timedelta(days=60)
                data_desmame_dt = previsao_dt + datetime.timedelta(days=210)
                proximo_iatf = proximo_iatf_dt.strftime("%d/%m/%Y")
                data_desmame = data_desmame_dt.strftime("%d/%m/%Y")
            else:
                proximo_iatf = "N/A"
                data_desmame = "N/A"
            
            acompanhamentos.append({
                'ID Animal': animal_id,
                'Último Ciclo': cad_info['Data Cadastro'],
                'Data Diagnóstico': data_diagnostico.strftime("%d/%m/%Y"),
                'Resultado': resultado,
                'Veterinário': veterinario,
                'Previsão Parto': previsao_str,
                'Data Provável Desmame': data_desmame,
                'Próximo IATF': proximo_iatf
            })
        
        if acompanhamentos:
            df_acomp = pd.DataFrame(acompanhamentos)
            filename = os.path.join(current_folder, "etapa_4.xlsx")
            format_excel_report(df_acomp, filename, 'Acompanhamento')
            print(f"\n\033[92mRelatório gerado: {filename}\033[0m")
        else:
            print("Nenhum acompanhamento realizado.")

    def validate_date(prompt):
        while True:
            try:
                date_str = input(prompt)
                return datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
            except ValueError:
                print("Formato de data inválido! Use DD/MM/AAAA")

    def calcular_previsao_parto(row, cad_info):
        if 'Data Inseminação' in row:
            data_ins = row['Data Inseminação']
            if isinstance(data_ins, str):
                data_ins = datetime.datetime.strptime(data_ins, "%d/%m/%Y")
            gestacao = gestation_times[cad_info['Tipo'].lower()]
            return (data_ins + datetime.timedelta(days=gestacao)).strftime("%d/%m/%Y")
        return "N/A"

    while True:
        print("\n\033[1m=== MENU IATF ===")
        print("1. Cadastro de Animais")
        print("2. Sincronização")
        print("3. Inseminação")
        print("4. Acompanhamento")
        print("5. Sair\033[0m")
        
        choice = input("\nSelecione a etapa: ")
        if choice == '1':
            etapa_1()
        elif choice == '2':
            etapa_2()
        elif choice == '3':
            etapa_3()
        elif choice == '4':
            etapa_4()
        elif choice == '5':
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    # Substitua o caminho abaixo pelo diretório desejado para salvar os relatórios do cliente
    realizar_iatf(r"C:\Caminho\Para\Pasta\Do\Cliente")
