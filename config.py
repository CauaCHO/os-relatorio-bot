import os

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

ARQUIVO_HISTORICO = "data/historico_relatorios.json"
ARQUIVO_USUARIOS = "data/usuarios_bot.json"
ARQUIVO_PENDENCIAS = "data/os_paralisadas.json"
ARQUIVO_APP_CONFIG = "data/app_config.json"

CONFIG_ALLOWED_USERS = ["GenericCHO", "EstoqueFlashNetFND"]
CONFIG_PASSWORD = os.getenv("CONFIG_PASSWORD", "xxxxx")