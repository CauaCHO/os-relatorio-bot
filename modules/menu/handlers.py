from telegram import Update
from telegram.ext import ContextTypes

from shared.keyboards import menu_principal, menu_atendimento_v5
from modules.os_report.handlers import iniciar_fluxo_tipo_v5, ajuda
from modules.material_delivery.handlers import estoque
from modules.absent_client.handlers import ausencia, paralisada, pendencias
from modules.client_withdrawal.handlers import retirada_cliente


async def start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    await update.effective_message.reply_text(
        "🚀 <b>Sistema Flash Reports v5.2</b>\n\n"
        "Selecione o módulo:",
        parse_mode="HTML",
        reply_markup=menu_principal()
    )


async def handle_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query or query.message.chat.type != "private":
        return

    await query.answer()

    try:
        campo, valor = query.data.split("|", 1)
    except Exception:
        return

    if campo == "menu":
        if valor == "atendimento":
            await query.message.reply_text(
                "🔧 <b>Atendimento</b>\n\nEscolha o tipo:",
                parse_mode="HTML",
                reply_markup=menu_atendimento_v5()
            )
            return

        if valor == "retirada_cliente":
            await retirada_cliente(update, context)
            return

        if valor == "estoque":
            await estoque(update, context)
            return

        if valor == "ausente":
            await ausencia(update, context)
            return

        if valor == "paralisada":
            await paralisada(update, context)
            return

        if valor == "pendencias":
            await pendencias(update, context)
            return

        if valor == "sistema":
            await ajuda(update, context)
            return

    if campo == "menu_atendimento_v5":
        await iniciar_fluxo_tipo_v5(update, context, valor)
