import traceback
from shared.storage import append_json
from config import LOGS_FILE


async def error_handler(update, context):
    erro = str(context.error)
    print("========== ERRO CAPTURADO ==========")
    print(erro)
    traceback.print_exception(type(context.error), context.error, context.error.__traceback__)
    print("====================================")
    append_json(LOGS_FILE, {"erro": erro})
