import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

DATA_DIR = "data"
CONFIG_FILE = "data/config.json"
RELATORIOS_FILE = "data/relatorios.json"
PENDENCIAS_FILE = "data/pendencias.json"
USUARIOS_FILE = "data/usuarios.json"
LOGS_FILE = "data/logs.json"

CONFIG_PASSWORD = os.getenv("CONFIG_PASSWORD", "xxxxx")
CONFIG_ALLOWED_USERS = ["GenericCHO", "EstoqueFlashNetFND"]
CONFIG_ALLOWED_IDS = []
