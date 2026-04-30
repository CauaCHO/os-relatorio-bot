from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from config import CHAT_ID
from core.helpers import validar_os
from core.storage import salvar_historico
from shared.keyboards import (
    build_inline_keyboard,
    CONFIRMACAO_ENVIO_OPCOES,
    GERAR_RETIRADA_OPCOES,
    TIPO_RETIRADA_OPCOES,
)
from modules.client_withdrawal.report import montar_relatorio_retirada_cliente
from modules.material_delivery.handlers import iniciar_fluxo_retirada_prefill

usuarios_retirada_cliente = {}


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


async def retirada_cliente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    usuarios_retirada_cliente[update.effective_user.id] = {
        "step": "os",
        "dados": {}
    }

    await update.effective_message.reply_text(
        "📦 Vamos iniciar o relatório de Retirada Cliente.\n\n📌 Digite o número da O.S.:",
        reply_markup=ReplyKeyboardRemove()
    )


async def cancelar_retirada_cliente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios_retirada_cliente.pop(update.effective_user.id, None)
    await update.effective_message.reply_text(
        "❌ Retirada Cliente cancelada.",
        reply_markup=ReplyKeyboardRemove()
    )


async def perguntar(message, estado):
    step = estado["step"]

    if step == "equipamentos":
        await message.reply_text(
            "📦 Digite os equipamentos retirados da casa do cliente:\n\n"
            "Exemplo:\n"
            "1 roteador ZTE + fonte\n"
            "1 ONU Chima + fonte\n"
            "1 patchcord",
            reply_markup=ReplyKeyboardRemove()
        )

    elif step == "confirmar":
        await message.reply_text(
            "📨 Revisão final da Retirada Cliente\n\nEscolha uma opção:",
            reply_markup=build_inline_keyboard("cw_confirmar", CONFIRMACAO_ENVIO_OPCOES)
        )

    elif step == "gerar_estoque":
        await message.reply_text(
            "🏢 Deseja gerar também o relatório de Entrega no Estoque?",
            reply_markup=build_inline_keyboard("cw_estoque", GERAR_RETIRADA_OPCOES)
        )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query or query.message.chat.type != "private":
        return

    await query.answer()

    user_id = query.from_user.id
    if user_id not in usuarios_retirada_cliente:
        return

    estado = usuarios_retirada_cliente[user_id]
    dados = estado["dados"]

    try:
        field, code = query.data.split("|", 1)
    except ValueError:
        return

    if field == "cw_confirmar":
        if code == "enviar":
            relatorio = montar_relatorio_retirada_cliente(dados)
            await enviar_grupo_longo(context, relatorio, query.from_user)
            salvar_historico(
                {"os": dados.get("os"), "tipo": "Retirada Cliente"},
                relatorio,
                "Retirada Cliente"
            )

            estado["step"] = "gerar_estoque"
            await query.message.reply_text(
                "✅ Relatório de Retirada Cliente enviado com sucesso.\n\n"
                f"📋 O.S.: {dados.get('os', '-')}"
            )
            await perguntar(query.message, estado)
            return

        if code == "editar":
            estado["step"] = "equipamentos"
            await perguntar(query.message, estado)
            return

        usuarios_retirada_cliente.pop(user_id, None)
        await query.message.reply_text(
            "❌ Fluxo cancelado.",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    if field == "cw_estoque":
        os_numero = dados.get("os", "-")
        usuarios_retirada_cliente.pop(user_id, None)

        if code == "sim":
            iniciar_fluxo_retirada_prefill(user_id, os_numero)
            await query.message.reply_text(
                f"🏢 Iniciando Entrega no Estoque para a O.S. {os_numero}.",
                reply_markup=build_inline_keyboard("tipo_retirada", TIPO_RETIRADA_OPCOES)
            )
        else:
            await query.message.reply_text(
                "👍 Fluxo finalizado.",
                reply_markup=ReplyKeyboardRemove()
            )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    user_id = update.effective_user.id
    if user_id not in usuarios_retirada_cliente:
        return

    estado = usuarios_retirada_cliente[user_id]
    dados = estado["dados"]
    texto = update.effective_message.text.strip()

    if estado["step"] == "os":
        if not validar_os(texto):
            await update.effective_message.reply_text("⚠️ Número de O.S. inválido. Digite apenas números.")
            return

        dados["os"] = texto
        estado["step"] = "equipamentos"
        await perguntar(update.effective_message, estado)
        return

    if estado["step"] == "equipamentos":
        dados["equipamentos"] = texto or "-"
        estado["step"] = "confirmar"
        await perguntar(update.effective_message, estado)
        return
