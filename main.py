from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import BOT_TOKEN
from core.error_handler import error_handler
from core.engine import start, assistencia_cmd, retirada_cmd, estoque_cmd, ausente_cmd, paralisada_cmd, pendencias_cmd, baixar_pendencia_cmd, config_cmd, handle_callback, handle_message

def main():
    if not BOT_TOKEN: raise RuntimeError('Variável BOT_TOKEN não configurada.')
    app=ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start',start)); app.add_handler(CommandHandler('assistencia',assistencia_cmd)); app.add_handler(CommandHandler('retirada',retirada_cmd)); app.add_handler(CommandHandler('estoque',estoque_cmd)); app.add_handler(CommandHandler('ausente',ausente_cmd)); app.add_handler(CommandHandler('paralisada',paralisada_cmd)); app.add_handler(CommandHandler('pendencias',pendencias_cmd)); app.add_handler(CommandHandler('baixar_pendencia',baixar_pendencia_cmd)); app.add_handler(CommandHandler('config',config_cmd))
    app.add_handler(CallbackQueryHandler(handle_callback)); app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)); app.add_error_handler(error_handler)
    print('Sistema Flash Reports v6 rodando...'); app.run_polling()
if __name__=='__main__': main()
