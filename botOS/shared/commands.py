def ajuda_texto() -> str:
    return (
        "📘 <b>Como usar o bot</b>\n\n"
        "Este bot é usado para gerar relatórios técnicos.\n\n"
        "<b>Comandos disponíveis:</b>\n"
        "/start - Inicia um novo relatório O.S.\n"
        "/assistencia - Inicia O.S. de assistência\n"
        "/instalacao - Inicia O.S. de instalação\n"
        "/mudanca - Inicia O.S. de mudança de endereço\n"
        "/retirada - Inicia retirada de equipamentos\n"
        "/ausencia - Inicia cliente ausente / O.S. paralisada\n"
        "/status - Status do módulo O.S.\n"
        "/status_material - Status do módulo de retirada\n"
        "/status_ausencia - Status do módulo de ausência\n"
        "/cancelar - Cancela O.S.\n"
        "/cancelar_material - Cancela retirada\n"
        "/cancelar_ausencia - Cancela ausência\n"
        "/ajuda - Mostra esta mensagem\n\n"
        "• O bot deve ser usado no privado\n"
        "• Ao final, o relatório é enviado ao grupo"
    )


def status_texto(fluxo_ativo: bool, step: str | None, languagetool_ativo: bool, modulo: str) -> str:
    return (
        f"✅ <b>{modulo} operacional</b>\n\n"
        f"🧠 <b>Correção textual:</b> {'LanguageTool ativo' if languagetool_ativo else 'Fallback local ativo'}\n"
        f"📝 <b>Fluxo em andamento:</b> {'Sim' if fluxo_ativo else 'Não'}\n"
        f"🔹 <b>Etapa atual:</b> {step if step else '-'}"
    )