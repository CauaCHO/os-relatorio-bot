import traceback


async def error_handler(update, context):
    print("=== ERRO NO BOT ===")
    print(f"Erro: {context.error}")
    traceback.print_exc()

    try:
        if update and getattr(update, "effective_chat", None):
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⚠️ Ocorreu um erro interno. Tente novamente ou use /cancelar."
            )
    except Exception:
        pass