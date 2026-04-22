from telegram import Update
from telegram.ext import ContextTypes

from shared.keyboards import menu_principal, menu_atendimento

from modules.os_report.handlers import (
    iniciar_fluxo_assistencia,
    iniciar_fluxo_instalacao,
    iniciar_fluxo_mudanca,
)

from modules.material_delivery.handlers import estoque
from modules.absent_client.handlers import ausencia, paralisada, pendencias


async def start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    await update.message.reply_text(
        "🚀 <b>Sistema Flash Reports</b>\n\n"
        "Selecione o relatório:",
        parse_mode="HTML",
        reply_markup=menu_principal()
    )


async def handle_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        campo, valor = query.data.split("|", 1)
    except:
        return

    if campo == "menu":

        if valor == "atendimento":
            await query.message.reply_text(
                "🔧 <b>Atendimento</b>\n\nEscolha o tipo:",
                parse_mode="HTML",
                reply_markup=menu_atendimento()
            )

        elif valor == "retirada":
            await query.message.reply_text(
                "📦 Fluxo Retirada será separado do Estoque.\nEm implantação."
            )

        elif valor == "estoque":
            await estoque(update, context)

        elif valor == "ausente":
            await ausencia(update, context)

        elif valor == "paralisada":
            await paralisada(update, context)

        elif valor == "pendencias":
            await pendencias(update, context)

    elif campo == "menu_atendimento":

        if valor == "assistencia":
            await iniciar_fluxo_assistencia(update, context)

        elif valor == "instalacao":
            await iniciar_fluxo_instalacao(update, context)

        elif valor == "mudanca":
            await iniciar_fluxo_mudanca(update, context)