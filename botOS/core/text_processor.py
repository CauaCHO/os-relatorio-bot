import re

tool = None
try:
    import language_tool_python
    tool = language_tool_python.LanguageTool("pt-BR")
    print("✅ LanguageTool inicializado com sucesso.")
except Exception as e:
    tool = None
    print(f"⚠️ LanguageTool não disponível. Fallback local ativo. Motivo: {e}")


ABREVIACOES_COMUNS = {
    r"\bq\b": "que",
    r"\bpq\b": "porque",
    r"\bvc\b": "você",
    r"\bta\b": "está",
    r"\btava\b": "estava",
    r"\bnet\b": "internet",
}

TERMOS_TECNICOS = {
    r"\bwifi\b": "Wi-Fi",
    r"\bwi-fi\b": "Wi-Fi",
    r"\biptv\b": "IPTV",
    r"\btvbox\b": "TVBOX",
    r"\bonu\b": "ONU",
    r"\bdrop\b": "cabo drop",
    r"\bax3000\b": "AX3000",
    r"\bmercusys\b": "Mercusys",
    r"\broteador zte\b": "roteador ZTE",
    r"\bsmartv\b": "Smart TV",
}

SUBSTITUICOES_TECNICAS = {
    r"\btroquei o roteador\b": "Foi realizada a substituição do roteador",
    r"\bmudei o canal\b": "Foi realizado o ajuste de canal",
    r"\barrumei o cabo\b": "Foi realizado o reparo no cabeamento",
    r"\barrumei o drop\b": "Foi realizado o reparo no cabo drop",
    r"\bpassei outro cabo\b": "Foi realizada a substituição do cabeamento",
    r"\bpassei outro drop\b": "Foi realizada a substituição do cabo drop",
    r"\bficou bom\b": "o funcionamento foi normalizado",
    r"\bnormalizou\b": "o funcionamento foi normalizado",
    r"\bsem net\b": "sem conexão",
    r"\binternet ruim\b": "instabilidade na conexão",
}

SUGESTOES_SOLUCAO = {
    "Link Loss": (
        "Ao chegarmos ao local, foi verificada a ocorrência de Link Loss. "
        "Após análise técnica, foi realizado o procedimento necessário para restabelecimento do serviço, normalizando o sinal."
    ),
    "Mudança de plano": (
        "Ao chegarmos ao local, foi realizada a adequação dos equipamentos ao novo plano contratado. "
        "Após os ajustes e testes, o serviço ficou dentro do padrão."
    ),
    "Mudança de cômodo": (
        "Ao chegarmos ao local, foi realizada a mudança de cômodo dos equipamentos. "
        "Após reorganização e testes, o funcionamento foi normalizado."
    ),
    "Segundo ponto": (
        "Ao chegarmos ao local, foi realizado o procedimento referente ao segundo ponto. "
        "Após os testes, o funcionamento foi verificado."
    ),
    "Instabilidade": (
        "Ao chegarmos ao local, foi analisada a instabilidade relatada pelo cliente. "
        "Após o procedimento técnico, a conexão ficou dentro do padrão."
    ),
}


def _limpar_espacos(texto: str) -> str:
    texto = texto.replace("\n", " ")
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def _aplicar_substituicoes(texto: str, mapa: dict[str, str]) -> str:
    for padrao, substituicao in mapa.items():
        texto = re.sub(padrao, substituicao, texto, flags=re.IGNORECASE)
    return texto


def _capitalizar_inicio(texto: str) -> str:
    if not texto:
        return "-"
    return texto[0].upper() + texto[1:]


def _garantir_ponto_final(texto: str) -> str:
    if not texto:
        return "-"
    if texto[-1] not in ".!?":
        texto += "."
    return texto


def _quebrar_frases(texto: str) -> str:
    texto = re.sub(r"\s*,\s*", ", ", texto)
    texto = re.sub(r"\s*\.\s*", ". ", texto)
    texto = re.sub(r"\s*;\s*", "; ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def lapidar_texto_local(texto: str, modo: str = "observacao") -> str:
    if not texto or texto.strip() == "-":
        return "-"

    texto = _limpar_espacos(texto)
    texto = _aplicar_substituicoes(texto, ABREVIACOES_COMUNS)
    texto = _aplicar_substituicoes(texto, TERMOS_TECNICOS)

    if modo in {"solucao", "danos", "assinatura", "ausencia"}:
        texto = _aplicar_substituicoes(texto, SUBSTITUICOES_TECNICAS)

    texto = _quebrar_frases(texto)
    texto = _capitalizar_inicio(texto)
    texto = _garantir_ponto_final(texto)
    return texto


def corrigir_com_languagetool(texto: str):
    if not tool or texto == "-":
        return None

    try:
        matches = tool.check(texto)
        corrigido = texto
        if matches:
            import language_tool_python
            corrigido = language_tool_python.utils.correct(texto, matches)

        corrigido = _limpar_espacos(corrigido)
        corrigido = _capitalizar_inicio(corrigido)
        corrigido = _garantir_ponto_final(corrigido)
        return corrigido
    except Exception as e:
        print(f"⚠️ Falha no LanguageTool. Usando fallback local. Motivo: {e}")
        return None


def processar_texto(texto_bruto: str, modo: str = "observacao") -> str:
    texto_local = lapidar_texto_local(texto_bruto, modo)
    texto_lt = corrigir_com_languagetool(texto_local)
    return texto_lt if texto_lt else texto_local


def sugerir_solucao(problema: str) -> str:
    return SUGESTOES_SOLUCAO.get(problema, "-")


def languagetool_ativo() -> bool:
    return tool is not None