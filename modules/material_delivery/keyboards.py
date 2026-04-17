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