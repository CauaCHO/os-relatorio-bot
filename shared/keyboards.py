from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def kb(prefix, options, per_row=2):
    rows, row = [], []
    for code, label in options:
        row.append(InlineKeyboardButton(label, callback_data=f"{prefix}|{code}"))
        if len(row) == per_row:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(rows)


MAIN_MENU = [
    ("assistencias", "🔧 Assistências"),
    ("retirada", "📦 Retirada"),
    ("estoque", "🏢 Estoque"),
    ("ausente", "🚫 Ausente"),
    ("paralisada", "⏸️ Paralisada"),
    ("pendencias", "📋 Pendências"),
    ("config", "⚙️ Configurações"),
]

CONFIRM_MENU = [
    ("enviar", "✅ Enviar relatório"),
    ("editar", "✏️ Editar etapa específica"),
    ("cancelar", "❌ Cancelar"),
]

YES_NO = [("Sim", "Sim"), ("Não", "Não")]

SECOND_POINT = [
    ("Roteador", "📡 Roteador"),
    ("PC", "💻 PC"),
    ("TV", "📺 TV"),
    ("Câmera", "🎥 Câmera"),
    ("Outro", "➕ Outro"),
]
