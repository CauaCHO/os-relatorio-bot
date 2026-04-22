def ajuda_texto() -> str:
    return (
        "🚀 <b>Sistema Flash Reports</b>\n\n"
        "<b>Comandos disponíveis:</b>\n"
        "/start - Abre o menu principal\n"
        "/atendimento - Inicia relatório de atendimento\n"
        "/estoque - Inicia relatório de entrega no estoque\n"
        "/retirada - Módulo de retirada\n"
        "/ausente - Inicia relatório de cliente ausente\n"
        "/paralisada - Inicia relatório de O.S. paralisada\n"
        "/pendencias - Lista O.S. paralisadas\n"
        "/status - Status do módulo de atendimento\n"
        "/status_material - Status do módulo estoque\n"
        "/status_ausencia - Status do módulo ausente/paralisada\n"
        "/cancelar - Cancela atendimento\n"
        "/cancelar_material - Cancela estoque\n"
        "/cancelar_ausencia - Cancela ausente/paralisada\n"
        "/ajuda - Mostra esta mensagem\n\n"
        "• Use o bot no privado\n"
        "• Os relatórios são enviados automaticamente ao grupo\n"
        "• O grupo é usado apenas para acompanhamento dos supervisores"
    )


def status_texto(fluxo_ativo: bool, step: str | None, languagetool_ativo: bool, modulo: str) -> str:
    return (
        f"✅ <b>{modulo} operacional</b>\n\n"
        f"🧠 <b>Correção textual:</b> {'LanguageTool ativo' if languagetool_ativo else 'Fallback local ativo'}\n"
        f"📝 <b>Fluxo em andamento:</b> {'Sim' if fluxo_ativo else 'Não'}\n"
        f"🔹 <b>Etapa atual:</b> {step if step else '-'}"
    )


def pendencias_texto(pendencias) -> str:
    if not pendencias:
        return "📋 <b>Pendências</b>\n\nNenhuma O.S. paralisada no momento."

    linhas = ["📋 <b>Pendências</b>", ""]

    # caso venha lista
    if isinstance(pendencias, list):
        for i, item in enumerate(pendencias, start=1):
            linhas.append(f"{i}️⃣ <b>O.S. {item.get('os', '-')}</b>")
            linhas.append(f"Motivo: {item.get('motivo', '-')}")
            linhas.append(f"Registrado por: {item.get('usuario', '-')}")
            linhas.append(f"Data: {item.get('data', '-')}")
            linhas.append("")
        linhas.append(f"Total: {len(pendencias)} O.S.")
        return "\n".join(linhas)

    # caso venha dict
    if isinstance(pendencias, dict):
        for i, (os_numero, dados) in enumerate(pendencias.items(), start=1):
            linhas.append(f"{i}️⃣ <b>O.S. {os_numero}</b>")
            linhas.append(f"Motivo: {dados.get('motivo', '-')}")
            linhas.append(f"Registrado por: {dados.get('usuario', '-')}")
            linhas.append(f"Data: {dados.get('data_hora', '-')}")
            linhas.append("")
        linhas.append(f"Total: {len(pendencias)} O.S.")
        return "\n".join(linhas)

    return "📋 <b>Pendências</b>\n\nNenhuma O.S. paralisada no momento."