# 🚀 Sistema Flash Reports

Bot em Python para geração automática de relatórios técnicos via Telegram, com fluxo guiado, padronização de texto e estrutura modular preparada para expansão.

---

# 📌 Visão Geral

O sistema foi desenvolvido para centralizar a criação de relatórios internos da equipe técnica, reduzindo erros de preenchimento e padronizando a comunicação.

Atualmente o bot possui múltiplos módulos operacionais, permitindo registrar diversos tipos de ocorrências técnicas do dia a dia.

---

# 📦 Módulos Disponíveis

- 🔧 Atendimento
- 📦 Retirada
- 🏢 Estoque
- 🚪 Ausente
- ⏸️ Paralisada
- 📋 Pendências

---

# 🚀 Funcionalidades

## ✅ Atendimento

Fluxo principal para relatórios técnicos de:

- Assistência
- Instalação
- Mudança de endereço

Inclui:

- número da O.S.
- horário inicial
- técnicos envolvidos
- problema relatado
- solução aplicada
- observações
- equipamentos via cabo
- equipamentos via Wi-Fi
- local da instalação
- segundo ponto
- IPTV/TVBOX
- sinal da fibra
- sinal da CTO
- danos no local
- orientação 2.4G / 5G
- teste de velocidade
- canais Wi-Fi
- organização
- assinatura do cliente
- materiais utilizados
- materiais retirados

---

## ✅ Retirada

Módulo reservado para retirada de equipamentos da residência do cliente.

Atualmente está em evolução e aparece no menu principal como módulo separado do Estoque.

---

## ✅ Estoque

Relatório para comprovar entrega de materiais/equipamentos no estoque.

Inclui:

- O.S.
- tipo da retirada
- roteador
- ONU
- patchcord
- outro equipamento
- destino
- recebido por
- cidade

---

## ✅ Ausente

Relatório para cliente ausente no local.

Exemplos:

- cliente não atendeu
- tentativa por ligação
- tentativa via agendamento
- aviso deixado no local

---

## ✅ Paralisada

Relatório para O.S. iniciada e interrompida.

Exemplos:

- falta de material
- reagendamento
- sem acesso
- cliente pediu retorno
- necessidade de retorno técnico

---

## ✅ Pendências

Lista automática de O.S. paralisadas ainda abertas.

Quando a mesma O.S. volta ao fluxo de Atendimento, o sistema informa que ela está pendente e pergunta se deseja remover da lista e continuar.

---

# 🧠 Processamento de Texto Local

O bot não depende de IA paga.

O sistema usa um fluxo híbrido de texto:

1. Entrada livre do técnico  
2. Padronização local  
3. Refinamento com LanguageTool  

Se o LanguageTool não estiver disponível, o sistema utiliza fallback local automaticamente.

---

# 🔄 Integração entre Módulos

Se no Atendimento forem informados materiais retirados, o bot pergunta automaticamente se deseja gerar também o relatório de Estoque, reaproveitando a mesma O.S.

---

# ✅ Revisão Antes do Envio

Antes de enviar o relatório ao grupo, o sistema **não envia automaticamente sem confirmação final**.

Primeiro ele apresenta a tela de revisão:

- ✅ Enviar
- ✏️ Editar etapa específica
- ❌ Cancelar

Ou seja:

- o relatório só é gerado e enviado ao grupo quando o usuário clicar em **Enviar**
- se o usuário quiser, ele pode voltar exatamente na etapa que deseja editar
- se cancelar, o relatório não é enviado

Esse fluxo evita erro humano e reduz risco de relatórios perdidos.

---

# 👤 Rastreabilidade

Todos os relatórios enviados ao grupo incluem a identificação de quem preencheu.

Exemplo:

```text
👤 Preenchido por: @usuario
