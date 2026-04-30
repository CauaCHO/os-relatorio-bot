from telegram import Update
from telegram.ext import ContextTypes

from core.config_store import (
    is_config_user,
    check_config_password,
    get_tecnicos,
    set_tecnicos,
    get_roteadores,
    set_roteadores,
    get_locais_instalacao,
    set_locais_instalacao,
    get_estoque_recebedores,
    set_estoque_recebedores,
    add_item,
    remove_item,
)
from shared.keyboards import build_inline_keyboard

config_sessions = {}

CATEGORY_LABELS = {
    "tecnicos": "👨‍🔧 Técnicos",
    "roteadores": "📡 Modelos de Roteador",
    "locais": "📍 Locais sugeridos",
    "estoque_fnd": "🏢 Recebedores Estoque FND",
    "estoque_vt": "🏢 Recebedores Estoque VT",
    "estoque_sjrp": "🏢 Recebedores Estoque SJRP",
}


def _get_lista(categoria: str) -> list[str]:
    if categoria == "tecnicos":
        return get_tecnicos()
    if categoria == "roteadores":
        return get_roteadores()
    if categoria == "locais":
        return get_locais_instalacao()
    if categoria == "estoque_fnd":
        return get_estoque_recebedores("Estoque FND")
    if categoria == "estoque_vt":
        return get_estoque_recebedores("Estoque VT")
    if categoria == "estoque_sjrp":
        return get_estoque_recebedores("Estoque SJRP")
    return []


def _set_lista(categoria: str, lista: list[str]):
    if categoria == "tecnicos":
        return set_tecnicos(lista)
    if categoria == "roteadores":
        return set_roteadores(lista)
    if categoria == "locais":
        return set_locais_instalacao(lista)
    if categoria == "estoque_fnd":
        return set_estoque_recebedores("Estoque FND", lista)
    if categoria == "estoque_vt":
        return set_estoque_recebedores("Estoque VT", lista)
    if categoria == "estoque_sjrp":
        return set_estoque_recebedores("Estoque SJRP", lista)


def _menu_principal():
    opcoes = [
        ("tecnicos", "👨‍🔧 Técnicos"),
        ("roteadores", "📡 Roteadores"),
        ("locais", "📍 Locais"),
        ("estoque_fnd", "🏢 Estoque FND"),
        ("estoque_vt", "🏢 Estoque VT"),
        ("estoque_sjrp", "🏢 Estoque SJRP"),
    ]
    return build_inline_keyboard("config_cat", opcoes, per_row=1)


def _menu_acoes(categoria: str):
    opcoes = [
        (f"{categoria}::listar", "📋 Listar"),
        (f"{categoria}::adicionar", "➕ Adicionar"),
        (f"{categoria}::remover", "➖ Remover"),
        ("voltar", "⬅️ Voltar"),
    ]
    return build_inline_keyboard("config_action", opcoes, per_row=1)


async def config_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    username = update.effective_user.username
    user_id = update.effective_user.id

    if not is_config_user(username, user_id):
        await update.effective_message.reply_text(
            "⛔ Você não tem permissão para acessar o painel de configuração.\n\n"
            f"👤 Usuário: @{username if username else '-'}\n"
            f"🆔 ID: {user_id}\n\n"
            "Peça para adicionar seu usuário ou ID no app_config.json."
        )
        return

    config_sessions[user_id] = {
        "step": "senha",
    }

    await update.effective_message.reply_text(
        "🔐 Digite a senha de acesso ao /config:\n\n"
        f"👤 Usuário: @{username if username else '-'}\n"
        f"🆔 ID: {user_id}"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != "private":
        return

    user_id = update.effective_user.id
    if user_id not in config_sessions:
        return

    sess = config_sessions[user_id]
    texto = update.effective_message.text.strip()

    if sess["step"] == "senha":
        if not check_config_password(texto):
            await update.effective_message.reply_text("❌ Senha incorreta.")
            config_sessions.pop(user_id, None)
            return

        sess["step"] = "menu"
        await update.effective_message.reply_text(
            "⚙️ <b>Painel de Configuração</b>\n\nSelecione a categoria:",
            parse_mode="HTML",
            reply_markup=_menu_principal()
        )
        return

    if sess["step"] == "adicionar":
        categoria = sess["categoria"]
        lista = _get_lista(categoria)
        lista = add_item(lista, texto)
        _set_lista(categoria, lista)
        sess["step"] = "menu"

        await update.effective_message.reply_text(
            f"✅ Item adicionado em {CATEGORY_LABELS[categoria]}.",
            reply_markup=_menu_acoes(categoria)
        )
        return


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query or query.message.chat.type != "private":
        return

    await query.answer()

    user_id = query.from_user.id
    if user_id not in config_sessions:
        await query.message.reply_text("⚠️ Inicie com /config.")
        return

    sess = config_sessions[user_id]

    try:
        field, code = query.data.split("|", 1)
    except ValueError:
        return

    if field == "config_cat":
        categoria = code
        sess["categoria"] = categoria
        sess["step"] = "menu"

        await query.message.reply_text(
            f"{CATEGORY_LABELS[categoria]}\n\nEscolha uma ação:",
            reply_markup=_menu_acoes(categoria)
        )
        return

    if field == "config_action":
        if code == "voltar":
            sess["step"] = "menu"
            await query.message.reply_text(
                "⚙️ <b>Painel de Configuração</b>\n\nSelecione a categoria:",
                parse_mode="HTML",
                reply_markup=_menu_principal()
            )
            return

        categoria, acao = code.split("::", 1)
        sess["categoria"] = categoria

        if acao == "listar":
            itens = _get_lista(categoria)
            texto = "\n".join([f"• {x}" for x in itens]) if itens else "Nenhum item cadastrado."

            await query.message.reply_text(
                f"{CATEGORY_LABELS[categoria]}\n\n{texto}",
                reply_markup=_menu_acoes(categoria)
            )
            return

        if acao == "adicionar":
            sess["step"] = "adicionar"
            await query.message.reply_text(
                f"✍️ Digite o item que deseja adicionar em {CATEGORY_LABELS[categoria]}:"
            )
            return

        if acao == "remover":
            itens = _get_lista(categoria)
            if not itens:
                await query.message.reply_text(
                    "Nenhum item para remover.",
                    reply_markup=_menu_acoes(categoria)
                )
                return

            opcoes = [(str(i), nome) for i, nome in enumerate(itens)]

            await query.message.reply_text(
                f"➖ Selecione o item para remover em {CATEGORY_LABELS[categoria]}:",
                reply_markup=build_inline_keyboard(f"config_remove_{categoria}", opcoes, per_row=1)
            )
            return

    if field.startswith("config_remove_"):
        categoria = field.replace("config_remove_", "")
        itens = _get_lista(categoria)

        try:
            idx = int(code)
        except ValueError:
            return

        if 0 <= idx < len(itens):
            removido = itens[idx]
            nova = remove_item(itens, removido)
            _set_lista(categoria, nova)

            await query.message.reply_text(
                f"✅ Removido: {removido}",
                reply_markup=_menu_acoes(categoria)
            )
