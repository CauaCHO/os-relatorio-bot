from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from core.helpers import validar_os
from core.storage import salvar_historico
from core.text_processor import processar_texto, languagetool_ativo
from shared.commands import status_texto
from shared.keyboards import (
    build_inline_keyboard,
    REINICIAR_FLUXO_OPCOES,
    CONFIRMACAO_ENVIO_OPCOES,
    OCORRENCIA_AUSENCIA_OPCOES,
    OCORRENCIA_AUSENCIA_MAP,
)
from modules.absent_client.report import montar_relatorio_ausencia
from config import CHAT_ID

usuarios_ausencia = {}

EDIT_MAP_AUSENCIA = {
    "os": "os",
    "ocorrencia": "ocorrencia",
    "texto": "texto",
}

EDITAR_AUSENCIA_OPCOES = [
    ("os", "O.S."),
    ("ocorrencia", "Ocorrência"),
    ("texto", "Texto"),
]


async def enviar_texto_longo(message, texto: str):
    partes = [texto[i:i + 4000] for i in range(0, len(texto), 4000)]
    for parte in partes:
        await message.reply_text(parte, parse_mode="HTML")


def montar_cabecalho_grupo(user) -> str:
    username = f"@{user.username}" if user.username else None
    nome = " ".join(x for x in [user.first_name, user.last_name] if x).strip()
    identificacao = username or nome or str(user.id)
    return f"👤 <b>Preenchido por:</b> {identificacao}\n\n"


async def enviar_grupo_longo(context: ContextTypes.DEFAULT_TYPE, texto: str, user):
    texto = montar_cabecalho_grupo(user) + texto
    partes = [texto[i:i + 4000] for i in range(0, len(texto), 4000)]
    for parte in partes:
        await context.bot.send_message(chat_id=CHAT_ID, text=parte, parse_mode="HTML")


async def ausencia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    if update.effective_user.id in usuarios_ausencia:
        await update.message.reply_text(
            "⚠️ Você já possui um relatório de ausência/paralisada em andamento.\n\nDeseja reiniciar?",
            reply_markup=build_inline_keyboard("reiniciar_ausencia", REINICIAR_FLUXO_OPCOES)
        )
        return

    usuarios_ausencia[update.effective_user.id] = {
        "step": "os",
        "dados": {},
        "pending_start": None,
    }
    await update.message.reply_text(
        "📄 Vamos iniciar o relatório de Cliente Ausente / O.S. Paralisada.\n\n📌 Digite o número da O.S.:",
        reply_markup=ReplyKeyboardRemove()
    )


async def cancelar_ausencia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios_ausencia.pop(update.effective_user.id, None)
    await update.message.reply_text("❌ Relatório de ausência cancelado.", reply_markup=ReplyKeyboardRemove())


async def status_ausencia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fluxo_ativo = update.effective_user.id in usuarios_ausencia
    step = usuarios_ausencia.get(update.effective_user.id, {}).get("step")
    await update.message.reply_text(
        status_texto(fluxo_ativo, step, languagetool_ativo(), "Módulo Cliente Ausente / O.S. Paralisada"),
        parse_mode="HTML"
    )


async def perguntar(message, estado: dict):
    step = estado["step"]

    if step == "ocorrencia":
        await message.reply_text(
            "📌 Selecione a ocorrência:",
            reply_markup=build_inline_keyboard("ocorrencia_ausencia", OCORRENCIA_AUSENCIA_OPCOES)
        )
    elif step == "motivo_outro":
        await message.reply_text("✍️ Escreva a ocorrência:", reply_markup=ReplyKeyboardRemove())
    elif step == "texto":
        await message.reply_text("📝 Escreva o texto do relatório:", reply_markup=ReplyKeyboardRemove())
    elif step == "confirmar":
        relatorio = montar_relatorio_ausencia(estado["dados"])
        await enviar_texto_longo(message, relatorio)
        await message.reply_text("📨 O que deseja fazer?", reply_markup=build_inline_keyboard("confirmar_ausencia", CONFIRMACAO_ENVIO_OPCOES))
    elif step == "editar":
        await message.reply_text("✏️ Selecione a etapa que deseja editar:", reply_markup=build_inline_keyboard("editar_ausencia", EDITAR_AUSENCIA_OPCOES, per_row=1))


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query or query.message.chat.type != "private":
        return
    await query.answer()

    user_id = query.from_user.id
    if user_id not in usuarios_ausencia:
        return

    estado = usuarios_ausencia[user_id]
    step = estado["step"]
    dados = estado["dados"]

    field, code = query.data.split("|", 1)
    valid = False

    if field == "reiniciar_ausencia":
        if code == "reiniciar_sim":
            usuarios_ausencia[user_id] = {"step": "os", "dados": {}, "pending_start": None}
            await query.message.reply_text("📌 Digite o número da O.S.:", reply_markup=ReplyKeyboardRemove())
            return
        else:
            await query.message.reply_text("👍 Fluxo atual mantido.")
            return

    if step == "ocorrencia" and field == "ocorrencia_ausencia":
        if code == "outro":
            dados["ocorrencia"] = "Outro"
            estado["step"] = "motivo_outro"
        else:
            dados["ocorrencia"] = OCORRENCIA_AUSENCIA_MAP.get(code, code)
            estado["step"] = "texto"
        valid = True

    elif step == "confirmar" and field == "confirmar_ausencia":
        if code == "enviar":
            relatorio = montar_relatorio_ausencia(dados)
            await enviar_grupo_longo(context, relatorio, query.from_user)
            salvar_historico({"os": dados.get("os"), "tipo": dados.get("ocorrencia")}, relatorio, "Ausência/Paralisada")
            await query.message.reply_text("✅ Relatório enviado com sucesso.", reply_markup=ReplyKeyboardRemove())
            usuarios_ausencia.pop(user_id, None)
            return
        elif code == "editar":
            estado["step"] = "editar"
            await perguntar(query.message, estado)
            return
        else:
            usuarios_ausencia.pop(user_id, None)
            await query.message.reply_text("❌ Fluxo cancelado.", reply_markup=ReplyKeyboardRemove())
            return

    elif step == "editar" and field == "editar_ausencia":
        novo_step = EDIT_MAP_AUSENCIA.get(code)
        if novo_step:
            estado["step"] = novo_step
            await perguntar(query.message, estado)
            return

    if not valid:
        return

    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except Exception:
        pass

    await perguntar(query.message, estado)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    user_id = update.effective_user.id
    if user_id not in usuarios_ausencia:
        return

    estado = usuarios_ausencia[user_id]
    step = estado["step"]
    dados = estado["dados"]
    texto = update.message.text.strip()

    if step == "os":
        if not validar_os(texto):
            await update.message.reply_text("⚠️ Número de O.S. inválido. Digite apenas números.")
            return
        dados["os"] = texto
        estado["step"] = "ocorrencia"
    elif step == "motivo_outro":
        dados["ocorrencia"] = processar_texto(texto or "-", "ausencia")
        estado["step"] = "texto"
    elif step == "texto":
        dados["texto"] = processar_texto(texto or "-", "ausencia")
        estado["step"] = "confirmar"
    else:
        return

    await perguntar(update.message, estado)