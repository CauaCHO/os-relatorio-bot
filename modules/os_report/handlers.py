from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from config import CHAT_ID
from core.helpers import validar_os, validar_hora, normalizar_sinal
from core.text_processor import processar_texto, languagetool_ativo
from core.storage import (
    salvar_historico,
    salvar_tecnico_usuario,
    obter_tecnico_usuario,
    obter_pendencia,
    remover_pendencia,
)
from core.config_store import get_tecnicos, get_roteadores, get_locais_instalacao
from shared.commands import ajuda_texto, status_texto
from shared.keyboards import (
    build_inline_keyboard,
    SIM_NAO_OPCOES,
    SIM_NAO_MAP,
    ENERGIA_OPCOES,
    ENERGIA_MAP,
    CANAIS_24_OPCOES,
    CANAIS_5_OPCOES,
    CONFIRMACAO_ENVIO_OPCOES,
    REINICIAR_FLUXO_OPCOES,
    GERAR_RETIRADA_OPCOES,
    REMOVER_PENDENCIA_OPCOES,
    ATENDIMENTO_V5_TIPOS_MAP,
)
from modules.os_report.modelos import MODELOS_ATENDIMENTO
from modules.os_report.report import montar_relatorio
from modules.material_delivery.handlers import iniciar_fluxo_retirada_prefill

usuarios = {}


def _tecnicos_options():
    itens = get_tecnicos()
    return [(str(i), nome) for i, nome in enumerate(itens)]


def _tecnicos_map():
    itens = get_tecnicos()
    return {str(i): nome for i, nome in enumerate(itens)}


def _roteadores_options():
    itens = get_roteadores()
    if "Outros" not in itens and "Outro" not in itens:
        itens = itens + ["Outros"]
    return [(str(i), nome) for i, nome in enumerate(itens)]


def _roteadores_map():
    itens = [x for _, x in _roteadores_options()]
    return {str(i): nome for i, nome in enumerate(itens)}


def _locais_options():
    itens = get_locais_instalacao()
    return [(str(i), nome) for i, nome in enumerate(itens)]


def _locais_map():
    itens = get_locais_instalacao()
    return {str(i): nome for i, nome in enumerate(itens)}


def montar_cabecalho_grupo(user) -> str:
    username = f"@{user.username}" if user.username else None
    nome = " ".join(x for x in [user.first_name, user.last_name] if x).strip()
    identificacao = username or nome or str(user.id)
    return f"👤 <b>Preenchido por:</b> {identificacao}\n\n"


async def enviar_grupo_longo(context: ContextTypes.DEFAULT_TYPE, texto: str, user):
    texto = montar_cabecalho_grupo(user) + texto
    partes = [texto[i:i + 4000] for i in range(0, len(texto), 4000)]
    for parte in partes:
        await context.bot.send_message(chat_id=CHAT_ID, text=parte, parse_mode="HTML")


def _todos_campos_modelo(tipo_v5: str):
    modelo = MODELOS_ATENDIMENTO[tipo_v5]
    campos = []
    for secao in modelo["secoes"]:
        campos.extend(secao["campos"])
    return campos


def _campo_deve_aparecer(campo: dict, dados: dict) -> bool:
    cond = campo.get("condicao")
    if not cond:
        return True
    return dados.get(cond["campo"]) == cond["valor"]


def _mapa_opcoes(campo: dict):
    tipo = campo["tipo"]

    if tipo == "sim_nao":
        return SIM_NAO_OPCOES, SIM_NAO_MAP
    if tipo == "tecnico":
        return _tecnicos_options(), _tecnicos_map()
    if tipo == "energia":
        return ENERGIA_OPCOES, ENERGIA_MAP
    if tipo == "canal24":
        return CANAIS_24_OPCOES, None
    if tipo == "canal5":
        return CANAIS_5_OPCOES, None
    if tipo == "roteador_sugestao":
        return _roteadores_options(), _roteadores_map()
    if tipo == "local_sugestao":
        return _locais_options(), _locais_map()

    return None, None


def _pre_campos():
    return [
        {"id": "os", "titulo": "Número da O.S.", "tipo": "os"},
        {"id": "inicio", "titulo": "Hora iniciada", "tipo": "hora"},
        {"id": "fim", "titulo": "Hora finalizada", "tipo": "hora"},
        {"id": "tec_ext", "titulo": "Técnico externo", "tipo": "tecnico"},
        {"id": "tec_int", "titulo": "Técnico interno", "tipo": "tecnico"},
    ]


def _todos_campos_fluxo(tipo_v5: str, dados: dict):
    return _pre_campos() + [c for c in _todos_campos_modelo(tipo_v5) if _campo_deve_aparecer(c, dados)]


async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(ajuda_texto(), parse_mode="HTML")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fluxo_ativo = update.effective_user.id in usuarios
    step = usuarios.get(update.effective_user.id, {}).get("step")
    await update.effective_message.reply_text(
        status_texto(fluxo_ativo, step, languagetool_ativo(), "Módulo de Atendimento"),
        parse_mode="HTML"
    )


async def _solicitar_reinicio(update: Update):
    await update.effective_message.reply_text(
        "⚠️ Você já possui um relatório de atendimento em andamento.\n\nDeseja cancelar o fluxo atual e iniciar um novo?",
        reply_markup=build_inline_keyboard("reiniciar_fluxo", REINICIAR_FLUXO_OPCOES)
    )


async def iniciar_fluxo_tipo_v5(update: Update, context: ContextTypes.DEFAULT_TYPE, tipo_codigo: str):
    if update.effective_chat.type != "private":
        return

    if update.effective_user.id in usuarios:
        usuarios[update.effective_user.id]["pending_start"] = tipo_codigo
        await _solicitar_reinicio(update)
        return

    tipo_nome = ATENDIMENTO_V5_TIPOS_MAP.get(tipo_codigo, "Atendimento")
    usuarios[update.effective_user.id] = {
        "step": "campo",
        "pending_start": None,
        "editando": False,
        "dados": {
            "tipo_v5": tipo_nome,
            "tipo": tipo_nome,
        },
        "campo_atual": "os",
    }

    await perguntar(update.effective_message, usuarios[update.effective_user.id])


async def atendimento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Use /start e selecione o tipo de atendimento pelo menu visual.")


async def assistencia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await iniciar_fluxo_tipo_v5(update, context, "fibra_assistencia")


async def instalacao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await iniciar_fluxo_tipo_v5(update, context, "fibra_instalacao")


async def mudanca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await iniciar_fluxo_tipo_v5(update, context, "fibra_instalacao")


async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios.pop(update.effective_user.id, None)
    await update.effective_message.reply_text("❌ Atendimento cancelado.", reply_markup=ReplyKeyboardRemove())


def _pergunta_campo(campo: dict) -> str:
    custom = {
        "os": "📌 Digite o número da O.S.:",
        "inicio": "⏰ Que horas você começou o serviço?\nExemplo: 15:30",
        "fim": "⏰ Que horas você finalizou o serviço?\nExemplo: 18:53",
        "tec_ext": "👨‍🔧 Quem foi o técnico externo?",
        "tec_int": "🧑‍💻 Quem foi o técnico interno?",
        "cabo_wifi": "🔌 Quais equipamentos estavam no cabo e quais estavam no Wi-Fi?",
        "local_instalacao": "📍 Onde os equipamentos ficaram instalados?",
        "mapeamento_wifi": "📶 Você fez o mapeamento do local pelo WiFiman?",
        "iptv_tvbox": "📺 O cliente tem IPTV ou TV Box?",
        "dados_antena": "📡 Informe alinhamento, sinal e TX/RX da antena:",
        "sinal_fibra": "📉 Qual foi o sinal da fibra?",
        "sinal_cto": "📡 Qual foi o sinal da CTO?",
        "houve_dano": "⚠️ Houve dano no local?",
        "descricao_dano": "✍️ Descreva o dano encontrado:",
        "orientacao_24_5": "📡 Você orientou o cliente sobre 2.4Ghz e 5.8Ghz?",
        "teste_realizado": "🚀 Você fez o teste de velocidade?",
        "teste_velocidade": "🚀 Qual foi o valor do speedtest?",
        "verificou_melhor_canal": "📶 Você verificou o melhor canal do Wi-Fi?",
        "config_padrao": "⚙️ Ficou tudo dentro do padrão da empresa?",
        "acesso_remoto": "🧩 Você verificou o acesso remoto?",
        "equipamentos_atualizados": "🔄 ONU e roteador estão atualizados?",
        "problema_procedimento": "🛠️ Qual era o problema e o que foi feito no local?",
        "fixacao": "🔩 Como os equipamentos ficaram fixados?",
        "energia": "🔌 Em que os equipamentos ficaram ligados?",
        "organizacao": "🧹 A instalação ficou organizada no padrão?",
        "pos_venda": "🤝 Foi feito o pós-venda imediato?",
        "motivo_sem_pos_venda": "✍️ Por que o pós-venda não foi feito?",
        "retirada_cabo_antigo": "🧵 Em mudança de endereço, o cabo antigo foi retirado? Se quiser, detalhe aqui.",
        "modelo_segundo_roteador": "📡 Qual foi o modelo do roteador do segundo ponto?",
        "ssid_segundo_roteador": "📶 Qual ficou sendo o nome da rede (SSID)?",
        "senha_segundo_roteador": "🔒 Qual ficou sendo a senha?",
        "passagem_cabo": "🔌 Houve passagem de cabo com testes?",
        "compatibilidade_roteador": "📡 Qual modelo do roteador e ele é compatível com o plano?",
        "motivo_link_loss": "🚨 Qual foi o motivo do Link Loss e como resolveu?",
        "mapeamento_primeiro_segundo": "📶 Foi feito o mapeamento do primeiro e do segundo ponto?",
        "materiais_utilizados": "📦 Digite os materiais utilizados:",
        "materiais_retirados": "📤 Digite os materiais retirados:",
        "material_linkado": "🔗 O material foi linkado no MK?",
    }
    return custom.get(campo["id"], f"✍️ {campo.get('titulo', 'Informe o campo')}:")


async def perguntar(message, estado: dict):
    dados = estado["dados"]
    tipo_v5 = dados["tipo_v5"]

    if estado["step"] == "remover_pendencia":
        await message.reply_text(
            "⚠️ Esta O.S. está em Pendências. Deseja remover da lista e continuar?",
            reply_markup=build_inline_keyboard("remover_pendencia", REMOVER_PENDENCIA_OPCOES)
        )
        return

    if estado["step"] == "confirmar":
        resumo = [
            "📋 <b>Resumo antes do envio</b>",
            "",
            f"<b>O.S.:</b> {dados.get('os', '-')}",
            f"<b>Tipo:</b> {dados.get('tipo_v5', '-')}",
            f"<b>Hora inicial:</b> {dados.get('inicio', '-')}",
            f"<b>Hora final:</b> {dados.get('fim', '-')}",
            f"<b>Técnico externo:</b> {dados.get('tec_ext', '-')}",
            f"<b>Técnico interno:</b> {dados.get('tec_int', '-')}",
            "",
            "📨 Escolha uma opção:",
        ]
        await message.reply_text("\n".join(resumo), parse_mode="HTML")
        await message.reply_text(
            "✅ Enviar\n✏️ Editar etapa específica\n❌ Cancelar",
            reply_markup=build_inline_keyboard("confirmar", CONFIRMACAO_ENVIO_OPCOES)
        )
        return

    if estado["step"] == "editar":
        opcoes = []
        for campo in _todos_campos_fluxo(tipo_v5, dados):
            titulo = campo.get("titulo", campo["id"])
            opcoes.append((campo["id"], titulo[:55]))
        await message.reply_text(
            "✏️ Selecione a etapa que deseja editar:",
            reply_markup=build_inline_keyboard("edit_os", opcoes, per_row=1)
        )
        return

    if estado["step"] == "perguntar_retirada":
        await message.reply_text(
            "📦 Foram informados materiais utilizados ou retirados.\nDeseja gerar também o relatório de entrega no estoque?",
            reply_markup=build_inline_keyboard("gerar_retirada", GERAR_RETIRADA_OPCOES)
        )
        return

    campo_id = estado["campo_atual"]
    campo = next(c for c in _todos_campos_fluxo(tipo_v5, dados) if c["id"] == campo_id)

    opcoes, _ = _mapa_opcoes(campo)
    if opcoes:
        await message.reply_text(
            _pergunta_campo(campo),
            reply_markup=build_inline_keyboard("resp", opcoes, per_row=2)
        )
    else:
        await message.reply_text(
            _pergunta_campo(campo),
            reply_markup=ReplyKeyboardRemove()
        )


def _proximo_campo(estado: dict):
    dados = estado["dados"]
    tipo_v5 = dados["tipo_v5"]
    campos = _todos_campos_fluxo(tipo_v5, dados)
    atual = estado["campo_atual"]
    ids = [c["id"] for c in campos]
    idx = ids.index(atual)

    if estado.get("editando"):
        estado["editando"] = False
        estado["step"] = "confirmar"
        return

    if idx + 1 < len(ids):
        estado["campo_atual"] = ids[idx + 1]
        estado["step"] = "campo"
    else:
        estado["step"] = "confirmar"


def _salvar_valor_campo(estado: dict, campo: dict, valor_bruto: str, valor_convertido: str | None = None):
    valor = valor_convertido if valor_convertido is not None else valor_bruto

    if campo["tipo"] == "texto":
        estado["dados"][campo["id"]] = processar_texto(valor or "-", "observacao")
    else:
        estado["dados"][campo["id"]] = valor or "-"


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query or query.message.chat.type != "private":
        return
    await query.answer()

    user_id = query.from_user.id
    if user_id not in usuarios:
        return

    estado = usuarios[user_id]
    dados = estado["dados"]
    tipo_v5 = dados["tipo_v5"]

    try:
        field, code = query.data.split("|", 1)
    except ValueError:
        return

    if field == "reiniciar_fluxo":
        pending = estado.get("pending_start")
        if code == "reiniciar_sim":
            usuarios.pop(user_id, None)
            if pending:
                await iniciar_fluxo_tipo_v5(update, context, pending)
                return
            await query.message.reply_text("Fluxo reiniciado.")
        else:
            await query.message.reply_text("👍 Fluxo atual mantido.")
        return

    if field == "remover_pendencia":
        if code == "sim":
            remover_pendencia(estado.get("os_pendente"))
        estado["step"] = "campo"
        estado["campo_atual"] = "inicio"
        await perguntar(query.message, estado)
        return

    if field == "confirmar":
        if code == "enviar":
            relatorio = montar_relatorio(dados)
            await enviar_grupo_longo(context, relatorio, query.from_user)
            salvar_historico(dados, relatorio, "Atendimento")

            materiais_utilizados = (dados.get("materiais_utilizados") or "-").strip()
            materiais_retirados = (dados.get("materiais_retirados") or "-").strip()

            if materiais_utilizados != "-" or materiais_retirados != "-":
                estado["step"] = "perguntar_retirada"
                await query.message.reply_text(
                    "✅ Relatório enviado com sucesso.\n\n"
                    f"📋 O.S.: {dados.get('os', '-')}\n"
                    f"🔧 Tipo: {dados.get('tipo_v5', '-')}\n"
                    f"👤 Técnico: {dados.get('tec_ext', '-')}"
                )
                await perguntar(query.message, estado)
                return

            usuarios.pop(user_id, None)
            await query.message.reply_text(
                "✅ Relatório enviado com sucesso.\n\n"
                f"📋 O.S.: {dados.get('os', '-')}\n"
                f"🔧 Tipo: {dados.get('tipo_v5', '-')}\n"
                f"👤 Técnico: {dados.get('tec_ext', '-')}",
                reply_markup=ReplyKeyboardRemove()
            )
            return

        if code == "editar":
            estado["step"] = "editar"
            await perguntar(query.message, estado)
            return

        usuarios.pop(user_id, None)
        await query.message.reply_text("❌ Fluxo cancelado.", reply_markup=ReplyKeyboardRemove())
        return

    if field == "edit_os":
        estado["campo_atual"] = code
        estado["step"] = "campo"
        estado["editando"] = True
        await perguntar(query.message, estado)
        return

    if field == "gerar_retirada":
        os_numero = dados.get("os", "-")
        usuarios.pop(user_id, None)
        if code == "sim":
            iniciar_fluxo_retirada_prefill(user_id, os_numero)
            await query.message.reply_text(
                f"🏢 Iniciando relatório de entrega no estoque para a O.S. {os_numero}.",
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await query.message.reply_text("👍 Fluxo finalizado.", reply_markup=ReplyKeyboardRemove())
        return

    if field == "resp":
        campo_id = estado["campo_atual"]
        campo = next(c for c in _todos_campos_fluxo(tipo_v5, dados) if c["id"] == campo_id)
        _, mapa = _mapa_opcoes(campo)

        if campo["tipo"] == "sim_nao":
            valor = SIM_NAO_MAP.get(code, code)
        elif campo["tipo"] == "tecnico":
            valor = _tecnicos_map().get(code, code)
        elif campo["tipo"] == "energia":
            valor = ENERGIA_MAP.get(code, code)
        elif campo["tipo"] == "roteador_sugestao":
            valor = _roteadores_map().get(code, code)
            if valor.lower().startswith("outro"):
                estado["step"] = "campo_texto"
                await query.message.reply_text("✍️ Digite manualmente o modelo do roteador:")
                return
        elif campo["tipo"] == "local_sugestao":
            valor = _locais_map().get(code, code)
            if valor.lower().startswith("outro"):
                estado["step"] = "campo_texto"
                await query.message.reply_text("✍️ Digite manualmente o local da instalação:")
                return
        else:
            valor = mapa.get(code, code) if mapa else code

        _salvar_valor_campo(estado, campo, code, valor)

        if campo["id"] == "tec_ext":
            salvar_tecnico_usuario(user_id, valor)

        _proximo_campo(estado)

        try:
            await query.edit_message_reply_markup(reply_markup=None)
        except Exception:
            pass

        await perguntar(query.message, estado)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    user_id = update.effective_user.id
    if user_id not in usuarios:
        return

    estado = usuarios[user_id]
    dados = estado["dados"]
    tipo_v5 = dados["tipo_v5"]
    texto = update.effective_message.text.strip()

    if estado["step"] == "campo_texto":
        campo_id = estado["campo_atual"]
        campo = next(c for c in _todos_campos_fluxo(tipo_v5, dados) if c["id"] == campo_id)
        _salvar_valor_campo(estado, campo, texto)
        estado["step"] = "campo"
        _proximo_campo(estado)
        await perguntar(update.effective_message, estado)
        return

    if estado["step"] != "campo":
        return

    campo_id = estado["campo_atual"]
    campo = next(c for c in _todos_campos_fluxo(tipo_v5, dados) if c["id"] == campo_id)

    if campo["tipo"] == "os":
        if not validar_os(texto):
            await update.effective_message.reply_text("⚠️ Número de O.S. inválido. Digite apenas números.")
            return

        dados["os"] = texto
        pendencia = obter_pendencia(texto)
        if pendencia:
            estado["os_pendente"] = texto
            estado["step"] = "remover_pendencia"
            await perguntar(update.effective_message, estado)
            return

        _proximo_campo(estado)
        await perguntar(update.effective_message, estado)
        return

    if campo["tipo"] == "hora":
        if not validar_hora(texto):
            await update.effective_message.reply_text("⚠️ Hora inválida. Use o formato HH:MM.")
            return

        dados[campo["id"]] = texto

        if campo["id"] == "inicio":
            tecnico_padrao = obter_tecnico_usuario(user_id)
            if tecnico_padrao and not estado.get("editando"):
                dados["tec_ext"] = tecnico_padrao
                estado["campo_atual"] = "tec_int"
                estado["step"] = "campo"
                await perguntar(update.effective_message, estado)
                return

        _proximo_campo(estado)
        await perguntar(update.effective_message, estado)
        return

    if campo["tipo"] == "sinal":
        valor = normalizar_sinal(texto)
        if valor is None:
            await update.effective_message.reply_text("⚠️ Digite um valor válido. Exemplo: 17.22 ou apenas -")
            return

        _salvar_valor_campo(estado, campo, texto, valor)
        _proximo_campo(estado)
        await perguntar(update.effective_message, estado)
        return

    if campo["tipo"] == "speed":
        texto_limpo = texto.lower().replace("mbps", "").strip()
        try:
            float(texto_limpo.replace(",", "."))
        except ValueError:
            await update.effective_message.reply_text("⚠️ Digite apenas o valor do speedtest. Exemplo: 250")
            return

        _salvar_valor_campo(estado, campo, texto, texto_limpo)
        _proximo_campo(estado)
        await perguntar(update.effective_message, estado)
        return

    _salvar_valor_campo(estado, campo, texto)
    _proximo_campo(estado)
    await perguntar(update.effective_message, estado)