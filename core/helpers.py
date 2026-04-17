from datetime import datetime, timedelta
import re


def valor_ou_traco(valor: str) -> str:
    valor = str(valor).strip() if valor is not None else ""
    return valor if valor else "-"


def escapar_html(texto: str) -> str:
    if texto is None:
        return ""
    return (
        str(texto)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def limpar_dbm(valor: str) -> str:
    return valor.replace("dBm", "").replace("dB", "").strip()


def validar_os(texto: str) -> bool:
    return texto.isdigit()


def validar_hora(texto: str) -> bool:
    return re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", texto) is not None


def parse_hora(hora_str: str):
    try:
        return datetime.strptime(hora_str.strip(), "%H:%M")
    except Exception:
        return None


def calcular_tempo_gasto(inicio: str, fim: str) -> str:
    hora_inicio = parse_hora(inicio)
    hora_fim = parse_hora(fim)

    if not hora_inicio or not hora_fim:
        return "-"

    if hora_fim < hora_inicio:
        hora_fim += timedelta(days=1)

    diferenca = hora_fim - hora_inicio
    total_minutos = int(diferenca.total_seconds() // 60)
    horas = total_minutos // 60
    minutos = total_minutos % 60

    if horas > 0 and minutos > 0:
        return f"{horas} h {minutos} min"
    if horas > 0:
        return f"{horas} h"
    return f"{minutos} min"


def normalizar_sinal(texto: str):
    valor = limpar_dbm(texto)

    if valor.lower() in {"não informado", "nao informado"}:
        return "-"

    if valor == "-":
        return "-"

    valor = valor.replace(",", ".")

    if valor.startswith("-"):
        corpo = valor[1:]
        if corpo.replace(".", "", 1).isdigit():
            return valor
        return None

    if valor.replace(".", "", 1).isdigit():
        return f"-{valor}"

    return None


def is_assistencia(tipo: str) -> bool:
    return tipo == "Assistência"