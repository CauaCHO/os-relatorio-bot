import json
import os
from datetime import datetime

BASE_DIR = "data"

ARQ_HISTORICO = f"{BASE_DIR}/historico_relatorios.json"
ARQ_USUARIOS = f"{BASE_DIR}/usuarios_bot.json"
ARQ_PENDENCIAS = f"{BASE_DIR}/os_paralisadas.json"


def garantir_pasta():
    os.makedirs(BASE_DIR, exist_ok=True)


def carregar_json(arquivo, default):
    garantir_pasta()

    if not os.path.exists(arquivo):
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(default, f, ensure_ascii=False, indent=4)
        return default

    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return default


def salvar_json(arquivo, dados):
    garantir_pasta()

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


# =========================
# HISTÓRICO
# =========================

def salvar_historico(dados, relatorio, modulo):
    historico = carregar_json(ARQ_HISTORICO, [])

    historico.append({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "modulo": modulo,
        "os": dados.get("os", "-"),
        "tipo": dados.get("tipo", dados.get("ocorrencia", "-")),
        "relatorio": relatorio
    })

    salvar_json(ARQ_HISTORICO, historico)


# =========================
# USUÁRIOS
# =========================

def salvar_tecnico_usuario(user_id, tecnico):
    dados = carregar_json(ARQ_USUARIOS, {})
    dados[str(user_id)] = tecnico
    salvar_json(ARQ_USUARIOS, dados)


def obter_tecnico_usuario(user_id):
    dados = carregar_json(ARQ_USUARIOS, {})
    return dados.get(str(user_id))


# =========================
# PENDÊNCIAS
# =========================

def salvar_pendencia(os_numero, motivo, usuario):
    dados = carregar_json(ARQ_PENDENCIAS, [])

    for item in dados:
        if item["os"] == os_numero:
            return

    dados.append({
        "os": os_numero,
        "motivo": motivo,
        "usuario": usuario,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M")
    })

    salvar_json(ARQ_PENDENCIAS, dados)


def listar_pendencias():
    return carregar_json(ARQ_PENDENCIAS, [])


def obter_pendencia(os_numero):
    dados = carregar_json(ARQ_PENDENCIAS, [])

    for item in dados:
        if item["os"] == os_numero:
            return item

    return None


def remover_pendencia(os_numero):
    dados = carregar_json(ARQ_PENDENCIAS, [])

    dados = [x for x in dados if x["os"] != os_numero]

    salvar_json(ARQ_PENDENCIAS, dados)