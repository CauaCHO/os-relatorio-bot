from telegram import InlineKeyboardMarkup, InlineKeyboardButton

# =========================
# OPÇÕES GERAIS
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

# =========================
# MENU V5
# =========================

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

# =========================
# ATENDIMENTO
# =========================

TECNICOS_OPCOES = [
    ("caua", "Cauã Henrique"),
    ("jamildo", "Jamildo Ferreira"),
    ("erick", "Erick"),
    ("valdisney", "Valdisney"),
    ("wellington", "Wellington Arouca"),
    ("wesley", "Wesley Texeira"),
]
TECNICOS_MAP = dict(TECNICOS_OPCOES)

PROBLEMAS_OPCOES = [
    ("link_loss", "Link Loss"),
    ("mudanca_plano", "Mudança de plano"),
    ("mudanca_comodo", "Mudança de cômodo"),
    ("segundo_ponto", "Segundo ponto"),
    ("instabilidade", "Instabilidade"),
]
PROBLEMAS_MAP = {
    "link_loss": "Link Loss",
    "mudanca_plano": "Mudança de plano",
    "mudanca_comodo": "Mudança de cômodo",
    "segundo_ponto": "Segundo ponto",
    "instabilidade": "Instabilidade",
}

ENERGIA_OPCOES = [
    ("adaptador_t", "Adaptador T"),
    ("filtro", "Filtro de linha"),
    ("tomada_individual", "Tomada Individual"),
    ("tomada_dupla", "Tomada dupla"),
    ("tomada_tripla", "Tomada Tripla"),
    ("outro", "Outro"),
]
ENERGIA_MAP = {
    "adaptador_t": "Adaptador T",
    "filtro": "Filtro de linha",
    "tomada_individual": "Tomada Individual",
    "tomada_dupla": "Tomada dupla",
    "tomada_tripla": "Tomada Tripla",
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

ROTEADOR_SUGESTOES_OPCOES = [
    ("zte_h3601pe", "ZTE H3601PE"),
    ("zte_h199a", "ZTE H199A"),
    ("mercusys_ac12g", "Mercusys AC12G"),
    ("mercusys_mr80x", "Mercusys MR80X"),
    ("tplink_c20", "TP-Link C20"),
    ("tplink_c5", "TP-Link C5"),
    ("tplink_c6", "TP-Link C6"),
    ("outro", "Outros"),
]
ROTEADOR_SUGESTOES_MAP = {
    "zte_h3601pe": "ZTE H3601PE",
    "zte_h199a": "ZTE H199A",
    "mercusys_ac12g": "Mercusys AC12G",
    "mercusys_mr80x": "Mercusys MR80X",
    "tplink_c20": "TP-Link C20",
    "tplink_c5": "TP-Link C5",
    "tplink_c6": "TP-Link C6",
    "outro": "Outros",
}

LOCAL_INSTALACAO_OPCOES = [
    ("sala", "Sala"),
    ("cozinha", "Cozinha"),
    ("quarto", "Quarto"),
    ("outro", "Outros"),
]
LOCAL_INSTALACAO_MAP = {
    "sala": "Sala",
    "cozinha": "Cozinha",
    "quarto": "Quarto",
    "outro": "Outros",
}

TESTE_STATUS_OPCOES = [
    ("sim", "Sim"),
    ("nao", "Não"),
]
TESTE_STATUS_MAP = {
    "sim": "Sim",
    "nao": "Não",
}

# =========================
# ESTOQUE
# =========================

TIPO_RETIRADA_OPCOES = [
    ("troca", "Troca"),
    ("cancelamento", "Cancelamento"),
]
TIPO_RETIRADA_MAP = dict(TIPO_RETIRADA_OPCOES)

ROTEADORES_OPCOES = [
    ("zte_h3601pe_ax3000", "ZTE H3601PE AX3000"),
    ("zte_h199a_ac1200", "ZTE H199A AC1200"),
    ("mercusys_ac12g_ac1200", "Mercusys AC12G AC1200"),
    ("mercusys_mr80x_ac1800", "Mercusys MR80X AC1800"),
    ("tplink_c20", "TP-Link C20"),
    ("tplink_c5", "TP-Link C5"),
    ("tplink_c6", "TP-Link C6"),
]
ROTEADORES_MAP = {
    "zte_h3601pe_ax3000": "ZTE H3601PE AX3000",
    "zte_h199a_ac1200": "ZTE H199A AC1200",
    "mercusys_ac12g_ac1200": "Mercusys AC12G AC1200",
    "mercusys_mr80x_ac1800": "Mercusys MR80X AC1800",
    "tplink_c20": "TP-Link C20",
    "tplink_c5": "TP-Link C5",
    "tplink_c6": "TP-Link C6",
}

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

RECEBIDO_POR_OPCOES = [
    ("caua", "Cauã"),
    ("giovani", "Giovani"),
    ("dwedinei", "Dwedinei"),
    ("leonardo", "Leonardo"),
    ("kesli", "Kesli"),
]
RECEBIDO_POR_MAP = {
    "caua": "Cauã",
    "giovani": "Giovani",
    "dwedinei": "Dwedinei",
    "leonardo": "Leonardo",
    "kesli": "Kesli",
}

CIDADE_OPCOES = [
    ("fernandopolis", "Fernandópolis"),
    ("votuporanga", "Votuporanga"),
    ("sjrp", "São José do Rio Preto"),
]
CIDADE_MAP = {
    "fernandopolis": "Fernandópolis",
    "votuporanga": "Votuporanga",
    "sjrp": "São José do Rio Preto",
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