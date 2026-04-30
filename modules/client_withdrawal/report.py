from core.helpers import escapar_html, valor_ou_traco


def montar_relatorio_retirada_cliente(dados: dict) -> str:
    equipamentos = dados.get("equipamentos", "-")

    return f"""
📦 <b>RETIRADA DE EQUIPAMENTOS DA CASA DO CLIENTE</b>

<b>O.S.:</b> {escapar_html(valor_ou_traco(dados.get("os")))}

<b>Equipamentos retirados:</b>
{escapar_html(valor_ou_traco(equipamentos))}

@FlashNetNegociacoesCobranca
""".strip()
