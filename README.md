# IATF Control - Sistema de Gestão Zootécnica/Medicos veterinarios

![Livestock Management](https://img.icons8.com/color/96/000000/cow--v1.png) *Ícone ilustrativo*

## 🐄 Descrição do Projeto

Sistema profissional para gestão de Inseminação Artificial em Tempo Fixo (IATF) em rebanhos bovinos, equinos e ovinos. Desenvolvido para veterinários e produtores rurais, oferece controle completo do processo reprodutivo animal, desde o cadastro de clientes até o acompanhamento gestacional.

**Principais Funcionalidades:**
- 👥 Gestão de clientes e propriedades rurais
- 📋 Controle das 4 etapas do IATF (Cadastro, Sincronização, Inseminação, Acompanhamento)
- 📊 Geração automática de relatórios em Excel
- 💰 Módulo financeiro integrado
- 🗂️ Sistema de armazenamento organizado por cliente/data

## 🛠️ Funcionalidades Técnicas

| Módulo         | Tecnologias                          | Recursos Especiais                     |
|----------------|--------------------------------------|----------------------------------------|
| Cadastro       | Pandas, CSV                          | Validação de dados, Relatórios         |
| IATF           | XlsxWriter, Openpyxl                 | Planilhas formatadas, Cálculos automáticos |
| Financeiro     | Pandas, Datetime                     | Extrato PDF, Balanço financeiro        |
| Interface      | CLI puro                             | Menus intuitivos, Cores personalizadas |

## ⚙️ Instalação

1. **Pré-requisitos:**
   - Python 3.8+
   - Git

2. **Clonar repositório:**
   ```bash
   git clone https://github.com/seu-usuario/iatf-control.git
   cd iatf-control

   iatf-control/
3.**Estrutura do Projeto

├── clientes/              # Dados dos clientes
├── src/                   # Código-fonte
│   ├── main.py            # Ponto de entrada
│   ├── bem_vindo.py       # Módulo de boas-vindas
│   ├── realizacao_iatf.py # Lógica do IATF
│   ├── meu_caixa.py       # Gestão financeira
│   └── buscar_relatorios.py # Sistema de busca
├── requirements.txt       # Dependências
└── README.md              # Documentação
