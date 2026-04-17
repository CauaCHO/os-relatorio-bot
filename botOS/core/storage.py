import json
from pathlib import Path
from datetime import datetime
from config import ARQUIVO_HISTORICO, ARQUIVO_USUARIOS

arquivo_historico = Path(ARQUIVO_HISTORICO)
arquivo_usuarios = Path(ARQUIVO_USUARIOS)


def _garantir_pasta(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def _ler_json(path: Path, default):
    _garantir_pasta(path)
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _escrever_json(path: Path, data):
    _garantir_pasta(path)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def salvar_historico(dados: dict, relatorio: str, categoria: str = "O.S."):
    historico = _ler_json(arquivo_historico, [])
    historico.append({
        "categoria": categoria,
        "os": dados.get("os", "-"),
        "tipo": dados.get("tipo", "-"),
        "tecnico_externo": dados.get("tec_ext", "-"),
        "tecnico_interno": dados.get("tec_int", "-"),
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "relatorio": relatorio,
    })
    _escrever_json(arquivo_historico, historico)


def salvar_tecnico_usuario(user_id: int, tecnico_nome: str):
    usuarios = _ler_json(arquivo_usuarios, {})
    usuarios[str(user_id)] = tecnico_nome
    _escrever_json(arquivo_usuarios, usuarios)


def obter_tecnico_usuario(user_id: int):
    usuarios = _ler_json(arquivo_usuarios, {})
    return usuarios.get(str(user_id))