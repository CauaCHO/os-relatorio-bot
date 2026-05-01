import traceback
async def error_handler(update, context):
    print('========== ERRO CAPTURADO ==========')
    print(context.error)
    traceback.print_exception(type(context.error), context.error, context.error.__traceback__)
    print('====================================')
