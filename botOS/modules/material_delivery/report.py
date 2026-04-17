from core.helpers import escapar_html, valor_ou_traco


def montar_relatorio_material(dados: dict) -> str:
    equipamentos = []

    roteador = dados.get("roteador")
    if roteador and roteador != "-":
        equipamentos.append(f"1x {roteador} + fonte")

    onu = dados.get("onu")
    if onu and onu != "-":
        equipamentos.append(f"1x ONU {onu} + fonte")

    if dados.get("patchcord") == "Sim":
        equipamentos.append("1x PatchCord")

    outro = dados.get("outro")
    if outro and outro != "-":
        equipamentos.append(outro)

    lista_equipamentos = "\n".join(f"- {escapar_html(item)}" for item in equipamentos) or "-"

    return f"""
📦 <b>RETIRADA DE EQUIPAMENTOS</b>

<b>O.S.:</b> {escapar_html(valor_ou_traco(dados.get("os")))}
<b>Tipo:</b> Retirada ({escapar_html(valor_ou_traco(dados.get("tipo_retirada")))})

<b>Equipamentos retirados:</b>
{lista_equipamentos}

<b>Destino:</b> {escapar_html(valor_ou_traco(dados.get("destino")))}
<b>Recebido por:</b> {escapar_html(valor_ou_traco(dados.get("recebido_por")))}
<b>Cidade:</b> {escapar_html(valor_ou_traco(dados.get("cidade")))}
""".strip()