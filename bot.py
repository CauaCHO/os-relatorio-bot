from datetime import datetime, timedelta
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================
# CONFIG
# =========================
TOKEN = "8662376885:AAHBROjjwfwcdHlj0yzIsOf6Zd2koz6VZM4"
CHAT_ID = "-1003622167197"

# Defina sua chave no sistema com:
# Windows PowerShell:
# setx OPENAI_API_KEY "sua_chave_aqui"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

# =========================
# OPENAI OPCIONAL
# =========================
client = None
if OPENAI_API_KEY:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception:
        client = None

# =========================
# ESTADO
# =========================
usuarios = {}

TIPOS = [
    ["Assistência", "Instalação"],
    ["Mudança de endereço", "Mudança de plano"],
    ["Mudança de cômodo", "Segundo ponto"],
    ["Link Loss", "Troca de plano"],
]

SIM_NAO = [["Sim", "Não"]]

TECNICOS = [
    ["Cauã Henrique", "Jamildo Ferreira"],
    ["Erick", "Valdisney"],
    ["Wellington Arouca", "Wesley Texeira"],
]

ENERGIA = [
    ["T", "Filtro de linha"],
    ["Tomada individual", "Tomada dupla"],
    ["Adaptador T", "Outro"],
]

PROBLEMAS_PADRAO = [
    ["Assistência", "Link Loss"],
    ["Mudança de plano", "Mudança de cômodo"],
    ["Segundo ponto", "Troca de plano"],
    ["Instabilidade", "Sem conexão"],
    ["Outro"],
]

# =========================
# REGRAS POR TIPO
# =========================
TIPOS_COM_PROBLEMA = {
    "Assistência",
    "Mudança de plano",
    "Mudança de cômodo",
    "Segundo ponto",
    "Link Loss",
    "Troca de plano",
}

TIPOS_COM_SOLUCAO = {
    "Assistência",
    "Mudança de plano",
    "Mudança de cômodo",
    "Segundo ponto",
    "Link Loss",
    "Troca de plano",
}

TIPOS_COM_FIXACAO = {
    "Instalação",
    "Mudança de endereço",
}

TIPOS_COM_CTO = {
    "Instalação",
    "Mudança de endereço",
}

TIPOS_COM_POS_VENDA = {
    "Instalação",
    "Mudança de endereço",
}

# =========================
# IA
# =========================
def corrigir_texto_solucao(texto_bruto: str) -> str:
    if not client:
        return texto_bruto

    try:
        resposta = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um assistente técnico de telecom. "
                        "Reescreva o texto em português formal, claro e profissional, "
                        "no padrão de relatório técnico. "
                        "Não invente fatos. Apenas corrija, organize e melhore a escrita."
                    ),
                },
                {"role": "user", "content": texto_bruto},
            ],
        )
        return resposta.choices[0].message.content.strip()
    except Exception:
        return texto_bruto

# =========================
# AUXILIARES
# =========================
def precisa_problema(tipo: str) -> bool:
    return tipo in TIPOS_COM_PROBLEMA

def precisa_solucao(tipo: str) -> bool:
    return tipo in TIPOS_COM_SOLUCAO

def precisa_fixacao(tipo: str) -> bool:
    return tipo in TIPOS_COM_FIXACAO

def precisa_cto(tipo: str) -> bool:
    return tipo in TIPOS_COM_CTO

def precisa_pos_venda(tipo: str) -> bool:
    return tipo in TIPOS_COM_POS_VENDA

def limpar_dbm(valor: str) -> str:
    return valor.replace("dBm", "").replace("dB", "").strip()

def escapar_html(texto: str) -> str:
    if texto is None:
        return ""
    return (
        str(texto)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

def parse_hora(hora_str: str):
    try:
        return datetime.strptime(hora_str.strip(), "%H:%M")
    except Exception:
        return None

def calcular_tempo_gasto(inicio: str, fim: str) -> str:
    hora_inicio = parse_hora(inicio)
    hora_fim = parse_hora(fim)

    if not hora_inicio or not hora_fim:
        return "Não informado"

    if hora_fim < hora_inicio:
        hora_fim += timedelta(days=1)

    diferenca = hora_fim - hora_inicio
    total_minutos = int(diferenca.total_seconds() // 60)
    horas = total_minutos // 60
    minutos = total_minutos % 60

    if horas > 0 and minutos > 0:
        return f"{horas} h {minutos} min"
    if horas > 0:
        return f"{horas} h"
    return f"{minutos} min"

def montar_relatorio(dados: dict) -> str:
    final = datetime.now().strftime("%H:%M")
    tempo_gasto = calcular_tempo_gasto(dados.get("inicio", ""), final)
    tipo = escapar_html(dados.get("tipo", "").upper())

    linhas = [
        f"<b>{tipo}</b>",
        "",
        f"<b>O.S:</b> {escapar_html(dados.get('os', ''))}",
        "",
        f"<b>Iniciada:</b> {escapar_html(dados.get('inicio', ''))}",
        f"<b>Finalizada:</b> {escapar_html(final)}",
        f"<b>Tempo gasto:</b> {escapar_html(tempo_gasto)}",
        "",
        f"<b>Técnico externo:</b> {escapar_html(dados.get('tec_ext', ''))}",
        f"<b>Técnico interno:</b> {escapar_html(dados.get('tec_int', ''))}",
        "",
    ]

    if precisa_problema(dados.get("tipo", "")):
        linhas += [
            "<b>1.13 - O problema relatado é?:</b>",
            escapar_html(dados.get("problema", "")),
            "",
        ]

    if precisa_solucao(dados.get("tipo", "")):
        linhas += [
            "<b>1.13 - Para solucionar o problema foi feito:</b>",
            escapar_html(dados.get("solucao", "")),
            "",
        ]

    linhas += [
        "<b>Informações em fotos:</b>",
        "1.1 - Fotos dos equipamentos conectados via cabo de rede.",
        "1.1.1 - Fotos dos equipamentos conectados via Wi-fi.",
        "1.2 - Local da instalação dos equipamentos (foto de perto e de longe, mostrando todo o ambiente).",
        "1.3 - Mapeamento de todo o local pelo WiFiman.",
        "1.4 - Foto de dispositivos diversos (IPTV, TVBOX, DVR...).",
        "1.5 - Medição de sinal da Fibra.",
        "1.8 - Realização de teste de velocidade.",
        "1.9 - Verificação de melhor canal (Wifi Analyser) rede 2.4Ghz e 5.8Ghz.",
    ]

    if precisa_fixacao(dados.get("tipo", "")):
        linhas.append("1.11 - Configurações do roteador dentro do nosso padrão (Lan, Wan, Gateway, Dhcp, DNS, IPv6 e Acesso Remoto).")
    else:
        linhas.append("1.10 - Configurações do roteador dentro do nosso padrão (Lan, Wan, Gateway, Dhcp, DNS, IPv6 e Acesso Remoto).")

    linhas += [
        "",
        "<b>Informações Descritas:</b>",
        "",
        "<b>Observações Relevantes:</b>",
        escapar_html(dados.get("observacoes", "") or "Nenhuma."),
        "",
        "<b>1.1 - Quais equipamentos o cliente tem conectado no cabo:</b>",
        escapar_html(dados.get("cabo", "")),
        "",
        "<b>1.1.1 - Quais equipamentos o cliente tem conectado via Wi-fi?:</b>",
        escapar_html(dados.get("wifi", "")),
        "",
        "<b>1.2 - Qual o local da instalação dos equipamentos?:</b>",
        escapar_html(dados.get("local", "")),
        "",
        "<b>1.3 - Cliente necessita de um segundo ponto?:</b>",
        escapar_html(dados.get("segundo_ponto", "")),
        "",
        "<b>1.4 - Cliente possui IPTV/TVBOX?:</b>",
        escapar_html(dados.get("iptv", "")),
        "",
        "<b>1.5.1 - Qual o sinal da Fibra?:</b>",
        f"{escapar_html(dados.get('sinal_fibra', ''))} dBm",
        "",
    ]

    sinal_cto = str(dados.get("sinal_cto", "")).strip()
    if precisa_cto(dados.get("tipo", "")) and sinal_cto:
        linhas += [
            "<b>1.5.2 - Qual o sinal da CTO?:</b>",
            f"{escapar_html(sinal_cto)} dBm",
            "",
        ]

    linhas += [
        "<b>1.6 - Houve danos no local?:</b>",
        escapar_html(dados.get("danos", "")),
        "",
        "<b>1.7 - Foi orientado o cliente sobre a rede 2.4Ghz e 5.8Ghz?:</b>",
        escapar_html(dados.get("orientacao", "")),
        "",
        "<b>1.8 - Teste de velocidade dentro do plano contratado?:</b>",
        escapar_html(dados.get("velocidade", "")),
        "",
        "<b>1.9.1 - Qual canal foi escolhido na rede 2.4Ghz?:</b>",
        escapar_html(dados.get("canal24", "")),
        "",
        "<b>1.9.2 - Qual canal foi escolhido na rede 5.8Ghz?:</b>",
        escapar_html(dados.get("canal58", "")),
        "",
    ]

    if precisa_fixacao(dados.get("tipo", "")):
        linhas += [
            "<b>1.10 - Qual a forma de fixação dos equipamentos (roteador e ONU)?:</b>",
            escapar_html(dados.get("fixacao", "")),
            "",
            "<b>1.11 e 1.12 - Padrões de configurações do roteador e acesso remoto habilitado?:</b>",
            escapar_html(dados.get("config_padrao", "")),
            "",
        ]
    else:
        linhas += [
            "<b>1.10 - Padrões de configurações do roteador e acesso remoto habilitado?:</b>",
            escapar_html(dados.get("config_padrao", "")),
            "",
        ]

    if precisa_pos_venda(dados.get("tipo", "")):
        linhas += [
            "<b>1.13 - Feito pós venda imediato?:</b>",
            escapar_html(dados.get("pos_venda", "")),
            "",
        ]

    linhas += [
        "<b>2.1 - Equipamentos ficaram ligados em?:</b>",
        escapar_html(dados.get("energia", "")),
        "",
        "<b>2.2 - Equipamentos foram organizados conforme nossos padrões?:</b>",
        escapar_html(dados.get("organizacao", "")),
        "",
        "<b>Assinatura do cliente:</b>",
        escapar_html(dados.get("assinatura", "")),
        "",
        "<b>Materiais utilizados:</b>",
        escapar_html(dados.get("materiais_utilizados", "")),
        "",
        "<b>Materiais retirados:</b>",
        escapar_html(dados.get("materiais_retirados", "")),
    ]

    return "\n".join(linhas).strip()

async def enviar_texto_longo(update: Update, texto: str):
    partes = [texto[i:i+4000] for i in range(0, len(texto), 4000)]
    for parte in partes:
        await update.message.reply_text(parte, parse_mode="HTML")

async def enviar_grupo_longo(context: ContextTypes.DEFAULT_TYPE, texto: str):
    partes = [texto[i:i+4000] for i in range(0, len(texto), 4000)]
    for parte in partes:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=parte,
            parse_mode="HTML"
        )

# =========================
# COMANDOS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios[update.effective_user.id] = {
        "step": "os",
        "dados": {}
    }
    await update.message.reply_text(
        "Vamos iniciar o relatório.\n\nDigite o número da O.S.:",
        reply_markup=ReplyKeyboardRemove()
    )

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios.pop(update.effective_user.id, None)
    await update.message.reply_text(
        "Atendimento cancelado.",
        reply_markup=ReplyKeyboardRemove()
    )

# =========================
# PERGUNTAS
# =========================
async def perguntar(update: Update, estado: dict):
    step = estado["step"]
    dados = estado["dados"]
    tipo = dados.get("tipo", "")

    if step == "tipo":
        await update.message.reply_text(
            "Selecione o tipo de atendimento:",
            reply_markup=ReplyKeyboardMarkup(TIPOS, resize_keyboard=True)
        )

    elif step == "inicio":
        await update.message.reply_text(
            "Digite a hora iniciada no formato HH:MM\nExemplo: 16:04",
            reply_markup=ReplyKeyboardRemove()
        )

    elif step == "tec_ext":
        await update.message.reply_text(
            "Selecione o técnico externo:",
            reply_markup=ReplyKeyboardMarkup(TECNICOS, resize_keyboard=True)
        )

    elif step == "tec_int":
        await update.message.reply_text(
            "Selecione o técnico interno:",
            reply_markup=ReplyKeyboardMarkup(TECNICOS, resize_keyboard=True)
        )

    elif step == "problema":
        if precisa_problema(tipo):
            await update.message.reply_text(
                "Selecione o problema relatado ou digite outro:",
                reply_markup=ReplyKeyboardMarkup(PROBLEMAS_PADRAO, resize_keyboard=True)
            )
        else:
            estado["step"] = "observacoes"
            await perguntar(update, estado)

    elif step == "solucao":
        if precisa_solucao(tipo):
            await update.message.reply_text(
                "Descreva o que foi feito para solucionar:"
            )
        else:
            estado["step"] = "observacoes"
            await perguntar(update, estado)

    elif step == "observacoes":
        await update.message.reply_text(
            "Observações relevantes (se não tiver, digite: Nenhuma):",
            reply_markup=ReplyKeyboardRemove()
        )

    elif step == "cabo":
        await update.message.reply_text("Quais equipamentos o cliente tem conectado no cabo?")

    elif step == "wifi":
        await update.message.reply_text("Quais equipamentos o cliente tem conectado via Wi-fi?")

    elif step == "local":
        await update.message.reply_text("Qual o local da instalação dos equipamentos?")

    elif step == "segundo_ponto":
        await update.message.reply_text(
            "Cliente necessita de um segundo ponto?",
            reply_markup=ReplyKeyboardMarkup(SIM_NAO, resize_keyboard=True)
        )

    elif step == "iptv":
        await update.message.reply_text(
            "Cliente possui IPTV/TVBOX?",
            reply_markup=ReplyKeyboardMarkup(SIM_NAO, resize_keyboard=True)
        )

    elif step == "sinal_fibra":
        await update.message.reply_text(
            "Qual o sinal da Fibra?\nExemplo: -17.22",
            reply_markup=ReplyKeyboardRemove()
        )

    elif step == "sinal_cto":
        if precisa_cto(tipo):
            await update.message.reply_text(
                "Qual o sinal da CTO?\nSe não medir, digite: Não informado"
            )
        else:
            estado["step"] = "danos"
            await perguntar(update, estado)

    elif step == "danos":
        await update.message.reply_text(
            "Houve danos no local?",
            reply_markup=ReplyKeyboardMarkup(SIM_NAO, resize_keyboard=True)
        )

    elif step == "orientacao":
        await update.message.reply_text(
            "Foi orientado o cliente sobre a rede 2.4Ghz e 5.8Ghz?",
            reply_markup=ReplyKeyboardMarkup(SIM_NAO, resize_keyboard=True)
        )

    elif step == "velocidade":
        await update.message.reply_text(
            "Teste de velocidade dentro do plano contratado?",
            reply_markup=ReplyKeyboardMarkup(SIM_NAO, resize_keyboard=True)
        )

    elif step == "canal24":
        await update.message.reply_text("Qual canal foi escolhido na rede 2.4Ghz?")

    elif step == "canal58":
        await update.message.reply_text("Qual canal foi escolhido na rede 5.8Ghz?")

    elif step == "fixacao":
        if precisa_fixacao(tipo):
            await update.message.reply_text("Qual a forma de fixação dos equipamentos (roteador e ONU)?")
        else:
            estado["step"] = "config_padrao"
            await perguntar(update, estado)

    elif step == "config_padrao":
        await update.message.reply_text(
            "Padrões de configurações do roteador e acesso remoto habilitado?",
            reply_markup=ReplyKeyboardMarkup(SIM_NAO, resize_keyboard=True)
        )

    elif step == "pos_venda":
        if precisa_pos_venda(tipo):
            await update.message.reply_text("Feito pós venda imediato?")
        else:
            estado["step"] = "energia"
            await perguntar(update, estado)

    elif step == "energia":
        await update.message.reply_text(
            "Equipamentos ficaram ligados em?",
            reply_markup=ReplyKeyboardMarkup(ENERGIA, resize_keyboard=True)
        )

    elif step == "organizacao":
        await update.message.reply_text(
            "Equipamentos foram organizados conforme nossos padrões?",
            reply_markup=ReplyKeyboardMarkup(SIM_NAO, resize_keyboard=True)
        )

    elif step == "assinatura":
        await update.message.reply_text("Assinatura do cliente?")

    elif step == "materiais_utilizados":
        await update.message.reply_text(
            "Materiais utilizados:",
            reply_markup=ReplyKeyboardRemove()
        )

    elif step == "materiais_retirados":
        await update.message.reply_text("Materiais retirados (se não houver, digite: Nenhum):")

# =========================
# FLUXO
# =========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    texto = update.message.text.strip()

    if user_id not in usuarios:
        await update.message.reply_text("Digite /start para iniciar.")
        return

    estado = usuarios[user_id]
    step = estado["step"]
    dados = estado["dados"]

    if step == "os":
        dados["os"] = texto
        estado["step"] = "tipo"

    elif step == "tipo":
        dados["tipo"] = texto
        estado["step"] = "inicio"

    elif step == "inicio":
        dados["inicio"] = texto
        estado["step"] = "tec_ext"

    elif step == "tec_ext":
        dados["tec_ext"] = texto
        estado["step"] = "tec_int"

    elif step == "tec_int":
        dados["tec_int"] = texto
        estado["step"] = "problema"

    elif step == "problema":
        dados["problema"] = texto
        estado["step"] = "solucao"

    elif step == "solucao":
        await update.message.reply_text("Corrigindo texto com IA...")
        dados["solucao"] = corrigir_texto_solucao(texto)
        estado["step"] = "observacoes"

    elif step == "observacoes":
        dados["observacoes"] = texto
        estado["step"] = "cabo"

    elif step == "cabo":
        dados["cabo"] = texto
        estado["step"] = "wifi"

    elif step == "wifi":
        dados["wifi"] = texto
        estado["step"] = "local"

    elif step == "local":
        dados["local"] = texto
        estado["step"] = "segundo_ponto"

    elif step == "segundo_ponto":
        dados["segundo_ponto"] = texto
        estado["step"] = "iptv"

    elif step == "iptv":
        dados["iptv"] = texto
        estado["step"] = "sinal_fibra"

    elif step == "sinal_fibra":
        valor = limpar_dbm(texto)
        if valor.lower() not in {"não informado", "nao informado"} and not valor.startswith("-"):
            await update.message.reply_text("Digite um valor válido. Exemplo: -17.22")
            return
        dados["sinal_fibra"] = valor
        estado["step"] = "sinal_cto"

    elif step == "sinal_cto":
        valor = limpar_dbm(texto)
        dados["sinal_cto"] = valor
        estado["step"] = "danos"

    elif step == "danos":
        dados["danos"] = texto
        estado["step"] = "orientacao"

    elif step == "orientacao":
        dados["orientacao"] = texto
        estado["step"] = "velocidade"

    elif step == "velocidade":
        dados["velocidade"] = texto
        estado["step"] = "canal24"

    elif step == "canal24":
        dados["canal24"] = texto
        estado["step"] = "canal58"

    elif step == "canal58":
        dados["canal58"] = texto
        estado["step"] = "fixacao"

    elif step == "fixacao":
        dados["fixacao"] = texto
        estado["step"] = "config_padrao"

    elif step == "config_padrao":
        dados["config_padrao"] = texto
        estado["step"] = "pos_venda"

    elif step == "pos_venda":
        dados["pos_venda"] = texto
        estado["step"] = "energia"

    elif step == "energia":
        dados["energia"] = texto
        estado["step"] = "organizacao"

    elif step == "organizacao":
        dados["organizacao"] = texto
        estado["step"] = "assinatura"

    elif step == "assinatura":
        dados["assinatura"] = texto
        estado["step"] = "materiais_utilizados"

    elif step == "materiais_utilizados":
        dados["materiais_utilizados"] = texto
        estado["step"] = "materiais_retirados"

    elif step == "materiais_retirados":
        dados["materiais_retirados"] = texto
        relatorio = montar_relatorio(dados)

        await update.message.reply_text(
            "Relatório gerado com sucesso.",
            reply_markup=ReplyKeyboardRemove()
        )
        await enviar_texto_longo(update, relatorio)
        await enviar_grupo_longo(context, relatorio)

        usuarios.pop(user_id, None)
        return

    await perguntar(update, estado)

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cancelar", cancelar))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
