from core.helpers import escapar_html, valor_ou_traco

def montar_relatorio_ausencia(dados: dict) -> str:
    return f"""
📄 <b>CLIENTE AUSENTE / O.S. PARALISADA</b>

<b>O.S.:</b> {escapar_html(valor_ou_traco(dados.get("os")))}
<b>Ocorrência:</b> {escapar_html(valor_ou_traco(dados.get("ocorrencia")))}

{escapar_html(valor_ou_traco(dados.get("texto")))}
""".strip()