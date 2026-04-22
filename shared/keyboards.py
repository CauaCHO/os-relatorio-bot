from telegram import InlineKeyboardMarkup, InlineKeyboardButton

# =========================
# ATENDIMENTO
# =========================

TIPOS_OPCOES = [
    ("assistencia", "Assistência"),
    ("instalacao", "Instalação"),
    ("mudanca_endereco", "Mudança de endereço"),
]

TECNICOS_OPCOES = [
    ("caua", "Cauã Henrique"),
    ("jamildo", "Jamildo Ferreira"),
    ("erick", "Erick"),
    ("valdisney", "Valdisney"),
    ("wellington", "Wellington Arouca"),
    ("wesley", "Wesley Texeira"),
]

SIM_NAO_OPCOES = [
    ("sim", "Sim"),
    ("nao", "Não"),
]

PROBLEMAS_OPCOES = [
    ("link_loss", "Link Loss"),
    ("mudanca_plano", "Mudança de plano"),
    ("mudanca_comodo", "Mudança de cômodo"),
    ("segundo_ponto", "Segundo ponto"),
    ("instabilidade", "Instabilidade"),
]

ENERGIA_OPCOES = [
    ("adaptador_t", "Adaptador T"),
    ("filtro", "Filtro de linha"),
    ("tomada_individual", "Tomada Individual"),
    ("tomada_dupla", "Tomada dupla"),
    ("tomada_tripla", "Tomada Tripla"),
    ("outro", "Outro"),
]

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

TIPOS_MAP = dict(TIPOS_OPCOES)
TECNICOS_MAP = dict(TECNICOS_OPCOES)
SIM_NAO_MAP = dict(SIM_NAO_OPCOES)

PROBLEMAS_MAP = {
    "link_loss": "Link Loss",
    "mudanca_plano": "Mudança de plano",
    "mudanca_comodo": "Mudança de cômodo",
    "segundo_ponto": "Segundo ponto",
    "instabilidade": "Instabilidade",
}

ENERGIA_MAP = {
    "adaptador_t": "Adaptador T",
    "filtro": "Filtro de linha",
    "tomada_individual": "Tomada Individual",
    "tomada_dupla": "Tomada dupla",
    "tomada_tripla": "Tomada Tripla",
    "outro": "Outro",
}

# =========================
# CONFIRMAÇÃO / CONTROLE
# =========================

CONFIRMACAO_ENVIO_OPCOES = [
    ("enviar", "✅ Enviar"),
    ("editar", "✏️ Editar etapa"),
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
# ESTOQUE
# =========================

TIPO_RETIRADA_OPCOES = [
    ("troca", "Troca"),
    ("cancelamento", "Cancelamento"),
]

ROTEADORES_OPCOES = [
    ("zte_h3601pe_ax3000", "ZTE H3601PE AX3000"),
    ("zte_h199a_ac1200", "ZTE H199A AC1200"),
    ("mercusys_ac12g_ac1200", "Mercusys AC12G AC1200"),
    ("mercusys_mr80x_ac1800", "Mercusys MR80X AC1800"),
    ("tplink_c20", "TP-Link C20"),
    ("tplink_c5", "TP-Link C5"),
    ("tplink_c6", "TP-Link C6"),
]

ONU_OPCOES = [
    ("chima", "CHIMA"),
    ("alcatel", "ALCATEL"),
    ("cdata", "CDATA"),
    ("tplink", "TP-LINK"),
    ("huawei", "HUAWEI"),
]

DESTINO_OPCOES = [
    ("estoque_fnd", "Estoque FND"),
    ("estoque_vt", "Estoque VT"),
    ("estoque_sjrp", "Estoque SJRP"),
]

RECEBIDO_POR_OPCOES = [
    ("caua", "Cauã"),
    ("giovani", "Giovani"),
    ("dwedinei", "Dwedinei"),
    ("leonardo", "Leonardo"),
    ("kesli", "Kesli"),
]

CIDADE_OPCOES = [
    ("fernandopolis", "Fernandópolis"),
    ("votuporanga", "Votuporanga"),
    ("sjrp", "São José do Rio Preto"),
]

TIPO_RETIRADA_MAP = dict(TIPO_RETIRADA_OPCOES)

ROTEADORES_MAP = {
    "zte_h3601pe_ax3000": "ZTE H3601PE AX3000",
    "zte_h199a_ac1200": "ZTE H199A AC1200",
    "mercusys_ac12g_ac1200": "Mercusys AC12G AC1200",
    "mercusys_mr80x_ac1800": "Mercusys MR80X AC1800",
    "tplink_c20": "TP-Link C20",
    "tplink_c5": "TP-Link C5",
    "tplink_c6": "TP-Link C6",
}

ONU_MAP = {
    "chima": "CHIMA",
    "alcatel": "ALCATEL",
    "cdata": "CDATA",
    "tplink": "TP-LINK",
    "huawei": "HUAWEI",
}

DESTINO_MAP = {
    "estoque_fnd": "Estoque FND",
    "estoque_vt": "Estoque VT",
    "estoque_sjrp": "Estoque SJRP",
}

RECEBIDO_POR_MAP = {
    "caua": "Cauã",
    "giovani": "Giovani",
    "dwedinei": "Dwedinei",
    "leonardo": "Leonardo",
    "kesli": "Kesli",
}

CIDADE_MAP = {
    "fernandopolis": "Fernandópolis",
    "votuporanga": "Votuporanga",
    "sjrp": "São José do Rio Preto",
}

# =========================
# AUSENTE / PARALISADA
# =========================

OCORRENCIA_AUSENCIA_OPCOES = [
    ("paralisada", "O.S. paralisada"),
    ("ausencia", "Cliente ausente"),
    ("outro", "Outro"),
]

OCORRENCIA_AUSENCIA_MAP = {
    "paralisada": "O.S. paralisada",
    "ausencia": "Cliente ausente",
    "outro": "Outro",
}

# =========================
# MENU VISUAL V4
# =========================

MENU_PRINCIPAL_OPCOES = [
    ("atendimento", "🔧 Atendimento"),
    ("retirada", "📦 Retirada"),
    ("estoque", "🏢 Estoque"),
    ("ausente", "🚪 Ausente"),
    ("paralisada", "⏸️ Paralisada"),
    ("pendencias", "📋 Pendências"),
]

MENU_ATENDIMENTO_OPCOES = [
    ("assistencia", "🛠️ Assistência"),
    ("instalacao", "📡 Instalação"),
    ("mudanca", "🏠 Mudança"),
]

# =========================
# FUNÇÕES AUXILIARES
# =========================

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


def menu_atendimento() -> InlineKeyboardMarkup:
    return build_inline_keyboard("menu_atendimento", MENU_ATENDIMENTO_OPCOES, per_row=1)