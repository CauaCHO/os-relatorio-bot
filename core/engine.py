import json
from pathlib import Path

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from config import CHAT_ID, CONFIG_FILE, RELATORIOS_FILE, PENDENCIAS_FILE, USUARIOS_FILE, CONFIG_PASSWORD, CONFIG_ALLOWED_USERS, CONFIG_ALLOWED_IDS
from shared.keyboards import kb, MAIN_MENU, CONFIRM_MENU, YES_NO, SECOND_POINT
from shared.storage import read_json, write_json, append_json
from shared.utils import escape_html, now_hm, calc_time, valid_hour, normalize_signal, normalize_speed, format_materials_free

SESSIONS = {}


def cfg():
    default = {
        "allowed_config_users": CONFIG_ALLOWED_USERS,
        "allowed_config_ids": CONFIG_ALLOWED_IDS,
        "config_password": CONFIG_PASSWORD,
        "tecnicos": [],
        "roteadores": ["Outro"],
        "onus": ["Outro"],
        "locais": ["Outro"],
        "energia": ["Outro"],
        "materiais": ["Outro"],
        "equipamentos_cliente": ["Outro"],
        "solucoes": ["Escrever manualmente"],
        "link_loss_solucoes": ["Escrever manualmente"],
        "estoques": {}
    }
    data = read_json(CONFIG_FILE, default)
    changed = False
    for k, v in default.items():
        if k not in data:
            data[k] = v
            changed = True
    if changed:
        write_json(CONFIG_FILE, data)
    return data


def models():
    return json.loads(Path("models/assistencias.json").read_text(encoding="utf-8"))


def user_name(user):
    return f"@{user.username}" if user.username else (user.first_name or str(user.id))


async def send_group(context, text, user):
    if not CHAT_ID:
        return
    full = f"👤 <b>Preenchido por:</b> {escape_html(user_name(user))}\n\n{text}"
    for i in range(0, len(full), 3900):
        await context.bot.send_message(chat_id=CHAT_ID, text=full[i:i+3900], parse_mode="HTML")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "🚀 <b>Sistema Flash Reports v6.5 Ultra</b>\n\nSelecione uma opção:",
        parse_mode="HTML",
        reply_markup=kb("menu", MAIN_MENU, 2)
    )


async def cmd_assistencia(update, context):
    await show_assistencias(update.effective_message)


async def cmd_retirada(update, context):
    await start_flow(update, "retirada")


async def cmd_estoque(update, context):
    await start_flow(update, "estoque")


async def cmd_ausente(update, context):
    await start_flow(update, "ausente")


async def cmd_paralisada(update, context):
    await show_paralisada(update.effective_message)


async def cmd_pendencias(update, context):
    await show_pendencias(update.effective_message)


async def cmd_baixar_pendencia(update, context):
    if not context.args:
        await update.effective_message.reply_text("Use assim:\n/baixar_pendencia 123456")
        return
    baixa_pendencia(context.args[0])
    await update.effective_message.reply_text(f"✅ O.S. {context.args[0]} removida das pendências.")


async def cmd_config(update, context):
    c = cfg()
    username = update.effective_user.username
    uid = update.effective_user.id
    allowed = (username and username in [u.lstrip("@") for u in c.get("allowed_config_users", [])]) or str(uid) in [str(x) for x in c.get("allowed_config_ids", [])]
    if not allowed:
        await update.effective_message.reply_text(
            f"⛔ Você não tem permissão para acessar o /config.\n\n👤 @{username or '-'}\n🆔 {uid}"
        )
        return
    SESSIONS[uid] = {"mode": "config", "step": "senha"}
    await update.effective_message.reply_text(f"🔐 Digite a senha do /config:\n\n👤 @{username or '-'}\n🆔 {uid}")


async def show_assistencias(message):
    opts = [(k, v["title"]) for k, v in models().items()]
    await message.reply_text("🔧 Escolha o modelo:", reply_markup=kb("assist", opts, 1))


async def show_paralisada(message):
    opts = [("nova", "⏸️ Paralisar nova O.S."), ("lista", "📋 Ver / desparalisar O.S.")]
    await message.reply_text("⏸️ O.S. Paralisada:", reply_markup=kb("par_menu", opts, 1))


async def show_pendencias(message):
    pend = read_json(PENDENCIAS_FILE, [])
    if not pend:
        await message.reply_text("✅ Nenhuma pendência/paralisada no momento.")
        return
    linhas = ["📋 <b>Pendências / O.S. Paralisadas</b>", ""]
    opts = []
    for p in pend:
        osn = str(p.get("os", "-"))
        linhas.append(f"• O.S. {escape_html(osn)} — {escape_html(p.get('tipo', '-'))}")
        opts.append((osn, f"✅ Baixar {osn}"))
    await message.reply_text("\n".join(linhas), parse_mode="HTML", reply_markup=kb("baixar", opts, 1))


def baixa_pendencia(osn):
    pend = read_json(PENDENCIAS_FILE, [])
    pend = [p for p in pend if str(p.get("os")) != str(osn)]
    write_json(PENDENCIAS_FILE, pend)


def add_pendencia(data, tipo):
    pend = read_json(PENDENCIAS_FILE, [])
    osn = data.get("os")
    pend = [p for p in pend if str(p.get("os")) != str(osn)]
    pend.append({"os": osn, "tipo": tipo, "data": data})
    write_json(PENDENCIAS_FILE, pend)


def simple_flows():
    return {
        "retirada": {
            "title": "🔧 RETIRADA DE EQUIPAMENTOS",
            "fields": [
                {"id": "os", "label": "O.S", "type": "os", "question": "📌 Digite o número da O.S.:"},
                {"id": "equipamentos", "label": "Equipamentos recolhidos", "type": "materials", "question": "📦 Adicione equipamentos retirados:"},
                {"id": "obs", "label": "Observações", "type": "text", "question": "📝 Observações:"},
            ],
            "mention": "@FlashNetCobranca"
        },
        "estoque": {
            "title": "📦 ENTRADA DE EQUIPAMENTOS NO ESTOQUE",
            "fields": [
                {"id": "os", "label": "O.S", "type": "os", "question": "📌 Digite o número da O.S.:"},
                {"id": "tipo_os", "label": "Tipo", "type": "choice_static", "options": ["Retirada", "Troca", "Cancelamento", "Outro"], "question": "🔧 Tipo da O.S.:"},
                {"id": "equipamentos", "label": "Equipamentos recebidos", "type": "materials", "question": "📦 Adicione equipamentos recebidos:"},
                {"id": "destino", "label": "Destino", "type": "estoque", "question": "🏢 Selecione o destino:"},
                {"id": "obs", "label": "Observações", "type": "text", "question": "📝 Observações:"},
            ]
        },
        "ausente": {
            "title": "🚫 CLIENTE AUSENTE",
            "fields": [
                {"id": "os", "label": "O.S", "type": "os", "question": "📌 Digite o número da O.S.:"},
                {"id": "tentativas", "label": "Tentativas de contato", "type": "choice_static", "options": ["Ligação sem resposta", "WhatsApp sem resposta", "Portão fechado", "Vizinho informou ausência", "Escrever manualmente"], "question": "📞 Qual foi a tentativa principal?"},
                {"id": "situacao", "label": "Situação", "type": "text", "question": "📌 Qual a situação atual?"},
                {"id": "obs", "label": "Observações", "type": "text", "question": "📝 Observações:"},
            ],
            "mention": "@flashnetagendamento"
        },
        "paralisada": {
            "title": "⏸️ O.S. PARALISADA",
            "fields": [
                {"id": "os", "label": "O.S", "type": "os", "question": "📌 Digite o número da O.S.:"},
                {"id": "motivo", "label": "Motivo da paralisação", "type": "choice_static", "options": ["Cliente solicitou reagendamento", "Falta de acesso ao local", "Aguardando material", "Aguardando suporte interno", "Problema técnico", "Escrever manualmente"], "question": "⏸️ Motivo da paralisação:"},
                {"id": "situacao", "label": "Situação atual", "type": "text", "question": "📌 Situação atual:"},
                {"id": "obs", "label": "Observações", "type": "text", "question": "📝 Observações:"},
            ]
        }
    }


async def start_assist(update, code):
    model = models()[code]
    session = {
        "mode": "flow",
        "kind": "assistencia",
        "title": model["title"],
        "fields": [
            {"id": "os", "label": "O.S", "type": "os", "question": "📌 Digite o número da O.S.:"},
            {"id": "inicio", "label": "Hora iniciada", "type": "hour", "question": "⏰ Que horas começou? Exemplo: 15:30"},
            {"id": "tec_ext", "label": "Técnico externo", "type": "choice_config", "source": "tecnicos", "question": "👨‍🔧 Técnico externo:"},
            {"id": "tec_int", "label": "Técnico interno", "type": "choice_config", "source": "tecnicos", "question": "🧑‍💻 Técnico interno:"},
        ] + model["fields"],
        "index": 0,
        "data": {},
        "materials_temp": [],
    }
    SESSIONS[update.effective_user.id] = session
    await ask(update.effective_message, session)


async def start_flow(update, name, prefill=None):
    f = simple_flows()[name]
    session = {"mode": "flow", "kind": name, "title": f["title"], "fields": f["fields"], "mention": f.get("mention"), "index": 0, "data": prefill or {}, "materials_temp": []}
    SESSIONS[update.effective_user.id] = session
    await ask(update.effective_message, session)


def cond_ok(field, data):
    cond = field.get("condition")
    if not cond:
        return True
    return data.get(cond.get("field")) == cond.get("equals")


def current_field(session):
    fields = session["fields"]
    while session["index"] < len(fields) and not cond_ok(fields[session["index"]], session["data"]):
        session["index"] += 1
    if session["index"] >= len(fields):
        return None
    return fields[session["index"]]


async def ask(message, session):
    field = current_field(session)
    if field is None:
        await review(message, session)
        return

    typ = field["type"]
    c = cfg()

    if typ == "yesno":
        await message.reply_text(field["question"], reply_markup=kb("ans", YES_NO, 2))
    elif typ == "second_point":
        await message.reply_text(field["question"], reply_markup=kb("ans", SECOND_POINT, 2))
    elif typ == "choice_config":
        opts = [(x, x) for x in c.get(field["source"], [])]
        opts.append(("__manual__", "➕ Outro / manual"))
        await message.reply_text(field["question"], reply_markup=kb("ans", opts, 1))
    elif typ == "choice_static":
        opts = [(x, x) for x in field.get("options", [])]
        await message.reply_text(field["question"], reply_markup=kb("ans", opts, 1))
    elif typ == "preset_text":
        opts = [(x, x[:55]) for x in c.get(field["source"], ["Escrever manualmente"])]
        await message.reply_text(field["question"], reply_markup=kb("ans", opts, 1))
    elif typ == "estoque":
        opts = [(x, x) for x in c.get("estoques", {}).keys()]
        await message.reply_text(field["question"], reply_markup=kb("ans", opts, 1))
    elif typ == "materials":
        await materials_menu(message, session)
    else:
        await message.reply_text(field["question"], reply_markup=ReplyKeyboardRemove())


async def materials_menu(message, session):
    c = cfg()
    opts = [(x, x) for x in c.get("materiais", [])]
    opts.append(("__manual__", "➕ Outro / manual"))
    opts.append(("__finish__", "✅ Finalizar materiais"))
    await message.reply_text("📦 Selecione um material:", reply_markup=kb("mat", opts, 1))


async def review(message, session):
    session["review"] = True
    lines = ["📋 <b>Revisão antes do envio</b>", ""]
    for f in session["fields"]:
        if not cond_ok(f, session["data"]):
            continue
        val = session["data"].get(f["id"], "-")
        lines.append(f"<b>{escape_html(f['label'])}:</b> {escape_html(val)}")
    await message.reply_text("\n".join(lines), parse_mode="HTML")
    await message.reply_text("Escolha uma opção:", reply_markup=kb("confirm", CONFIRM_MENU, 1))


def format_value(field, value):
    typ = field["type"]
    if typ == "materials":
        return escape_html(value)
    if typ == "sinal":
        return escape_html(normalize_signal(value))
    if typ == "speed":
        return escape_html(normalize_speed(value))
    return escape_html(value)


def build_report(session):
    data = session["data"]
    title = session["title"]
    kind = session["kind"]

    lines = [f"<b>{escape_html(title)}</b>", ""]

    if kind == "assistencia":
        data["fim"] = data.get("fim") or now_hm()
        tempo = calc_time(data.get("inicio", "-"), data.get("fim", "-"))
        lines.extend([
            f"<b>O.S:</b> {escape_html(data.get('os'))}",
            "",
            f"<b>Iniciada:</b> {escape_html(data.get('inicio'))}",
            f"<b>Finalizada:</b> {escape_html(data.get('fim'))}",
            f"<b>Tempo gasto:</b> {escape_html(tempo)}",
            "",
            f"<b>Técnico externo:</b> {escape_html(data.get('tec_ext'))}",
            f"<b>Técnico interno:</b> {escape_html(data.get('tec_int'))}",
            ""
        ])

    for f in session["fields"]:
        if not cond_ok(f, data):
            continue
        if kind == "assistencia" and f["id"] in ["os", "inicio", "tec_ext", "tec_int"]:
            continue
        val = format_value(f, data.get(f["id"], "-"))
        if f["id"] == "os":
            lines.append(f"<b>O.S:</b> {val}")
            lines.append("")
        else:
            lines.append(f"<b>{escape_html(f['label'])}:</b>")
            lines.append(val)
            lines.append("")

    if kind == "estoque":
        dest = data.get("destino")
        ecfg = cfg().get("estoques", {}).get(dest, {})
        cidade = ecfg.get("cidade", "-")
        recebedores = ", ".join(ecfg.get("recebedores", [])) or "-"
        lines.append(f"<b>Recebido por:</b> {escape_html(recebedores)}")
        lines.append(f"<b>Cidade:</b> {escape_html(cidade)}")

    mention = session.get("mention")
    if mention:
        lines.append("")
        lines.append(escape_html(mention))

    return "\n".join(lines).strip()


async def finalize(update, context, session):
    report = build_report(session)
    await send_group(context, report, update.effective_user)

    append_json(RELATORIOS_FILE, {"kind": session["kind"], "title": session["title"], "data": session["data"], "report": report, "user": user_name(update.effective_user)})

    if session["kind"] == "paralisada":
        add_pendencia(session["data"], "O.S. paralisada")
    elif session["kind"] == "ausente":
        add_pendencia(session["data"], "Cliente ausente")
    elif session["kind"] == "assistencia":
        baixa_pendencia(session["data"].get("os"))

    uid = update.effective_user.id

    if session["kind"] == "retirada":
        session["after_retirada"] = True
        await update.effective_message.reply_text("✅ Relatório enviado.\n\nDeseja gerar entrada no estoque?", reply_markup=kb("after_ret", YES_NO, 2))
        return

    SESSIONS.pop(uid, None)
    await update.effective_message.reply_text("✅ Relatório enviado com sucesso.")


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id

    try:
        prefix, value = q.data.split("|", 1)
    except ValueError:
        return

    if prefix == "menu":
        if value == "assistencias":
            await show_assistencias(q.message)
        elif value == "retirada":
            await start_flow(update, "retirada")
        elif value == "estoque":
            await start_flow(update, "estoque")
        elif value == "ausente":
            await start_flow(update, "ausente")
        elif value == "paralisada":
            await show_paralisada(q.message)
        elif value == "pendencias":
            await show_pendencias(q.message)
        elif value == "config":
            await cmd_config(update, context)
        return

    if prefix == "assist":
        await start_assist(update, value)
        return

    if prefix == "par_menu":
        if value == "nova":
            await start_flow(update, "paralisada")
        else:
            await show_pendencias(q.message)
        return

    if prefix == "baixar":
        baixa_pendencia(value)
        await q.message.reply_text(f"✅ O.S. {value} removida das pendências.")
        return

    if prefix.startswith("cfg"):
        await config_callback(q, prefix, value)
        return

    if uid not in SESSIONS:
        return

    session = SESSIONS[uid]

    if prefix == "ans":
        field = current_field(session)
        if not field:
            return
        if value == "__manual__" or value == "Escrever manualmente":
            session["manual_field"] = field
            await q.message.reply_text("✍️ Digite manualmente:")
            return

        session["data"][field["id"]] = value
        session["index"] += 1
        await ask(q.message, session)
        return

    if prefix == "mat":
        if value == "__finish__":
            field = current_field(session)
            materiais = session.get("materials_temp", [])
            session["data"][field["id"]] = "\n".join([f"{m['qty']}x {m['name']}" for m in materiais]) if materiais else "-"
            session["materials_temp"] = []
            session["index"] += 1
            await ask(q.message, session)
            return
        if value == "__manual__":
            session["material_manual"] = True
            await q.message.reply_text("✍️ Digite o nome do material:")
            return
        session["material_name"] = value
        await q.message.reply_text(f"Quantidade de {value}?")
        return

    if prefix == "confirm":
        if value == "enviar":
            await finalize(update, context, session)
        elif value == "cancelar":
            SESSIONS.pop(uid, None)
            await q.message.reply_text("❌ Fluxo cancelado.")
        elif value == "editar":
            opts = []
            for i, f in enumerate(session["fields"]):
                if cond_ok(f, session["data"]):
                    opts.append((str(i), f["label"][:55]))
            await q.message.reply_text("✏️ Escolha a etapa para editar:", reply_markup=kb("edit", opts, 1))
        return

    if prefix == "edit":
        session["index"] = int(value)
        session["review"] = False
        await ask(q.message, session)
        return

    if prefix == "after_ret":
        old = session["data"]
        SESSIONS.pop(uid, None)
        if value == "Sim":
            await start_flow(update, "estoque", {"os": old.get("os"), "equipamentos": old.get("equipamentos")})
        else:
            await q.message.reply_text("👍 Fluxo finalizado.")
        return


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.effective_message.text.strip()

    if uid not in SESSIONS:
        return

    session = SESSIONS[uid]

    if session.get("mode") == "config":
        await config_message(update, text)
        return

    if session.get("material_manual"):
        session["material_manual"] = False
        session["material_name"] = text
        await update.effective_message.reply_text(f"Quantidade de {text}?")
        return

    if session.get("material_name"):
        try:
            qty = int(text)
        except ValueError:
            await update.effective_message.reply_text("⚠️ Digite apenas o número da quantidade.")
            return
        session.setdefault("materials_temp", []).append({"name": session.pop("material_name"), "qty": qty})
        await update.effective_message.reply_text("✅ Material adicionado.")
        await materials_menu(update.effective_message, session)
        return

    if session.get("manual_field"):
        field = session.pop("manual_field")
        session["data"][field["id"]] = text
        session["index"] += 1
        await ask(update.effective_message, session)
        return

    field = current_field(session)
    if not field:
        return

    typ = field["type"]

    if typ == "os" and not text.isdigit():
        await update.effective_message.reply_text("⚠️ Digite apenas números para a O.S.")
        return
    if typ == "hour" and not valid_hour(text):
        await update.effective_message.reply_text("⚠️ Hora inválida. Use HH:MM. Exemplo: 15:30")
        return
    if typ == "materials":
        session["data"][field["id"]] = format_materials_free(text)
    else:
        session["data"][field["id"]] = text

    session["index"] += 1
    await ask(update.effective_message, session)


async def config_message(update, text):
    uid = update.effective_user.id
    session = SESSIONS[uid]
    c = cfg()

    if session["step"] == "senha":
        if text != c.get("config_password", CONFIG_PASSWORD):
            SESSIONS.pop(uid, None)
            await update.effective_message.reply_text("❌ Senha incorreta.")
            return
        session["step"] = "menu"
        await show_config_menu(update.effective_message)
        return

    if session["step"].startswith("add:"):
        key = session["step"].split(":", 1)[1]
        c.setdefault(key, [])
        if text not in c[key]:
            c[key].append(text)
        write_json(CONFIG_FILE, c)
        session["step"] = "menu"
        await update.effective_message.reply_text("✅ Item adicionado.")
        await show_config_menu(update.effective_message)
        return

    if session["step"] == "add_estoque_nome":
        session["new_estoque"] = text
        session["step"] = "add_estoque_cidade"
        await update.effective_message.reply_text("Cidade/unidade desse estoque?")
        return

    if session["step"] == "add_estoque_cidade":
        nome = session["new_estoque"]
        c.setdefault("estoques", {})[nome] = {"cidade": text, "recebedores": []}
        write_json(CONFIG_FILE, c)
        session["step"] = "menu"
        await update.effective_message.reply_text("✅ Estoque criado.")
        await show_config_menu(update.effective_message)
        return


async def show_config_menu(message):
    opts = [
        ("tecnicos", "👨‍🔧 Técnicos"),
        ("roteadores", "📡 Roteadores"),
        ("onus", "🧱 ONU/ONT"),
        ("locais", "📍 Locais"),
        ("materiais", "🔌 Materiais"),
        ("energia", "🔋 Energia"),
        ("solucoes", "🛠️ Textos rápidos"),
        ("estoques", "🏢 Estoques"),
        ("sair", "🚪 Sair"),
    ]
    await message.reply_text("⚙️ <b>Painel de Configuração</b>", parse_mode="HTML", reply_markup=kb("cfg_menu", opts, 1))


async def config_callback(q, prefix, value):
    uid = q.from_user.id
    if uid not in SESSIONS:
        await q.message.reply_text("Use /config primeiro.")
        return
    session = SESSIONS[uid]
    c = cfg()

    if prefix == "cfg_menu":
        if value == "sair":
            SESSIONS.pop(uid, None)
            await q.message.reply_text("✅ Configuração encerrada.")
            return
        if value == "estoques":
            opts = [("add_estoque", "➕ Adicionar estoque")]
            for k in c.get("estoques", {}).keys():
                opts.append((f"list_estoque:{k}", f"📋 {k}"))
            await q.message.reply_text("🏢 Estoques:", reply_markup=kb("cfg_action", opts, 1))
            return

        session["cfg_key"] = value
        opts = [("listar", "📋 Listar"), ("add", "➕ Adicionar"), ("remove", "➖ Remover"), ("voltar", "⬅️ Voltar")]
        await q.message.reply_text(f"⚙️ {value}", reply_markup=kb("cfg_action", opts, 1))
        return

    if prefix == "cfg_action":
        if value == "voltar":
            await show_config_menu(q.message)
            return
        if value == "add_estoque":
            session["step"] = "add_estoque_nome"
            await q.message.reply_text("Nome do estoque. Ex: Estoque FND")
            return
        key = session.get("cfg_key")
        if not key:
            return
        if value == "listar":
            items = c.get(key, [])
            text = "\n".join([f"• {x}" for x in items]) if items else "Nenhum item cadastrado."
            await q.message.reply_text(text)
            return
        if value == "add":
            session["step"] = f"add:{key}"
            await q.message.reply_text("Digite o novo item:")
            return
        if value == "remove":
            items = c.get(key, [])
            if not items:
                await q.message.reply_text("Nenhum item para remover.")
                return
            opts = [(x, f"➖ {x}") for x in items]
            await q.message.reply_text("Selecione para remover:", reply_markup=kb("cfg_remove", opts, 1))
            return

    if prefix == "cfg_remove":
        key = session.get("cfg_key")
        if key:
            c[key] = [x for x in c.get(key, []) if x != value]
            write_json(CONFIG_FILE, c)
            await q.message.reply_text("✅ Removido.")
