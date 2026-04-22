from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

from config import TOKEN
from core.error_handler import error_handler

from modules.menu.handlers import start_menu, handle_menu_callback

from modules.os_report.handlers import (
    atendimento,
    assistencia,
    instalacao,
    mudanca,
    cancelar,
    ajuda,
    status,
    handle_message as os_msg,
    handle_callback as os_callback
)

from modules.material_delivery.handlers import (
    retirada,
    estoque,
    cancelar_material,
    status_material,
    handle_message as material_msg,
    handle_callback as material_callback
)

from modules.absent_client.handlers import (
    ausencia,
    ausente,
    paralisada,
    pendencias,
    cancelar_ausencia,
    status_ausencia,
    handle_message as ausencia_msg,
    handle_callback as ausencia_callback
)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # MENU
    app.add_handler(CommandHandler("start", start_menu))

    # GERAL
    app.add_handler(CommandHandler("ajuda", ajuda))

    # ATENDIMENTO
    app.add_handler(CommandHandler("atendimento", atendimento))
    app.add_handler(CommandHandler("assistencia", assistencia))
    app.add_handler(CommandHandler("instalacao", instalacao))
    app.add_handler(CommandHandler("mudanca", mudanca))
    app.add_handler(CommandHandler("cancelar", cancelar))
    app.add_handler(CommandHandler("status", status))

    # ESTOQUE
    app.add_handler(CommandHandler("retirada", retirada))
    app.add_handler(CommandHandler("estoque", estoque))
    app.add_handler(CommandHandler("cancelar_material", cancelar_material))
    app.add_handler(CommandHandler("status_material", status_material))

    # AUSENTE / PARALISADA
    app.add_handler(CommandHandler("ausente", ausente))
    app.add_handler(CommandHandler("ausencia", ausencia))
    app.add_handler(CommandHandler("paralisada", paralisada))
    app.add_handler(CommandHandler("pendencias", pendencias))
    app.add_handler(CommandHandler("cancelar_ausencia", cancelar_ausencia))
    app.add_handler(CommandHandler("status_ausencia", status_ausencia))

    # CALLBACK MENU
    app.add_handler(
        CallbackQueryHandler(
            handle_menu_callback,
            pattern=r"^(menu|menu_atendimento)\|"
        )
    )

    # CALLBACKS MÓDULOS
    app.add_handler(CallbackQueryHandler(os_callback))
    app.add_handler(CallbackQueryHandler(material_callback))
    app.add_handler(CallbackQueryHandler(ausencia_callback))

    # TEXTOS
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, os_msg), group=1)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, material_msg), group=2)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ausencia_msg), group=3)

    app.add_error_handler(error_handler)

    print("Bot rodando...")
    app.run_polling()


if __name__ == "__main__":
    main()