from datetime import datetime
from core.helpers import escapar_html, valor_ou_traco, calcular_tempo_gasto, is_assistencia


def montar_relatorio(dados: dict) -> str:
    final = datetime.now().strftime("%H:%M")
    tempo_gasto = calcular_tempo_gasto(dados.get("inicio", ""), final)

    linhas = [
        f"<b>{escapar_html(valor_ou_traco(dados.get('tipo', '')).upper())}</b>",
        "",
        f"<b>O.S:</b> {escapar_html(valor_ou_traco(dados.get('os', '')))}",
        "",
        f"<b>Iniciada:</b> {escapar_html(valor_ou_traco(dados.get('inicio', '')))}",
        f"<b>Finalizada:</b> {escapar_html(final)}",
        f"<b>Tempo gasto:</b> {escapar_html(tempo_gasto)}",
        "",
        f"<b>Técnico externo:</b> {escapar_html(valor_ou_traco(dados.get('tec_ext', '')))}",
        f"<b>Técnico interno:</b> {escapar_html(valor_ou_traco(dados.get('tec_int', '')))}",
        "",
    ]

    if is_assistencia(dados.get("tipo", "")):
        linhas += [
            "<b>1.13 - O problema relatado é?:</b>",
            escapar_html(valor_ou_traco(dados.get("problema", ""))),
            "",
            "<b>1.13 - Para solucionar o problema foi feito:</b>",
            escapar_html(valor_ou_traco(dados.get("solucao", ""))),
            "",
        ]

    linhas += [
        "<b>Informações em fotos:</b>",
        "1.1 - Fotos dos equipamentos conectados via cabo de rede.",
        "1.1.1 - Fotos dos equipamentos conectados via Wi-fi.",
        "1.2 - Local da instalação dos equipamentos (foto de perto e de longe, mostrando todo o ambiente).",
        "1.3 - Mapeamento de todo o local pelo WiFiman.",
        "1.4 - Foto de dispositivos diversos (IPTV, TVBOX, DVR...).",
        "1.5 - Medição de sinal da Fibra.",
        "1.8 - Realização de teste de velocidade.",
        "1.9 - Verificação de melhor canal (Wifi Analyser) rede 2.4Ghz e 5.8Ghz.",
        "",
        "<b>Informações Descritas:</b>",
        "",
        "<b>Observações Relevantes:</b>",
        escapar_html(valor_ou_traco(dados.get("observacoes", ""))),
        "",
        "<b>1.1 - Quais equipamentos o cliente tem conectado no cabo:</b>",
        escapar_html(valor_ou_traco(dados.get("cabo", ""))),
        "",
        "<b>1.1.1 - Quais equipamentos o cliente tem conectado via Wi-fi?:</b>",
        escapar_html(valor_ou_traco(dados.get("wifi", ""))),
        "",
        "<b>1.2 - Qual o local da instalação dos equipamentos?:</b>",
        escapar_html(valor_ou_traco(dados.get("local", ""))),
        "",
        "<b>1.3 - Cliente necessita de um segundo ponto?:</b>",
        escapar_html(valor_ou_traco(dados.get("segundo_ponto", ""))),
        "",
        "<b>1.4 - Cliente possui IPTV/TVBOX?:</b>",
        escapar_html(valor_ou_traco(dados.get("iptv", ""))),
        "",
        "<b>1.5.1 - Qual o sinal da Fibra?:</b>",
        f"{escapar_html(valor_ou_traco(dados.get('sinal_fibra', '')))} dBm" if valor_ou_traco(dados.get("sinal_fibra", "")) != "-" else "-",
        "",
    ]

    sinal_cto = valor_ou_traco(dados.get("sinal_cto", ""))
    if dados.get("tipo") in {"Instalação", "Mudança de endereço"}:
        if sinal_cto == "-":
            linhas += [
                "<b>1.5.2 - Fibra Flash:</b>",
                "Sim",
                "",
            ]
        else:
            linhas += [
                "<b>1.5.2 - Qual o sinal da CTO?:</b>",
                f"{escapar_html(sinal_cto)} dBm",
                "",
            ]

    linhas += [
        "<b>1.6 - Houve danos no local?:</b>",
        escapar_html(valor_ou_traco(dados.get("danos", ""))),
        "",
    ]

    if valor_ou_traco(dados.get("danos", "")) == "Sim":
        linhas += [
            "<b>1.6.1 - Supervisor ciente do ocorrido?:</b>",
            escapar_html(valor_ou_traco(dados.get("supervisor_ciente", ""))),
            "",
            "<b>1.6.2 - Descrição do ocorrido:</b>",
            escapar_html(valor_ou_traco(dados.get("danos_descricao", ""))),
            "",
        ]

    linhas += [
        "<b>1.7 - Foi orientado o cliente sobre a rede 2.4Ghz e 5.8Ghz?:</b>",
        escapar_html(valor_ou_traco(dados.get("orientacao", ""))),
        "",
        "<b>1.8 - Teste de velocidade dentro do plano contratado?:</b>",
        escapar_html(valor_ou_traco(dados.get("velocidade", ""))),
        "",
        "<b>1.9.1 - Qual canal foi escolhido na rede 2.4Ghz?:</b>",
        escapar_html(valor_ou_traco(dados.get("canal24", ""))),
        "",
        "<b>1.9.2 - Qual canal foi escolhido na rede 5.8Ghz?:</b>",
        escapar_html(valor_ou_traco(dados.get("canal5", ""))),
        "",
    ]

    if dados.get("tipo") in {"Instalação", "Mudança de endereço"}:
        linhas += [
            "<b>1.10 - Qual a forma de fixação dos equipamentos (roteador e ONU)?:</b>",
            escapar_html(valor_ou_traco(dados.get("fixacao", ""))),
            "",
            "<b>1.11 e 1.12 - Padrões de configurações do roteador e acesso remoto habilitado?:</b>",
            escapar_html(valor_ou_traco(dados.get("config_padrao", ""))),
            "",
            "<b>1.13 - Feito pós venda imediato?:</b>",
            escapar_html(valor_ou_traco(dados.get("pos_venda", ""))),
            "",
        ]
    else:
        linhas += [
            "<b>1.10 - Padrões de configurações do roteador e acesso remoto habilitado?:</b>",
            escapar_html(valor_ou_traco(dados.get("config_padrao", ""))),
            "",
        ]

    linhas += [
        "<b>2.1 - Equipamentos ficaram ligados em?:</b>",
        escapar_html(valor_ou_traco(dados.get("energia", ""))),
        "",
        "<b>2.2 - Equipamentos foram organizados conforme nossos padrões?:</b>",
        escapar_html(valor_ou_traco(dados.get("organizacao", ""))),
        "",
        "<b>Assinatura do cliente:</b>",
        escapar_html(valor_ou_traco(dados.get("assinatura", ""))),
        "",
    ]

    if valor_ou_traco(dados.get("assinatura", "")) == "Não":
        linhas += [
            "<b>Motivo da ausência de assinatura:</b>",
            escapar_html(valor_ou_traco(dados.get("assinatura_motivo", ""))),
            "",
        ]

    linhas += [
        "<b>Materiais utilizados:</b>",
        escapar_html(valor_ou_traco(dados.get("materiais_utilizados", ""))),
        "",
        "<b>Materiais retirados:</b>",
        escapar_html(valor_ou_traco(dados.get("materiais_retirados", ""))),
    ]

    return "\n".join(linhas).strip()