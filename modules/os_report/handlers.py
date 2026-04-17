from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from config import CHAT_ID
from core.helpers import validar_os, validar_hora, normalizar_sinal, is_assistencia
from core.text_processor import processar_texto, sugerir_solucao, languagetool_ativo
from core.storage import salvar_historico, salvar_tecnico_usuario, obter_tecnico_usuario
from shared.commands import ajuda_texto, status_texto
from shared.keyboards import (
    build_inline_keyboard,
    TIPOS_OPCOES, TECNICOS_OPCOES, SIM_NAO_OPCOES, PROBLEMAS_OPCOES,
    ENERGIA_OPCOES, CANAIS_24_OPCOES, CANAIS_5_OPCOES, CONFIRMACAO_ENVIO_OPCOES,
    REINICIAR_FLUXO_OPCOES, GERAR_RETIRADA_OPCOES,
    TIPOS_MAP, TECNICOS_MAP, SIM_NAO_MAP, PROBLEMAS_MAP, ENERGIA_MAP
)
from modules.os_report.report import montar_relatorio
from modules.material_delivery.handlers import iniciar_fluxo_retirada_prefill

usuarios = {}

EDIT_MAP_OS = {
    "os": "os",
    "inicio": "inicio",
    "tec_ext": "tec_ext",
    "tec_int": "tec_int",
    "problema": "problema",
    "solucao": "solucao",
    "observacoes": "observacoes",
    "cabo": "cabo",
    "wifi": "wifi",
    "local": "local",
    "segundo_ponto": "segundo_ponto",
    "iptv": "iptv",
    "sinal_fibra": "sinal_fibra",
    "sinal_cto": "sinal_cto",
    "danos": "danos",
    "orientacao": "orientacao",
    "velocidade": "velocidade",
    "canal24": "canal24",
    "canal5": "canal5",
    "fixacao": "fixacao",
    "config_padrao": "config_padrao",
    "pos_venda": "pos_venda",
    "energia": "energia",
    "organizacao": "organizacao",
    "assinatura": "assinatura",
    "materiais_utilizados": "materiais_utilizados",
    "materiais_retirados": "materiais_retirados",
}

EDITAR_OS_OPCOES = [
    ("os", "O.S."),
    ("inicio", "Hora iniciada"),
    ("tec_ext", "Técnico externo"),
    ("tec_int", "Técnico interno"),
    ("problema", "Problema"),
    ("solucao", "Solução"),
    ("observacoes", "Observações"),
    ("cabo", "Equipamentos no cabo"),
    ("wifi", "Equipamentos no Wi-Fi"),
    ("local", "Local"),
    ("segundo_ponto", "Segundo ponto"),
    ("iptv", "IPTV/TVBOX"),
    ("sinal_fibra", "Sinal da fibra"),
    ("sinal_cto", "Sinal da CTO"),
    ("danos", "Danos no local"),
    ("orientacao", "Orientação 2.4/5.8"),
    ("velocidade", "Teste de velocidade"),
    ("canal24", "Canal 2.4G"),
    ("canal5", "Canal 5G"),
    ("fixacao", "Fixação"),
    ("config_padrao", "Configuração padrão"),
    ("pos_venda", "Pós-venda"),
    ("energia", "Energia"),
    ("organizacao", "Organização"),
    ("assinatura", "Assinatura"),
    ("materiais_utilizados", "Materiais utilizados"),
    ("materiais_retirados", "Materiais retirados"),
]


async def enviar_texto_longo(message, texto: str):
    partes = [texto[i:i + 4000] for i in range(0, len(texto), 4000)]
    for parte in partes:
        await message.reply_text(parte, parse_mode="HTML")


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


async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ajuda_texto(), parse_mode="HTML")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fluxo_ativo = update.effective_user.id in usuarios
    step = usuarios.get(update.effective_user.id, {}).get("step")
    await update.message.reply_text(
        status_texto(fluxo_ativo, step, languagetool_ativo(), "Módulo de O.S."),
        parse_mode="HTML"
    )


async def _solicitar_reinicio(update: Update):
    await update.message.reply_text(
        "⚠️ Você já possui um relatório O.S. em andamento.\n\nDeseja cancelar o fluxo atual e iniciar um novo?",
        reply_markup=build_inline_keyboard("reiniciar_fluxo", REINICIAR_FLUXO_OPCOES)
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    if update.effective_user.id in usuarios:
        await _solicitar_reinicio(update)
        return

    usuarios[update.effective_user.id] = {"step": "os", "dados": {}, "pending_start": "normal"}
    await update.message.reply_text("👋 Vamos iniciar o relatório.\n\n📌 Digite o número da O.S.:", reply_markup=ReplyKeyboardRemove())


async def assistencia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    if update.effective_user.id in usuarios:
        usuarios[update.effective_user.id]["pending_start"] = "assistencia"
        await _solicitar_reinicio(update)
        return

    usuarios[update.effective_user.id] = {"step": "os", "dados": {"tipo": "Assistência"}, "pending_start": None}
    await update.message.reply_text("🛠️ Tipo definido: Assistência.\n\n📌 Digite o número da O.S.:", reply_markup=ReplyKeyboardRemove())


async def instalacao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    if update.effective_user.id in usuarios:
        usuarios[update.effective_user.id]["pending_start"] = "instalacao"
        await _solicitar_reinicio(update)
        return

    usuarios[update.effective_user.id] = {"step": "os", "dados": {"tipo": "Instalação"}, "pending_start": None}
    await update.message.reply_text("📡 Tipo definido: Instalação.\n\n📌 Digite o número da O.S.:", reply_markup=ReplyKeyboardRemove())


async def mudanca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    if update.effective_user.id in usuarios:
        usuarios[update.effective_user.id]["pending_start"] = "mudanca"
        await _solicitar_reinicio(update)
        return

    usuarios[update.effective_user.id] = {"step": "os", "dados": {"tipo": "Mudança de endereço"}, "pending_start": None}
    await update.message.reply_text("🏠 Tipo definido: Mudança de endereço.\n\n📌 Digite o número da O.S.:", reply_markup=ReplyKeyboardRemove())


async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios.pop(update.effective_user.id, None)
    await update.message.reply_text("❌ Atendimento cancelado.", reply_markup=ReplyKeyboardRemove())


async def perguntar(message, estado: dict):
    step = estado["step"]
    dados = estado["dados"]
    tipo = dados.get("tipo", "")

    if step == "tipo":
        await message.reply_text("📋 Selecione o tipo de atendimento:", reply_markup=build_inline_keyboard("tipo", TIPOS_OPCOES))
    elif step == "inicio":
        await message.reply_text("⏰ Digite a hora iniciada no formato HH:MM\nExemplo: 16:04", reply_markup=ReplyKeyboardRemove())
    elif step == "tec_ext":
        await message.reply_text("👨‍🔧 Selecione o técnico externo:", reply_markup=build_inline_keyboard("tec_ext", TECNICOS_OPCOES))
    elif step == "tec_int":
        await message.reply_text("🧑‍💻 Selecione o técnico interno:", reply_markup=build_inline_keyboard("tec_int", TECNICOS_OPCOES))
    elif step == "problema":
        if is_assistencia(tipo):
            await message.reply_text("🚨 Selecione o problema relatado:", reply_markup=build_inline_keyboard("problema", PROBLEMAS_OPCOES))
        else:
            estado["step"] = "observacoes"
            await perguntar(message, estado)
    elif step == "solucao":
        if is_assistencia(tipo):
            sugestao = sugerir_solucao(dados.get("problema", "-"))
            if sugestao and sugestao != "-":
                await message.reply_text(f"💡 Sugestão de apoio:\n{sugestao}")
            await message.reply_text("🛠️ Descreva o que foi feito para solucionar:", reply_markup=ReplyKeyboardRemove())
        else:
            estado["step"] = "observacoes"
            await perguntar(message, estado)
    elif step == "observacoes":
        await message.reply_text("📝 Observações relevantes (se não tiver, digite: -):", reply_markup=ReplyKeyboardRemove())
    elif step == "cabo":
        await message.reply_text("🔌 Quais equipamentos o cliente tem conectado no cabo?")
    elif step == "wifi":
        await message.reply_text("📶 Quais equipamentos o cliente tem conectado via Wi-Fi?")
    elif step == "local":
        await message.reply_text("📍 Qual o local da instalação dos equipamentos?")
    elif step == "segundo_ponto":
        await message.reply_text("➕ Cliente necessita de um segundo ponto?", reply_markup=build_inline_keyboard("segundo_ponto", SIM_NAO_OPCOES))
    elif step == "iptv":
        await message.reply_text("📺 Cliente possui IPTV/TVBOX?", reply_markup=build_inline_keyboard("iptv", SIM_NAO_OPCOES))
    elif step == "sinal_fibra":
        await message.reply_text("📉 Qual o sinal da Fibra?\nExemplo: 17.22", reply_markup=ReplyKeyboardRemove())
    elif step == "sinal_cto":
        if tipo in {"Instalação", "Mudança de endereço"}:
            await message.reply_text("📡 Qual o sinal da CTO?\nExemplo: 16.25\nSe for Fibra Flash, digite apenas -", reply_markup=ReplyKeyboardRemove())
        else:
            estado["step"] = "danos"
            await perguntar(message, estado)
    elif step == "danos":
        await message.reply_text("⚠️ Houve danos no local?", reply_markup=build_inline_keyboard("danos", SIM_NAO_OPCOES))
    elif step == "supervisor_ciente":
        await message.reply_text("👀 Supervisor ciente do ocorrido?", reply_markup=build_inline_keyboard("supervisor_ciente", SIM_NAO_OPCOES))
    elif step == "danos_descricao":
        await message.reply_text("✍️ Descreva o ocorrido:", reply_markup=ReplyKeyboardRemove())
    elif step == "orientacao":
        await message.reply_text("📡 Foi orientado o cliente sobre a rede 2.4Ghz e 5.8Ghz?", reply_markup=build_inline_keyboard("orientacao", SIM_NAO_OPCOES))
    elif step == "velocidade":
        await message.reply_text("🚀 Teste de velocidade dentro do plano contratado?", reply_markup=build_inline_keyboard("velocidade", SIM_NAO_OPCOES))
    elif step == "canal24":
        await message.reply_text("📶 Selecione o canal 2.4Ghz:", reply_markup=build_inline_keyboard("canal24", CANAIS_24_OPCOES))
    elif step == "canal5":
        await message.reply_text("📶 Selecione o canal 5Ghz:", reply_markup=build_inline_keyboard("canal5", CANAIS_5_OPCOES))
    elif step == "fixacao":
        if tipo in {"Instalação", "Mudança de endereço"}:
            await message.reply_text("🔩 Qual a forma de fixação dos equipamentos (roteador e ONU)?", reply_markup=ReplyKeyboardRemove())
        else:
            estado["step"] = "config_padrao"
            await perguntar(message, estado)
    elif step == "config_padrao":
        await message.reply_text("⚙️ Padrões de configurações do roteador e acesso remoto habilitado?", reply_markup=build_inline_keyboard("config_padrao", SIM_NAO_OPCOES))
    elif step == "pos_venda":
        if tipo in {"Instalação", "Mudança de endereço"}:
            await message.reply_text("🤝 Feito pós venda imediato?", reply_markup=ReplyKeyboardRemove())
        else:
            estado["step"] = "energia"
            await perguntar(message, estado)
    elif step == "energia":
        await message.reply_text("🔌 Equipamentos ficaram ligados em?", reply_markup=build_inline_keyboard("energia", ENERGIA_OPCOES))
    elif step == "energia_outro":
        await message.reply_text("✍️ Descreva em que os equipamentos ficaram ligados:", reply_markup=ReplyKeyboardRemove())
    elif step == "organizacao":
        await message.reply_text("🧹 Equipamentos foram organizados conforme nossos padrões?", reply_markup=build_inline_keyboard("organizacao", SIM_NAO_OPCOES))
    elif step == "assinatura":
        await message.reply_text("🖊️ Assinatura do cliente?", reply_markup=build_inline_keyboard("assinatura", SIM_NAO_OPCOES))
    elif step == "assinatura_motivo":
        await message.reply_text("✍️ Informe o motivo da ausência de assinatura:", reply_markup=ReplyKeyboardRemove())
    elif step == "materiais_utilizados":
        await message.reply_text("📦 Materiais utilizados:", reply_markup=ReplyKeyboardRemove())
    elif step == "materiais_retirados":
        await message.reply_text("📤 Materiais retirados (se não houver, digite: -):", reply_markup=ReplyKeyboardRemove())
    elif step == "confirmar":
        relatorio = montar_relatorio(dados)
        await enviar_texto_longo(message, relatorio)
        await message.reply_text("📨 O que deseja fazer?", reply_markup=build_inline_keyboard("confirmar", CONFIRMACAO_ENVIO_OPCOES))
    elif step == "editar":
        await message.reply_text("✏️ Selecione a etapa que deseja editar:", reply_markup=build_inline_keyboard("editar_os", EDITAR_OS_OPCOES, per_row=1))
    elif step == "perguntar_retirada":
        await message.reply_text(
            "📦 Foram informados materiais retirados.\nDeseja gerar também o relatório de retirada de equipamentos?",
            reply_markup=build_inline_keyboard("gerar_retirada", GERAR_RETIRADA_OPCOES)
        )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query or query.message.chat.type != "private":
        return
    await query.answer()

    user_id = query.from_user.id
    if user_id not in usuarios:
        return

    estado = usuarios[user_id]
    step = estado["step"]
    dados = estado["dados"]

    field, code = query.data.split("|", 1)
    valid = False

    if field == "reiniciar_fluxo":
        pending = estado.get("pending_start")
        if code == "reiniciar_sim":
            usuarios.pop(user_id, None)
            if pending == "assistencia":
                usuarios[user_id] = {"step": "os", "dados": {"tipo": "Assistência"}, "pending_start": None}
                await query.message.reply_text("🛠️ Tipo definido: Assistência.\n\n📌 Digite o número da O.S.:", reply_markup=ReplyKeyboardRemove())
                return
            elif pending == "instalacao":
                usuarios[user_id] = {"step": "os", "dados": {"tipo": "Instalação"}, "pending_start": None}
                await query.message.reply_text("📡 Tipo definido: Instalação.\n\n📌 Digite o número da O.S.:", reply_markup=ReplyKeyboardRemove())
                return
            elif pending == "mudanca":
                usuarios[user_id] = {"step": "os", "dados": {"tipo": "Mudança de endereço"}, "pending_start": None}
                await query.message.reply_text("🏠 Tipo definido: Mudança de endereço.\n\n📌 Digite o número da O.S.:", reply_markup=ReplyKeyboardRemove())
                return
            else:
                usuarios[user_id] = {"step": "os", "dados": {}, "pending_start": None}
                await query.message.reply_text("👋 Vamos iniciar o relatório.\n\n📌 Digite o número da O.S.:", reply_markup=ReplyKeyboardRemove())
                return
        else:
            await query.message.reply_text("👍 Fluxo atual mantido.")
            return

    if step == "tipo" and field == "tipo":
        dados["tipo"] = TIPOS_MAP.get(code, code)
        estado["step"] = "inicio"
        valid = True
    elif step == "tec_ext" and field == "tec_ext":
        dados["tec_ext"] = TECNICOS_MAP.get(code, code)
        salvar_tecnico_usuario(user_id, dados["tec_ext"])
        estado["step"] = "tec_int"
        valid = True
    elif step == "tec_int" and field == "tec_int":
        dados["tec_int"] = TECNICOS_MAP.get(code, code)
        estado["step"] = "problema"
        valid = True
    elif step == "problema" and field == "problema":
        dados["problema"] = PROBLEMAS_MAP.get(code, code)
        estado["step"] = "solucao"
        valid = True
    elif step == "segundo_ponto" and field == "segundo_ponto":
        dados["segundo_ponto"] = SIM_NAO_MAP.get(code, code)
        estado["step"] = "iptv"
        valid = True
    elif step == "iptv" and field == "iptv":
        dados["iptv"] = "Sim, cliente ciente de possível interferência" if code == "sim" else "Não"
        estado["step"] = "sinal_fibra"
        valid = True
    elif step == "danos" and field == "danos":
        dados["danos"] = SIM_NAO_MAP.get(code, code)
        if code == "sim":
            estado["step"] = "supervisor_ciente"
        else:
            dados["supervisor_ciente"] = "-"
            dados["danos_descricao"] = "-"
            estado["step"] = "orientacao"
        valid = True
    elif step == "supervisor_ciente" and field == "supervisor_ciente":
        dados["supervisor_ciente"] = SIM_NAO_MAP.get(code, code)
        estado["step"] = "danos_descricao"
        valid = True
    elif step == "orientacao" and field == "orientacao":
        dados["orientacao"] = SIM_NAO_MAP.get(code, code)
        estado["step"] = "velocidade"
        valid = True
    elif step == "velocidade" and field == "velocidade":
        dados["velocidade"] = SIM_NAO_MAP.get(code, code)
        estado["step"] = "canal24"
        valid = True
    elif step == "canal24" and field == "canal24":
        dados["canal24"] = code
        estado["step"] = "canal5"
        valid = True
    elif step == "canal5" and field == "canal5":
        dados["canal5"] = code
        estado["step"] = "fixacao"
        valid = True
    elif step == "config_padrao" and field == "config_padrao":
        dados["config_padrao"] = SIM_NAO_MAP.get(code, code)
        estado["step"] = "pos_venda"
        valid = True
    elif step == "energia" and field == "energia":
        if code == "outro":
            estado["step"] = "energia_outro"
        else:
            dados["energia"] = ENERGIA_MAP.get(code, code)
            estado["step"] = "organizacao"
        valid = True
    elif step == "organizacao" and field == "organizacao":
        dados["organizacao"] = SIM_NAO_MAP.get(code, code)
        estado["step"] = "assinatura"
        valid = True
    elif step == "assinatura" and field == "assinatura":
        dados["assinatura"] = "Sim" if code == "sim" else "Não"
        if code == "nao":
            estado["step"] = "assinatura_motivo"
        else:
            dados["assinatura_motivo"] = "-"
            estado["step"] = "materiais_utilizados"
        valid = True
    elif step == "confirmar" and field == "confirmar":
        if code == "enviar":
            relatorio = montar_relatorio(dados)
            await enviar_grupo_longo(context, relatorio, query.from_user)
            salvar_historico(dados, relatorio, "O.S.")
            materiais_retirados = (dados.get("materiais_retirados") or "-").strip()
            if materiais_retirados != "-":
                estado["step"] = "perguntar_retirada"
                await query.message.reply_text("✅ Relatório O.S. enviado com sucesso.")
                await perguntar(query.message, estado)
                return
            await query.message.reply_text("✅ Relatório O.S. enviado com sucesso.", reply_markup=ReplyKeyboardRemove())
            usuarios.pop(user_id, None)
            return
        elif code == "editar":
            estado["step"] = "editar"
            await perguntar(query.message, estado)
            return
        else:
            usuarios.pop(user_id, None)
            await query.message.reply_text("❌ Fluxo cancelado.", reply_markup=ReplyKeyboardRemove())
            return
    elif step == "editar" and field == "editar_os":
        novo_step = EDIT_MAP_OS.get(code)
        if novo_step:
            estado["step"] = novo_step
            await perguntar(query.message, estado)
            return
    elif step == "perguntar_retirada" and field == "gerar_retirada":
        os_numero = dados.get("os", "-")
        usuarios.pop(user_id, None)
        if code == "sim":
            iniciar_fluxo_retirada_prefill(user_id, os_numero)
            await query.message.reply_text(
                f"📦 Iniciando relatório de retirada para a O.S. {os_numero}.\n\n🔄 Selecione o tipo de retirada:",
                reply_markup=build_inline_keyboard("tipo_retirada", [
                    ("troca", "Troca"),
                    ("cancelamento", "Cancelamento"),
                ])
            )
        else:
            await query.message.reply_text("👍 Fluxo finalizado.", reply_markup=ReplyKeyboardRemove())
        return

    if not valid:
        return

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
    step = estado["step"]
    dados = estado["dados"]
    texto = update.message.text.strip()

    if step == "os":
        if not validar_os(texto):
            await update.message.reply_text("⚠️ Número de O.S. inválido. Digite apenas números.")
            return
        dados["os"] = texto
        if not dados.get("tipo"):
            estado["step"] = "tipo"
        else:
            estado["step"] = "inicio"
    elif step == "inicio":
        if not validar_hora(texto):
            await update.message.reply_text("⚠️ Hora inválida. Use o formato HH:MM. Ex: 16:04")
            return
        dados["inicio"] = texto
        tecnico_padrao = obter_tecnico_usuario(user_id)
        if tecnico_padrao:
            dados["tec_ext"] = tecnico_padrao
            estado["step"] = "tec_int"
        else:
            estado["step"] = "tec_ext"
    elif step == "solucao":
        await update.message.reply_text("🧠 Padronizando texto...", reply_markup=ReplyKeyboardRemove())
        dados["solucao"] = processar_texto(texto or "-", "solucao")
        estado["step"] = "observacoes"
    elif step == "observacoes":
        dados["observacoes"] = processar_texto(texto or "-", "observacao") if (texto or "-").strip() != "-" else "-"
        estado["step"] = "cabo"
    elif step == "cabo":
        dados["cabo"] = texto or "-"
        estado["step"] = "wifi"
    elif step == "wifi":
        dados["wifi"] = texto or "-"
        estado["step"] = "local"
    elif step == "local":
        dados["local"] = texto or "-"
        estado["step"] = "segundo_ponto"
    elif step == "sinal_fibra":
        valor = normalizar_sinal(texto)
        if valor is None:
            await update.message.reply_text("⚠️ Digite um valor válido. Exemplo: 17.22")
            return
        dados["sinal_fibra"] = valor
        estado["step"] = "sinal_cto"
    elif step == "sinal_cto":
        valor = normalizar_sinal(texto)
        if valor is None:
            await update.message.reply_text("⚠️ Digite um valor válido. Exemplo: 16.25 ou apenas - para Fibra Flash")
            return
        dados["sinal_cto"] = valor
        estado["step"] = "danos"
    elif step == "danos_descricao":
        descricao = processar_texto(texto or "-", "danos")
        if dados.get("supervisor_ciente") == "Não":
            descricao = f"Supervisor não ciente do ocorrido. {descricao}"
        dados["danos_descricao"] = descricao
        estado["step"] = "orientacao"
    elif step == "fixacao":
        dados["fixacao"] = texto or "-"
        estado["step"] = "config_padrao"
    elif step == "pos_venda":
        dados["pos_venda"] = texto or "-"
        estado["step"] = "energia"
    elif step == "energia_outro":
        dados["energia"] = texto or "-"
        estado["step"] = "organizacao"
    elif step == "assinatura_motivo":
        dados["assinatura_motivo"] = processar_texto(texto or "-", "assinatura")
        estado["step"] = "materiais_utilizados"
    elif step == "materiais_utilizados":
        dados["materiais_utilizados"] = texto or "-"
        estado["step"] = "materiais_retirados"
    elif step == "materiais_retirados":
        dados["materiais_retirados"] = texto or "-"
        estado["step"] = "confirmar"
    else:
        return

    await perguntar(update.message, estado)