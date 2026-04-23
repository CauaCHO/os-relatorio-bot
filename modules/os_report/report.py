from modules.os_report.modelos import MODELOS_ATENDIMENTO
import re


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
    """
    Tenta quebrar materiais em linhas quando encontrar padrão:
    número + descrição
    Ex:
    '1 roteador 2 conector apc 8 abraçadeira'
    =>
    1 roteador
    2 conector apc
    8 abraçadeira
    """
    valor = _normalizar_vazio(valor)

    if valor == "-":
        return valor

    # limpa espaços duplicados
    valor = re.sub(r"\s+", " ", valor).strip()

    # encontra blocos começando por número
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


def _formatar_valor(campo_id: str, valor) -> str:
    valor = _normalizar_vazio(valor)

    if campo_id in {"materiais_utilizados", "material_linkado"}:
        return valor

    if campo_id in {"materiais_retirados"}:
        return _formatar_materiais(valor)

    if campo_id in {"materiais_utilizados"}:
        return _formatar_materiais(valor)

    return valor


def montar_relatorio(dados: dict) -> str:
    tipo = dados.get("tipo_v5") or dados.get("tipo") or "Atendimento"
    modelo = MODELOS_ATENDIMENTO.get(tipo)

    linhas = [
        "🔧 <b>Relatório de Atendimento</b>",
        "",
        f"<b>O.S.:</b> {dados.get('os', '-')}",
        f"<b>Tipo:</b> {tipo}",
        f"<b>Hora iniciada:</b> {dados.get('inicio', '-')}",
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

            # resposta sempre embaixo da pergunta
            linhas.append(f"{campo['item']} - {campo['titulo']}:")
            linhas.append(f"{valor}")
            linhas.append("")

    return "\n".join(linhas).strip()