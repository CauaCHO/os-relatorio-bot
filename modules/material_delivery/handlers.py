from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from config import CHAT_ID
from core.helpers import validar_os
from core.storage import salvar_historico
from shared.commands import status_texto
from shared.keyboards import (
    build_inline_keyboard,
    REINICIAR_FLUXO_OPCOES,
    CONFIRMACAO_ENVIO_OPCOES,
    TIPO_RETIRADA_OPCOES,
    TIPO_RETIRADA_MAP,
    ROTEADORES_OPCOES,
    ROTEADORES_MAP,
    ONU_OPCOES,
    ONU_MAP,
    SIM_NAO_OPCOES,
    SIM_NAO_MAP,
    DESTINO_OPCOES,
    DESTINO_MAP,
    RECEBIDO_POR_OPCOES,
    RECEBIDO_POR_MAP,
)

from modules.material_delivery.report import montar_relatorio_material

usuarios_material = {}

EDIT_MAP_MATERIAL = {
    "os": "os",
    "tipo": "tipo_retirada",
    "tem_roteador": "tem_roteador",
    "roteador": "roteador",
    "tem_onu": "tem_onu",
    "onu": "onu",
    "patchcord": "patchcord",
    "outro": "outro_tem",
    "destino": "destino",
    "recebido": "recebido_por",
}

EDITAR_MATERIAL_OPCOES = [
    ("os", "O.S."),
    ("tipo", "Tipo de retirada"),
    ("tem_roteador", "Tem roteador"),
    ("roteador", "Modelo do roteador"),
    ("tem_onu", "Tem ONU"),
    ("onu", "Modelo da ONU"),
    ("patchcord", "PatchCord"),
    ("outro", "Outro equipamento"),
    ("destino", "Destino"),
    ("recebido", "Recebido por"),
]


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


def aplicar_destino_automatico(dados: dict, destino_codigo: str):
    """
    Regras:
    - Estoque FND  -> Cidade Fernandópolis / Recebido por Cauã
    - Estoque SJRP -> Cidade São José do Rio Preto / Recebido por Kesli
    - Estoque VT   -> Cidade Votuporanga / perguntar quem recebeu
    """
    dados["destino"] = DESTINO_MAP.get(destino_codigo, destino_codigo)

    if destino_codigo == "estoque_fnd":
        dados["cidade"] = "Fernandópolis"
        dados["recebido_por"] = "Cauã"

    elif destino_codigo == "estoque_sjrp":
        dados["cidade"] = "São José do Rio Preto"
        dados["recebido_por"] = "Kesli"

    elif destino_codigo == "estoque_vt":
        dados["cidade"] = "Votuporanga"
        dados["recebido_por"] = "-"

    else:
        dados["cidade"] = "-"
        dados["recebido_por"] = "-"


def iniciar_fluxo_retirada_prefill(user_id: int, os_numero: str):
    usuarios_material[user_id] = {
        "step": "tipo_retirada",
        "dados": {
            "os": os_numero,
            "tem_roteador": "Não",
            "roteador": "-",
            "tem_onu": "Não",
            "onu": "-",
            "patchcord": "Não",
            "outro": "-",
            "destino": "-",
            "cidade": "-",
            "recebido_por": "-",
        },
        "pending_start": None,
    }


async def retirada(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    if update.effective_user.id in usuarios_material:
        usuarios_material[update.effective_user.id]["pending_start"] = "retirada"
        await update.effective_message.reply_text(
            "⚠️ Você já possui um relatório de estoque em andamento.\n\nDeseja cancelar o fluxo atual e iniciar um novo?",
            reply_markup=build_inline_keyboard("reiniciar_material", REINICIAR_FLUXO_OPCOES)
        )
        return

    usuarios_material[update.effective_user.id] = {
        "step": "os",
        "dados": {
            "tem_roteador": "Não",
            "roteador": "-",
            "tem_onu": "Não",
            "onu": "-",
            "patchcord": "Não",
            "outro": "-",
            "destino": "-",
            "cidade": "-",
            "recebido_por": "-",
        },
        "pending_start": None,
    }

    await update.effective_message.reply_text(
        "🏢 Vamos iniciar o relatório de Entrega no Estoque.\n\n📌 Digite o número da O.S.:",
        reply_markup=ReplyKeyboardRemove()
    )


async def estoque(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await retirada(update, context)


async def cancelar_material(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios_material.pop(update.effective_user.id, None)
    await update.effective_message.reply_text(
        "❌ Relatório de estoque cancelado.",
        reply_markup=ReplyKeyboardRemove()
    )


async def status_material(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fluxo_ativo = update.effective_user.id in usuarios_material
    step = usuarios_material.get(update.effective_user.id, {}).get("step")
    await update.effective_message.reply_text(
        status_texto(fluxo_ativo, step, False, "Módulo Estoque"),
        parse_mode="HTML"
    )


async def perguntar(message, estado: dict):
    step = estado["step"]

    if step == "tipo_retirada":
        await message.reply_text(
            "🔄 Selecione o tipo de retirada:",
            reply_markup=build_inline_keyboard("tipo_retirada", TIPO_RETIRADA_OPCOES)
        )

    elif step == "tem_roteador":
        await message.reply_text(
            "📡 Há roteador entregue ao estoque?",
            reply_markup=build_inline_keyboard("tem_roteador", SIM_NAO_OPCOES)
        )

    elif step == "roteador":
        await message.reply_text(
            "📡 Selecione o modelo do roteador:",
            reply_markup=build_inline_keyboard("roteador", ROTEADORES_OPCOES)
        )

    elif step == "tem_onu":
        await message.reply_text(
            "📶 Há ONU entregue ao estoque?",
            reply_markup=build_inline_keyboard("tem_onu", SIM_NAO_OPCOES)
        )

    elif step == "onu":
        await message.reply_text(
            "📶 Selecione o modelo da ONU:",
            reply_markup=build_inline_keyboard("onu", ONU_OPCOES)
        )

    elif step == "patchcord":
        await message.reply_text(
            "🔗 Possui PatchCord?",
            reply_markup=build_inline_keyboard("patchcord", SIM_NAO_OPCOES)
        )

    elif step == "outro_tem":
        await message.reply_text(
            "➕ Há outro equipamento entregue?",
            reply_markup=build_inline_keyboard("outro_tem", SIM_NAO_OPCOES)
        )

    elif step == "outro_descricao":
        await message.reply_text(
            "✍️ Descreva o outro equipamento:",
            reply_markup=ReplyKeyboardRemove()
        )

    elif step == "destino":
        await message.reply_text(
            "📦 Selecione o destino:",
            reply_markup=build_inline_keyboard("destino", DESTINO_OPCOES)
        )

    elif step == "recebido_por":
        # Só deve ser perguntado para Votuporanga
        opcoes_vt = [
            ("giovani", "Giovani"),
            ("dwedinei", "Dwedinei"),
            ("leonardo", "Leonardo"),
        ]
        await message.reply_text(
            "👤 Selecione quem recebeu em Votuporanga:",
            reply_markup=build_inline_keyboard("recebido_por", opcoes_vt)
        )

    elif step == "confirmar":
        await message.reply_text(
            "📨 Revisão final do relatório de estoque\n\nEscolha uma opção:",
            reply_markup=build_inline_keyboard("confirmar_material", CONFIRMACAO_ENVIO_OPCOES)
        )

    elif step == "editar":
        await message.reply_text(
            "✏️ Selecione a etapa que deseja editar:",
            reply_markup=build_inline_keyboard("editar_material", EDITAR_MATERIAL_OPCOES, per_row=1)
        )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query or query.message.chat.type != "private":
        return

    await query.answer()

    user_id = query.from_user.id
    if user_id not in usuarios_material:
        return

    estado = usuarios_material[user_id]
    step = estado["step"]
    dados = estado["dados"]

    try:
        field, code = query.data.split("|", 1)
    except ValueError:
        return

    valid = False

    # =========================
    # REINÍCIO
    # =========================
    if field == "reiniciar_material":
        if code == "reiniciar_sim":
            usuarios_material[user_id] = {
                "step": "os",
                "dados": {
                    "tem_roteador": "Não",
                    "roteador": "-",
                    "tem_onu": "Não",
                    "onu": "-",
                    "patchcord": "Não",
                    "outro": "-",
                    "destino": "-",
                    "cidade": "-",
                    "recebido_por": "-",
                },
                "pending_start": None,
            }
            await query.message.reply_text(
                "🏢 Digite o número da O.S.:",
                reply_markup=ReplyKeyboardRemove()
            )
            return
        else:
            await query.message.reply_text("👍 Fluxo atual mantido.")
            return

    # =========================
    # FLUXO PRINCIPAL
    # =========================
    if step == "tipo_retirada" and field == "tipo_retirada":
        dados["tipo_retirada"] = TIPO_RETIRADA_MAP.get(code, code)
        estado["step"] = "tem_roteador"
        valid = True

    elif step == "tem_roteador" and field == "tem_roteador":
        dados["tem_roteador"] = SIM_NAO_MAP.get(code, code)
        if code == "sim":
            estado["step"] = "roteador"
        else:
            dados["roteador"] = "-"
            estado["step"] = "tem_onu"
        valid = True

    elif step == "roteador" and field == "roteador":
        dados["roteador"] = ROTEADORES_MAP.get(code, code)
        estado["step"] = "tem_onu"
        valid = True

    elif step == "tem_onu" and field == "tem_onu":
        dados["tem_onu"] = SIM_NAO_MAP.get(code, code)
        if code == "sim":
            estado["step"] = "onu"
        else:
            dados["onu"] = "-"
            estado["step"] = "patchcord"
        valid = True

    elif step == "onu" and field == "onu":
        dados["onu"] = ONU_MAP.get(code, code)
        estado["step"] = "patchcord"
        valid = True

    elif step == "patchcord" and field == "patchcord":
        dados["patchcord"] = SIM_NAO_MAP.get(code, code)
        estado["step"] = "outro_tem"
        valid = True

    elif step == "outro_tem" and field == "outro_tem":
        if code == "sim":
            estado["step"] = "outro_descricao"
        else:
            dados["outro"] = "-"
            estado["step"] = "destino"
        valid = True

    elif step == "destino" and field == "destino":
        aplicar_destino_automatico(dados, code)

        # FND e SJRP já definem automaticamente cidade e recebido_por
        if code in ("estoque_fnd", "estoque_sjrp"):
            estado["step"] = "confirmar"
        else:
            # VT precisa escolher quem recebeu
            estado["step"] = "recebido_por"

        valid = True

    elif step == "recebido_por" and field == "recebido_por":
        dados["recebido_por"] = RECEBIDO_POR_MAP.get(code, code)
        estado["step"] = "confirmar"
        valid = True

    elif step == "confirmar" and field == "confirmar_material":
        if code == "enviar":
            relatorio = montar_relatorio_material(dados)
            await enviar_grupo_longo(context, relatorio, query.from_user)
            salvar_historico(
                {"os": dados.get("os"), "tipo": "Entrega no Estoque"},
                relatorio,
                "Estoque"
            )

            await query.message.reply_text(
                "✅ Relatório de estoque enviado com sucesso.\n\n"
                f"📋 O.S.: {dados.get('os', '-')}\n"
                f"🏢 Destino: {dados.get('destino', '-')}\n"
                f"👤 Recebido por: {dados.get('recebido_por', '-')}",
                reply_markup=ReplyKeyboardRemove()
            )
            usuarios_material.pop(user_id, None)
            return

        elif code == "editar":
            estado["step"] = "editar"
            await perguntar(query.message, estado)
            return

        else:
            usuarios_material.pop(user_id, None)
            await query.message.reply_text(
                "❌ Fluxo cancelado.",
                reply_markup=ReplyKeyboardRemove()
            )
            return

    elif step == "editar" and field == "editar_material":
        novo_step = EDIT_MAP_MATERIAL.get(code)
        if novo_step:
            # Se editar destino, a lógica automática será reaplicada ao selecionar novamente
            estado["step"] = novo_step
            await perguntar(query.message, estado)
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
    if user_id not in usuarios_material:
        return

    estado = usuarios_material[user_id]
    step = estado["step"]
    dados = estado["dados"]
    texto = update.message.text.strip()

    if step == "os":
        if not validar_os(texto):
            await update.message.reply_text(
                "⚠️ Número de O.S. inválido. Digite apenas números."
            )
            return

        dados["os"] = texto
        estado["step"] = "tipo_retirada"

    elif step == "outro_descricao":
        dados["outro"] = texto or "-"
        estado["step"] = "destino"

    else:
        return

    await perguntar(update.message, estado)