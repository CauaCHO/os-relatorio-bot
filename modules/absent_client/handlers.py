from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from core.helpers import validar_os
from core.storage import salvar_historico, salvar_pendencia, listar_pendencias, remover_pendencia
from core.text_processor import processar_texto, languagetool_ativo
from shared.commands import status_texto, pendencias_texto
from shared.keyboards import (
    build_inline_keyboard,
    CONFIRMACAO_ENVIO_OPCOES,
)
from modules.absent_client.report import montar_relatorio_ausencia
from config import CHAT_ID

usuarios_ausencia = {}

EDIT_MAP_AUSENCIA = {
    "os": "os",
    "texto": "texto",
}

EDITAR_AUSENCIA_OPCOES = [
    ("os", "O.S."),
    ("texto", "Texto"),
]


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

    usuarios_ausencia[update.effective_user.id] = {
        "step": "os",
        "dados": {"ocorrencia": "Cliente ausente"},
        "modo": "ausencia",
    }

    await update.effective_message.reply_text(
        "🚪 Vamos iniciar o relatório de Cliente Ausente.\n\n📌 Digite o número da O.S.:",
        reply_markup=ReplyKeyboardRemove()
    )


async def ausente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await ausencia(update, context)


async def paralisada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    usuarios_ausencia[update.effective_user.id] = {
        "step": "os",
        "dados": {"ocorrencia": "O.S. paralisada"},
        "modo": "paralisada",
    }

    await update.effective_message.reply_text(
        "⏸️ Vamos iniciar o relatório de O.S. Paralisada.\n\n📌 Digite o número da O.S.:",
        reply_markup=ReplyKeyboardRemove()
    )


async def pendencias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pendencias_lista = listar_pendencias()
    texto = pendencias_texto(pendencias_lista)

    if not pendencias_lista:
        await update.effective_message.reply_text(texto, parse_mode="HTML")
        return

    opcoes = [(item.get("os", "-"), f"✅ Baixar O.S. {item.get('os', '-')}") for item in pendencias_lista]
    await update.effective_message.reply_text(
        texto,
        parse_mode="HTML",
        reply_markup=build_inline_keyboard("baixar_pendencia", opcoes, per_row=1)
    )


async def baixar_pendencia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.effective_message.reply_text("Use assim:\n/baixar_pendencia 331277")
        return

    os_numero = context.args[0].strip()
    remover_pendencia(os_numero)

    await update.effective_message.reply_text(
        f"✅ O.S. {os_numero} removida da lista de pendências."
    )


async def cancelar_ausencia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios_ausencia.pop(update.effective_user.id, None)
    await update.effective_message.reply_text("❌ Fluxo cancelado.", reply_markup=ReplyKeyboardRemove())


async def status_ausencia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fluxo_ativo = update.effective_user.id in usuarios_ausencia
    step = usuarios_ausencia.get(update.effective_user.id, {}).get("step")

    await update.effective_message.reply_text(
        status_texto(fluxo_ativo, step, languagetool_ativo(), "Módulo Ausente / Paralisada"),
        parse_mode="HTML"
    )


async def perguntar(message, estado: dict):
    step = estado["step"]

    if step == "texto":
        await message.reply_text("📝 Escreva o texto do relatório:", reply_markup=ReplyKeyboardRemove())

    elif step == "confirmar":
        await message.reply_text(
            "📨 Revisão final do relatório\n\nEscolha uma opção:",
            reply_markup=build_inline_keyboard("confirmar_ausencia", CONFIRMACAO_ENVIO_OPCOES)
        )

    elif step == "editar":
        await message.reply_text(
            "✏️ Selecione a etapa que deseja editar:",
            reply_markup=build_inline_keyboard("editar_ausencia", EDITAR_AUSENCIA_OPCOES, per_row=1)
        )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query or query.message.chat.type != "private":
        return

    await query.answer()

    try:
        field, code = query.data.split("|", 1)
    except ValueError:
        return

    if field == "baixar_pendencia":
        remover_pendencia(code)
        await query.message.reply_text(f"✅ O.S. {code} removida das pendências.")
        return

    user_id = query.from_user.id
    if user_id not in usuarios_ausencia:
        return

    estado = usuarios_ausencia[user_id]
    step = estado["step"]
    dados = estado["dados"]

    if step == "confirmar" and field == "confirmar_ausencia":
        if code == "enviar":
            relatorio = montar_relatorio_ausencia(dados)
            await enviar_grupo_longo(context, relatorio, query.from_user)
            salvar_historico(
                {"os": dados.get("os"), "tipo": dados.get("ocorrencia")},
                relatorio,
                "Ausência/Paralisada"
            )

            if dados.get("ocorrencia") == "O.S. paralisada":
                username = f"@{query.from_user.username}" if query.from_user.username else query.from_user.first_name
                salvar_pendencia(dados.get("os"), dados.get("texto", "-"), username)

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
        estado["step"] = "texto"

    elif step == "texto":
        dados["texto"] = processar_texto(texto or "-", "ausencia")
        estado["step"] = "confirmar"

    else:
        return

    await perguntar(update.message, estado)
