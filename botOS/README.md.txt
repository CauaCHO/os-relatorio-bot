# Bot de Relatórios Técnicos

Bot em Python para geração de relatórios técnicos via Telegram, com fluxo guiado, padronização de texto e estrutura modular preparada para expansão.

---

## 📌 Visão geral

O sistema foi desenvolvido para centralizar a criação de relatórios internos da equipe técnica, reduzindo erros de preenchimento e padronizando a comunicação.

Atualmente o bot possui **3 módulos principais**:

- **Relatório de O.S.**
- **Retirada de Equipamentos**
- **Cliente Ausente / O.S. Paralisada**

Além disso, o projeto já está organizado em módulos/pastas, facilitando manutenção e futuras expansões.

---

## 🚀 Funcionalidades

### ✅ Relatório de O.S.
Fluxo completo para relatórios técnicos de atendimento, com campos como:

- número da O.S.
- tipo de atendimento
- técnicos
- problema relatado
- solução
- observações
- sinal da fibra / CTO
- canais 2.4G e 5G
- materiais utilizados
- materiais retirados

### ✅ Retirada de Equipamentos
Módulo separado para retirada de equipamentos, com suporte para:

- tipo de retirada
- roteador
- ONU
- patchcord
- outro equipamento
- destino
- recebido por
- cidade

### ✅ Cliente Ausente / O.S. Paralisada
Módulo específico para ocorrências como:

- cliente ausente
- O.S. paralisada
- outro motivo

### ✅ Processamento de texto local
O bot não depende de IA paga.

O texto passa por um modelo de 3 camadas:

1. **Entrada livre do técnico**
2. **Lapidação local**
3. **Refinamento com LanguageTool**  
   Se o LanguageTool não estiver disponível, o sistema usa fallback local automaticamente.

### ✅ Integração entre módulos
Se no relatório de O.S. forem informados **materiais retirados**, o bot pergunta automaticamente se deseja gerar também o **relatório de retirada de equipamentos**.

### ✅ Confirmação antes do envio
Antes de enviar o relatório, o usuário pode:

- enviar
- editar etapa específica
- cancelar

### ✅ Rastreabilidade
Os relatórios enviados ao grupo incluem a informação de **quem preencheu**.

### ✅ Histórico local
Os relatórios são salvos localmente em JSON.

---

## 🧱 Estrutura do projeto

```bash
bot-relatorios/
├── main.py
├── config.py
├── requirements.txt
├── .gitignore
│
├── core/
│   ├── __init__.py
│   ├── helpers.py
│   ├── storage.py
│   ├── text_processor.py
│   └── error_handler.py
│
├── shared/
│   ├── __init__.py
│   ├── keyboards.py
│   └── commands.py
│
├── modules/
│   ├── __init__.py
│   ├── os_report/
│   │   ├── __init__.py
│   │   ├── handlers.py
│   │   └── report.py
│   │
│   ├── material_delivery/
│   │   ├── __init__.py
│   │   ├── handlers.py
│   │   └── report.py
│   │
│   └── absent_client/
│       ├── __init__.py
│       ├── handlers.py
│       └── report.py
│
└── data/
    ├── historico_relatorios.json
    └── usuarios_bot.json