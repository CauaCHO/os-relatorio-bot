from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from config import TOKEN
from core.error_handler import error_handler

from modules.os_report.handlers import (
    start,
    assistencia,
    instalacao,
    mudanca,
    cancelar,
    ajuda,
    status,
    handle_message as handle_message_os,
    handle_callback as handle_callback_os,
)

from modules.material_delivery.handlers import (
    retirada,
    cancelar_material,
    status_material,
    handle_message as handle_message_material,
    handle_callback as handle_callback_material,
)

from modules.absent_client.handlers import (
    ausencia,
    cancelar_ausencia,
    status_ausencia,
    handle_message as handle_message_ausencia,
    handle_callback as handle_callback_ausencia,
)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("assistencia", assistencia))
    app.add_handler(CommandHandler("instalacao", instalacao))
    app.add_handler(CommandHandler("mudanca", mudanca))
    app.add_handler(CommandHandler("cancelar", cancelar))
    app.add_handler(CommandHandler("ajuda", ajuda))
    app.add_handler(CommandHandler("status", status))

    app.add_handler(CommandHandler("retirada", retirada))
    app.add_handler(CommandHandler("cancelar_material", cancelar_material))
    app.add_handler(CommandHandler("status_material", status_material))

    app.add_handler(CommandHandler("ausencia", ausencia))
    app.add_handler(CommandHandler("cancelar_ausencia", cancelar_ausencia))
    app.add_handler(CommandHandler("status_ausencia", status_ausencia))

    app.add_handler(CallbackQueryHandler(
        handle_callback_os,
        pattern=r"^(reiniciar_fluxo|tipo|tec_ext|tec_int|problema|segundo_ponto|iptv|danos|supervisor_ciente|orientacao|velocidade|canal24|canal5|config_padrao|energia|organizacao|assinatura|confirmar|editar_os|gerar_retirada)\|"
    ))

    app.add_handler(CallbackQueryHandler(
        handle_callback_material,
        pattern=r"^(reiniciar_material|tipo_retirada|tem_roteador|roteador|tem_onu|onu|patchcord|outro_tem|destino|recebido_por|cidade|confirmar_material|editar_material)\|"
    ))

    app.add_handler(CallbackQueryHandler(
        handle_callback_ausencia,
        pattern=r"^(reiniciar_ausencia|ocorrencia_ausencia|confirmar_ausencia|editar_ausencia)\|"
    ))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message_os), group=1)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message_material), group=2)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message_ausencia), group=3)

    app.add_error_handler(error_handler)

    print("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()