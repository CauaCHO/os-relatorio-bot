from telegram import InlineKeyboardMarkup, InlineKeyboardButton

# =========================
# OPÇÕES FIXAS
# =========================

SIM_NAO_OPCOES = [
    ("sim", "Sim"),
    ("nao", "Não"),
]
SIM_NAO_MAP = dict(SIM_NAO_OPCOES)

CONFIRMACAO_ENVIO_OPCOES = [
    ("enviar", "✅ Enviar"),
    ("editar", "✏️ Editar etapa específica"),
    ("cancelar", "❌ Cancelar"),
]

REINICIAR_FLUXO_OPCOES = [
    ("reiniciar_sim", "✅ Sim, reiniciar"),
    ("reiniciar_nao", "❌ Não, continuar"),
]

GERAR_RETIRADA_OPCOES = [
    ("sim", "✅ Sim"),
    ("nao", "❌ Não"),
]

REMOVER_PENDENCIA_OPCOES = [
    ("sim", "✅ Sim, continuar"),
    ("nao", "❌ Não"),
]

ENERGIA_OPCOES = [
    ("adaptador_t", "Adaptador T"),
    ("filtro", "Filtro de linha"),
    ("tomada_individual", "Tomada individual"),
    ("tomada_dupla", "Tomada dupla"),
    ("tomada_tripla", "Tomada tripla"),
    ("outro", "Outro"),
]
ENERGIA_MAP = {
    "adaptador_t": "Adaptador T",
    "filtro": "Filtro de linha",
    "tomada_individual": "Tomada individual",
    "tomada_dupla": "Tomada dupla",
    "tomada_tripla": "Tomada tripla",
    "outro": "Outro",
}

CANAIS_24_OPCOES = [
    ("1", "Canal 1 (ideal)"),
    ("2", "Canal 2"),
    ("3", "Canal 3"),
    ("4", "Canal 4"),
    ("5", "Canal 5"),
    ("6", "Canal 6 (ideal)"),
    ("7", "Canal 7"),
    ("8", "Canal 8"),
    ("9", "Canal 9"),
    ("10", "Canal 10"),
    ("11", "Canal 11 (ideal)"),
]

CANAIS_5_OPCOES = [
    ("36", "Canal 36 (ideal)"),
    ("40", "Canal 40"),
    ("44", "Canal 44"),
    ("48", "Canal 48"),
    ("52", "Canal 52"),
    ("56", "Canal 56"),
    ("60", "Canal 60"),
    ("64", "Canal 64"),
    ("100", "Canal 100 (ideal)"),
    ("104", "Canal 104"),
    ("108", "Canal 108"),
    ("112", "Canal 112"),
    ("116", "Canal 116"),
    ("120", "Canal 120"),
    ("124", "Canal 124"),
    ("128", "Canal 128"),
    ("132", "Canal 132"),
    ("136", "Canal 136"),
    ("140", "Canal 140"),
    ("149", "Canal 149 (ideal)"),
    ("153", "Canal 153"),
    ("157", "Canal 157"),
    ("161", "Canal 161"),
]

MENU_PRINCIPAL_OPCOES = [
    ("atendimento", "🔧 Atendimento"),
    ("estoque", "🏢 Estoque"),
    ("ausente", "🚪 Ausente"),
    ("paralisada", "⏸️ Paralisada"),
    ("pendencias", "📋 Pendências"),
    ("sistema", "⚙️ Sistema"),
]

MENU_ATENDIMENTO_V5_OPCOES = [
    ("radio_assistencia", "📡 Assistência Rádio"),
    ("radio_instalacao", "📡 Instalação Rádio"),
    ("fibra_assistencia", "🌐 Fibra Assistência"),
    ("fibra_instalacao", "🏠 Fibra Instalação / Mudança"),
    ("segundo_ponto", "📶 Segundo Ponto / Troca Roteador"),
    ("link_loss", "🚨 Link Loss / Sinal Irregular"),
]

ATENDIMENTO_V5_TIPOS_MAP = {
    "radio_assistencia": "Assistência Rádio",
    "radio_instalacao": "Instalação Rádio",
    "fibra_assistencia": "Fibra Assistência",
    "fibra_instalacao": "Fibra Instalação / Mudança",
    "segundo_ponto": "Segundo Ponto / Troca Roteador",
    "link_loss": "Link Loss / Sinal Irregular",
}

TIPO_RETIRADA_OPCOES = [
    ("troca", "Troca"),
    ("cancelamento", "Cancelamento"),
]
TIPO_RETIRADA_MAP = dict(TIPO_RETIRADA_OPCOES)

ONU_OPCOES = [
    ("chima", "CHIMA"),
    ("alcatel", "ALCATEL"),
    ("cdata", "CDATA"),
    ("tplink", "TP-LINK"),
    ("huawei", "HUAWEI"),
]
ONU_MAP = {
    "chima": "CHIMA",
    "alcatel": "ALCATEL",
    "cdata": "CDATA",
    "tplink": "TP-LINK",
    "huawei": "HUAWEI",
}

DESTINO_OPCOES = [
    ("estoque_fnd", "Estoque FND"),
    ("estoque_vt", "Estoque VT"),
    ("estoque_sjrp", "Estoque SJRP"),
]
DESTINO_MAP = {
    "estoque_fnd": "Estoque FND",
    "estoque_vt": "Estoque VT",
    "estoque_sjrp": "Estoque SJRP",
}


def build_inline_keyboard(field: str, options: list[tuple[str, str]], per_row: int = 2) -> InlineKeyboardMarkup:
    buttons = []
    row = []

    for code, label in options:
        row.append(InlineKeyboardButton(label, callback_data=f"{field}|{code}"))
        if len(row) == per_row:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    return InlineKeyboardMarkup(buttons)


def menu_principal() -> InlineKeyboardMarkup:
    return build_inline_keyboard("menu", MENU_PRINCIPAL_OPCOES, per_row=2)


def menu_atendimento_v5() -> InlineKeyboardMarkup:
    return build_inline_keyboard("menu_atendimento_v5", MENU_ATENDIMENTO_V5_OPCOES, per_row=1)