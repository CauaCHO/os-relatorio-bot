from modules.os_report.modelos import MODELOS_ATENDIMENTO


def _campo_deve_aparecer(campo: dict, dados: dict) -> bool:
    cond = campo.get("condicao")
    if not cond:
        return True
    return dados.get(cond["campo"]) == cond["valor"]


def montar_relatorio(dados: dict) -> str:
    tipo = dados.get("tipo_v5") or dados.get("tipo") or "Atendimento"
    modelo = MODELOS_ATENDIMENTO.get(tipo)

    linhas = [
        f"🔧 <b>Relatório de Atendimento</b>",
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
            valor = dados.get(campo["id"], "-")
            linhas.append(f"{campo['item']} - {campo['titulo']}: {valor}")
        linhas.append("")

    return "\n".join(linhas).strip()