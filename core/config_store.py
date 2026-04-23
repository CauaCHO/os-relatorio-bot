import json
from pathlib import Path
from config import ARQUIVO_APP_CONFIG, CONFIG_ALLOWED_USERS, CONFIG_PASSWORD


DEFAULT_APP_CONFIG = {
    "allowed_config_users": CONFIG_ALLOWED_USERS,
    "config_password": CONFIG_PASSWORD,
    "tecnicos": [
        "Cauã Henrique",
        "Jamildo Ferreira",
        "Erick",
        "Valdisney",
        "Wellington Arouca",
        "Wesley Texeira"
    ],
    "roteadores": [
        "ZTE H3601PE",
        "ZTE H199A",
        "Mercusys AC12G",
        "Mercusys MR80X",
        "TP-Link C20",
        "TP-Link C5",
        "TP-Link C6"
    ],
    "locais_instalacao": [
        "Sala",
        "Cozinha",
        "Quarto",
        "Escritório",
        "Área externa",
        "Outro"
    ],
    "estoque_recebedores": {
        "Estoque FND": ["Cauã"],
        "Estoque VT": ["Giovani", "Dwedinei", "Leonardo"],
        "Estoque SJRP": ["Kesli"]
    }
}


def _path() -> Path:
    return Path(ARQUIVO_APP_CONFIG)


def _garantir():
    p = _path()
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text(json.dumps(DEFAULT_APP_CONFIG, ensure_ascii=False, indent=2), encoding="utf-8")


def load_app_config() -> dict:
    _garantir()
    try:
        return json.loads(_path().read_text(encoding="utf-8"))
    except Exception:
        save_app_config(DEFAULT_APP_CONFIG)
        return DEFAULT_APP_CONFIG.copy()


def save_app_config(data: dict):
    _garantir()
    _path().write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def is_config_user(username: str | None) -> bool:
    if not username:
        return False
    data = load_app_config()
    allowed = data.get("allowed_config_users", [])
    return username.lstrip("@") in [u.lstrip("@") for u in allowed]


def check_config_password(password: str) -> bool:
    data = load_app_config()
    return password == data.get("config_password", CONFIG_PASSWORD)


def get_tecnicos() -> list[str]:
    return load_app_config().get("tecnicos", [])


def set_tecnicos(items: list[str]):
    data = load_app_config()
    data["tecnicos"] = items
    save_app_config(data)


def get_roteadores() -> list[str]:
    return load_app_config().get("roteadores", [])


def set_roteadores(items: list[str]):
    data = load_app_config()
    data["roteadores"] = items
    save_app_config(data)


def get_locais_instalacao() -> list[str]:
    return load_app_config().get("locais_instalacao", [])


def set_locais_instalacao(items: list[str]):
    data = load_app_config()
    data["locais_instalacao"] = items
    save_app_config(data)


def get_estoque_recebedores(destino: str) -> list[str]:
    data = load_app_config()
    return data.get("estoque_recebedores", {}).get(destino, [])


def set_estoque_recebedores(destino: str, items: list[str]):
    data = load_app_config()
    if "estoque_recebedores" not in data:
        data["estoque_recebedores"] = {}
    data["estoque_recebedores"][destino] = items
    save_app_config(data)


def add_item(lista: list[str], valor: str) -> list[str]:
    valor = valor.strip()
    if valor and valor not in lista:
        lista.append(valor)
    return lista


def remove_item(lista: list[str], valor: str) -> list[str]:
    return [x for x in lista if x != valor]