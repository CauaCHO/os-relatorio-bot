from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import BOT_TOKEN
from core.engine import (
    start, cmd_assistencia, cmd_retirada, cmd_estoque, cmd_ausente, cmd_paralisada,
    cmd_pendencias, cmd_baixar_pendencia, cmd_config, callback_handler, message_handler
)
from core.error_handler import error_handler


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN não configurado no Railway.")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("assistencia", cmd_assistencia))
    app.add_handler(CommandHandler("retirada", cmd_retirada))
    app.add_handler(CommandHandler("estoque", cmd_estoque))
    app.add_handler(CommandHandler("ausente", cmd_ausente))
    app.add_handler(CommandHandler("paralisada", cmd_paralisada))
    app.add_handler(CommandHandler("pendencias", cmd_pendencias))
    app.add_handler(CommandHandler("baixar_pendencia", cmd_baixar_pendencia))
    app.add_handler(CommandHandler("config", cmd_config))

    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    app.add_error_handler(error_handler)

    print("Sistema Flash Reports v6.5 Ultra rodando...")
    app.run_polling()


if __name__ == "__main__":
    main()
