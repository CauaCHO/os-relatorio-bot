# 🚀 Sistema Flash Reports v6.5 Ultra

![Version](https://img.shields.io/badge/version-v6.5-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![Telegram Bot](https://img.shields.io/badge/bot-Telegram-blue)
![Status](https://img.shields.io/badge/status-ativo-success)

Sistema automatizado de geração de relatórios de O.S. (Ordem de Serviço) via Telegram, desenvolvido para padronizar atendimentos técnicos, reduzir erros e aumentar a produtividade da equipe de campo.

---

## 🎯 Objetivo

O Flash Reports foi criado para:

* ⚡ Reduzir o tempo de preenchimento de relatórios
* 📋 Padronizar informações técnicas
* ❌ Diminuir erros humanos
* 📡 Facilitar comunicação entre técnico e empresa
* 📊 Melhorar o controle operacional

---

## 🧠 Remasterização v6.5 Ultra

A versão v6.5 foi completamente reformulada com foco em:

✔ Usabilidade para técnicos
✔ Automação inteligente
✔ Redução de digitação manual
✔ Sistema dinâmico via `/config`
✔ Escalabilidade futura

---

## ⚙️ Funcionalidades

### 📋 Módulos principais

* 🔧 Assistências (todos os modelos)
* 📦 Retirada de equipamentos (cliente)
* 🏢 Entrada de equipamentos no estoque
* 🚫 Cliente ausente
* ⏸️ O.S. paralisada
* 📋 Pendências (listar e baixar)

---

### 🧠 Inteligência do sistema

* Botões rápidos para respostas comuns
* Sugestões automáticas de texto técnico
* Campos condicionais inteligentes
* Normalização automática:

  * 📉 Sinal → dBm
  * 🚀 Velocidade → Mbps
* ⏱️ Cálculo automático do tempo de serviço

---

## 📡 Segundo Ponto (corrigido)

Agora permite selecionar:

* 📡 Roteador
* 💻 PC
* 📺 TV
* 🎥 Câmera
* ➕ Outro

Com perguntas inteligentes baseadas na escolha.

---

## 📦 Sistema de materiais

Fluxo simplificado:

1. Seleciona material
2. Informa quantidade
3. Sistema organiza automaticamente

Exemplo:

```
1x Roteador
2x Conector APC
8x Abraçadeira
```

---

## 🧾 Relatórios

* Estrutura formal automática
* Organização por seções
* Padronização completa
* Envio direto para grupo Telegram

Exemplo:

```
👤 Preenchido por: @usuario

O.S: 123456

Iniciada: 15:30  
Finalizada: 16:45  
Tempo gasto: 1 h 15 min
```

---

## ⏱️ Controle de tempo

* Técnico informa apenas o horário de início
* Horário final automático
* Tempo total calculado automaticamente

---

## 📋 Pendências

Registro automático de:

* O.S. paralisada
* Cliente ausente

Comandos:

```
/pendencias
/baixar_pendencia 123456
```

---

## 🔁 Integração Retirada → Estoque

Após finalizar retirada:

```
Deseja gerar entrada no estoque?
[Sim] [Não]
```

Se escolher SIM:

* Dados são reaproveitados
* Fluxo continua automaticamente

---

## ⚙️ /config (Painel Administrativo)

Sistema dinâmico diretamente pelo Telegram.

### Permite gerenciar:

* 👨‍🔧 Técnicos
* 📡 Roteadores
* 🧱 ONU/ONT
* 📍 Locais
* 🔌 Materiais
* 🔋 Energia
* 🛠️ Textos rápidos
* 🏢 Estoques

---

### Ações disponíveis

* ➕ Adicionar
* 📋 Listar
* ➖ Remover

---

### Segurança

* Validação por username
* Validação por ID
* Senha via variável de ambiente

---

## 📂 Estrutura do Projeto

```
.
├── core/
│   ├── engine.py
│   ├── error_handler.py
│
├── shared/
│   ├── storage.py
│   ├── utils.py
│   ├── keyboards.py
│
├── models/
│   └── assistencias.json
│
├── data/
│   ├── config.json
│   ├── relatorios.json
│   ├── pendencias.json
│   ├── usuarios.json
│   ├── logs.json
│
├── config.py
├── main.py
├── requirements.txt
```

---

## 🔐 Variáveis de Ambiente (Railway)

Configure no Railway:

```
BOT_TOKEN=SEU_TOKEN
CHAT_ID=ID_DO_GRUPO
CONFIG_PASSWORD=SENHA_DO_CONFIG
```

---

## 🚀 Deploy

```
git add .
git commit -m "feat: v6.5 ultra"
git push origin main
```

---

## 🧪 Comandos disponíveis

```
/start
/assistencia
/retirada
/estoque
/ausente
/paralisada
/pendencias
/baixar_pendencia
/config
```

---

## 💡 Melhorias da v6.5

* Interface mais rápida
* Redução de digitação
* Botões inteligentes
* Sistema de materiais otimizado
* Configuração sem código
* Fluxo simplificado

---

## 🔮 Futuro do projeto

* Dashboard web
* Integração com MK/Auth
* Estatísticas de atendimento
* Histórico por O.S.
* Relatórios automáticos
* Integração com WhatsApp

---

## 👨‍💻 Desenvolvedor

Cauã Henrique de Oliveira
Sistema Flash Reports

---

## 🧠 Filosofia do projeto

```
Automatizar o máximo possível,
reduzir erros humanos,
e aumentar a produtividade do técnico
sem complicar o processo.
```
