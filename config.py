import os

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

ARQUIVO_HISTORICO = "data/historico_relatorios.json"
ARQUIVO_USUARIOS = "data/usuarios_bot.json"
ARQUIVO_PENDENCIAS = "data/os_paralisadas.json"
ARQUIVO_APP_CONFIG = "data/app_config.json"

CONFIG_ALLOWED_USERS = ["GenericCHO", "EstoqueFlashNetFND"]

# Opcional: coloque IDs do Telegram aqui para liberar acesso ao /config.
# O próprio /config mostra o ID do usuário ao pedir senha.
CONFIG_ALLOWED_IDS = []

CONFIG_PASSWORD = os.getenv("CONFIG_PASSWORD", "xxxxx")
