# 🚀 Sistema Flash Reports v6.6

![Version](https://img.shields.io/badge/version-v6.6-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![Telegram Bot](https://img.shields.io/badge/bot-Telegram-blue)
![Status](https://img.shields.io/badge/status-ativo-success)

Sistema automatizado de geração de relatórios de O.S. via Telegram, desenvolvido para padronizar atendimentos técnicos, reduzir erros e aumentar a produtividade da equipe de campo.

---

## 🎯 Objetivo

* ⚡ Reduzir tempo de preenchimento
* 📋 Padronizar relatórios técnicos
* ❌ Diminuir erros humanos
* 📡 Melhorar comunicação interna
* 📊 Organizar o fluxo operacional

---

## 🧠 Remasterização v6.6

A versão v6.6 é uma evolução direta da v6.5, com foco em:

✔ Fluxos mais inteligentes
✔ Padronização de equipamentos
✔ Interface mais limpa
✔ Correção de inconsistências
✔ Sincronização real do sistema

---

## ⚙️ Funcionalidades

### 📋 Módulos

* 🔧 Assistências
* 📦 Retirada
* 🏢 Estoque
* 🚫 Cliente ausente
* ⏸️ O.S. paralisada
* 📋 Pendências (via comando ou paralisada)

---

## 📡 Assistências

* Modelos completos (rádio, fibra, segundo ponto, etc.)
* Campos inteligentes e condicionais
* Sugestões de respostas
* Relatório final padronizado

---

## 📦 Retirada (v6.6)

Novo fluxo guiado:

* Pergunta se há roteador
* Se sim → lista modelos cadastrados
* Pergunta se há ONU
* Se sim → lista modelos cadastrados
* Pergunta se há patchcord
* Observação com botão Sim/Não

Resultado:

```text
1x Roteador X
1x ONU Y
1x Patchcord
```

---

## 🏢 Estoque (v6.6)

Fluxo padronizado:

* Tipo:

  * Retirada (Troca)
  * Retirada (Cancelamento)

* Equipamentos:

  * Roteador (se houver)
  * ONU (se houver)
  * Patchcord

* Observação opcional

✔ Mesmo padrão da retirada
✔ Mais controle de entrada

---

## 🔁 Integração Retirada → Estoque

Após finalizar retirada:

```text
Deseja gerar entrada no estoque?
```

Se SIM:

* Dados são reaproveitados automaticamente
* Fluxo continua no estoque

---

## 📦 Sistema de equipamentos

Agora padronizado:

* Seleção via botão
* Evita digitação errada
* Usa dados do `/config`

---

## 🧾 Relatórios

* Estrutura formal automática
* Organização por seção
* Padronização completa
* Envio direto ao grupo

Inclui:

```text
Início
Fim automático
Tempo gasto
Técnicos
Equipamentos
```

---

## ⏱️ Tempo automático

* Técnico informa apenas início
* Final automático
* Tempo calculado

---

## 📋 Pendências

* Registro automático de:

  * O.S. paralisada
  * Cliente ausente

### Comandos:

```bash
/pendencias
/baixar_pendencia 123456
```

---

## ⚙️ /config (corrigido v6.6)

Agora sincronizado corretamente entre usuários.

### Gerencia:

* 👨‍🔧 Técnicos
* 📡 Roteadores
* 🧱 ONU
* 📍 Locais
* 🔌 Materiais
* 🔋 Energia
* 🛠️ Textos rápidos
* 🏢 Estoques

---

### Correção importante

✔ Agora todos usuários veem as mesmas alterações
✔ Não há mais inconsistência entre contas

---

## 🧹 Melhorias da v6.6

* Removido botão duplicado de pendências do `/start`
* Retirada mais inteligente
* Estoque mais padronizado
* Observações com controle Sim/Não
* Sincronização do config corrigida
* Fluxo mais limpo

---

## 📂 Estrutura

```
core/
shared/
models/
data/

main.py
config.py
requirements.txt
README.md
```

---

## 🔐 Variáveis (Railway)

```
BOT_TOKEN=SEU_TOKEN
CHAT_ID=ID_DO_GRUPO
CONFIG_PASSWORD=SENHA
```

---

## 🚀 Deploy

```bash
git add .
git commit -m "feat: v6.6"
git push origin main
```

---

## 🧪 Comandos

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

## 🔮 Próximos passos

* Dashboard web
* Estatísticas de atendimento
* Integração com MK/Auth
* Histórico por O.S.
* Relatórios automáticos

---

## 👨‍💻 Desenvolvedor

Cauã Henrique de Oliveira

---

## 🧠 Filosofia

```
Menos digitação,
menos erro,
mais produtividade.
```
