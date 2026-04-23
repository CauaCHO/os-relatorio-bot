import re
from datetime import datetime
from modules.os_report.modelos import MODELOS_ATENDIMENTO


def _campo_deve_aparecer(campo: dict, dados: dict) -> bool:
    cond = campo.get("condicao")
    if not cond:
        return True
    return dados.get(cond["campo"]) == cond["valor"]


def _normalizar_vazio(valor) -> str:
    if valor is None:
        return "-"
    valor = str(valor).strip()
    return valor if valor else "-"


def _formatar_materiais(valor: str) -> str:
    valor = _normalizar_vazio(valor)

    if valor == "-":
        return valor

    valor = re.sub(r"\s+", " ", valor).strip()
    matches = list(re.finditer(r"(\d+)\s+([^0-9]+?)(?=(\s+\d+\s+)|$)", valor))

    if matches:
        linhas = []
        for m in matches:
            qtd = m.group(1).strip()
            desc = m.group(2).strip()
            if desc:
                linhas.append(f"{qtd} {desc}")
        if linhas:
            return "\n".join(linhas)

    return valor


def _formatar_speed(valor: str) -> str:
    valor = _normalizar_vazio(valor)
    if valor == "-":
        return valor
    valor_limpo = valor.lower().replace("mbps", "").strip()
    return f"{valor_limpo} Mbps"


def _formatar_sinal(valor: str) -> str:
    valor = _normalizar_vazio(valor)
    if valor == "-":
        return valor

    valor_limpo = valor.lower().replace("dbm", "").replace("dBm", "").strip()
    if not valor_limpo.startswith("-"):
        valor_limpo = f"-{valor_limpo}"

    return f"{valor_limpo} dBm"


def _formatar_valor(campo_id: str, valor) -> str:
    valor = _normalizar_vazio(valor)

    if campo_id in {"materiais_utilizados", "materiais_retirados"}:
        return _formatar_materiais(valor)

    if campo_id == "teste_velocidade":
        return _formatar_speed(valor)

    if campo_id in {"sinal_fibra", "sinal_cto"}:
        return _formatar_sinal(valor)

    return valor


def _calcular_tempo(inicio: str, fim: str) -> str:
    try:
        h1 = datetime.strptime(inicio, "%H:%M")
        h2 = datetime.strptime(fim, "%H:%M")
        delta = h2 - h1
        total_min = int(delta.total_seconds() // 60)
        if total_min < 0:
            return "-"
        horas = total_min // 60
        minutos = total_min % 60
        return f"{horas} h {minutos} min"
    except Exception:
        return "-"


def montar_relatorio(dados: dict) -> str:
    tipo = dados.get("tipo_v5") or dados.get("tipo") or "Atendimento"
    modelo = MODELOS_ATENDIMENTO.get(tipo)

    tempo_gasto = _calcular_tempo(dados.get("inicio", "-"), dados.get("fim", "-"))

    linhas = [
        "🔧 <b>Relatório de Atendimento</b>",
        "",
        f"<b>O.S.:</b> {dados.get('os', '-')}",
        f"<b>Tipo:</b> {tipo}",
        f"<b>Hora iniciada:</b> {dados.get('inicio', '-')}",
        f"<b>Hora finalizada:</b> {dados.get('fim', '-')}",
        f"<b>Tempo gasto:</b> {tempo_gasto}",
        f"<b>Técnico externo:</b> {dados.get('tec_ext', '-')}",
        f"<b>Técnico interno:</b> {dados.get('tec_int', '-')}",
        "",
    ]

    if not modelo:
        linhas.append("Modelo não encontrado.")
        return "\n".join(linhas)

    for secao in modelo["secoes"]:
        linhas.append(f"<b>{secao['titulo']}</b>")
        linhas.append("")

        for campo in secao["campos"]:
            if not _campo_deve_aparecer(campo, dados):
                continue

            valor = _formatar_valor(campo["id"], dados.get(campo["id"], "-"))

            linhas.append(f"{campo['item']} - {campo['titulo']}:")
            linhas.append(f"{valor}")
            linhas.append("")

    return "\n".join(linhas).strip()