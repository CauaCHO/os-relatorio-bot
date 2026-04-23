MODELOS_ATENDIMENTO = {
    "Assistência Rádio": {
        "codigo": "radio_assistencia",
        "secoes": [
            {
                "titulo": "SEÇÃO 1 - PADRÃO PARA FINALIZAÇÃO DE O.S ASSISTÊNCIA RÁDIO",
                "campos": [
                    {"id": "cabo_wifi", "item": "1.1", "titulo": "Informação dos equipamentos pelo cabo e Wi-Fi", "tipo": "texto"},
                    {"id": "local_instalacao", "item": "1.2", "titulo": "Local da instalação dos equipamentos", "tipo": "local_sugestao"},
                    {"id": "mapeamento_wifi", "item": "1.3", "titulo": "Feito mapeamento de todo o local pelo WiFiman", "tipo": "sim_nao"},
                    {"id": "iptv_tvbox", "item": "1.4", "titulo": "Verificação de IPTV/TVBOX", "tipo": "sim_nao"},
                    {"id": "dados_antena", "item": "1.5", "titulo": "Informação da tela principal da antena, alinhamento, sinal, TX/RX", "tipo": "texto"},
                    {"id": "teste_realizado", "item": "1.6", "titulo": "Realização de teste de velocidade", "tipo": "sim_nao"},
                    {"id": "teste_velocidade", "item": "1.6.1", "titulo": "Valor do teste de velocidade", "tipo": "speed", "condicao": {"campo": "teste_realizado", "valor": "Sim"}},
                    {"id": "verificou_melhor_canal", "item": "1.7", "titulo": "Verificação de melhor canal da rede Wi-Fi", "tipo": "sim_nao"},
                    {"id": "canal_24", "item": "1.7.1", "titulo": "Melhor canal da rede 2.4Ghz", "tipo": "canal24", "condicao": {"campo": "verificou_melhor_canal", "valor": "Sim"}},
                    {"id": "canal_5", "item": "1.7.2", "titulo": "Melhor canal da rede 5Ghz", "tipo": "canal5", "condicao": {"campo": "verificou_melhor_canal", "valor": "Sim"}},
                    {"id": "houve_dano", "item": "1.8", "titulo": "Se houve dano no local", "tipo": "sim_nao"},
                    {"id": "descricao_dano", "item": "1.8.1", "titulo": "Descrição do dano no local", "tipo": "texto", "condicao": {"campo": "houve_dano", "valor": "Sim"}},
                    {"id": "config_padrao", "item": "1.9", "titulo": "Configurações da antena e do roteador dentro do padrão", "tipo": "sim_nao"},
                    {"id": "acesso_remoto", "item": "1.10", "titulo": "Verificação do acesso remoto", "tipo": "sim_nao"},
                    {"id": "problema_procedimento", "item": "1.11", "titulo": "Problema do cliente e procedimento realizado no local", "tipo": "texto"},
                ],
            },
            {
                "titulo": "SEÇÃO 2 - ORGANIZAÇÃO ESTÉTICA DO PADRÃO DE INSTALAÇÃO",
                "campos": [
                    {"id": "energia", "item": "2.1", "titulo": "Método de instalação em T, tomada ou filtro de linha", "tipo": "energia"},
                    {"id": "organizacao", "item": "2.2", "titulo": "Organização da instalação ou reorganização", "tipo": "sim_nao"},
                ],
            },
            {
                "titulo": "SEÇÃO 3 - MATERIAL UTILIZADO/RETIRADO",
                "campos": [
                    {"id": "materiais_utilizados", "item": "3.1", "titulo": "Material utilizado", "tipo": "texto"},
                    {"id": "materiais_retirados", "item": "3.1.1", "titulo": "Material retirado", "tipo": "texto"},
                    {"id": "material_linkado", "item": "3.2", "titulo": "Material linkado no MK de acordo com o utilizado/retirado", "tipo": "sim_nao"},
                ],
            },
        ],
    },
    "Instalação Rádio": {
        "codigo": "radio_instalacao",
        "secoes": [
            {
                "titulo": "SEÇÃO 1 - PADRÃO PARA FINALIZAÇÃO DE O.S INSTALAÇÃO RÁDIO",
                "campos": [
                    {"id": "cabo_wifi", "item": "1.1", "titulo": "Informação dos equipamentos pelo cabo e Wi-Fi", "tipo": "texto"},
                    {"id": "local_instalacao", "item": "1.2", "titulo": "Local da instalação dos equipamentos", "tipo": "local_sugestao"},
                    {"id": "mapeamento_wifi", "item": "1.3", "titulo": "Feito mapeamento de todo o local pelo WiFiman", "tipo": "sim_nao"},
                    {"id": "iptv_tvbox", "item": "1.4", "titulo": "Verificação de IPTV/TVBOX", "tipo": "sim_nao"},
                    {"id": "dados_antena", "item": "1.5", "titulo": "Informação da tela principal da antena, alinhamento, sinal, TX/RX", "tipo": "texto"},
                    {"id": "houve_dano", "item": "1.6", "titulo": "Se houve dano no local", "tipo": "sim_nao"},
                    {"id": "descricao_dano", "item": "1.6.1", "titulo": "Descrição do dano no local", "tipo": "texto", "condicao": {"campo": "houve_dano", "valor": "Sim"}},
                    {"id": "teste_realizado", "item": "1.7", "titulo": "Realização de teste de velocidade", "tipo": "sim_nao"},
                    {"id": "teste_velocidade", "item": "1.7.1", "titulo": "Valor do teste de velocidade", "tipo": "speed", "condicao": {"campo": "teste_realizado", "valor": "Sim"}},
                    {"id": "verificou_melhor_canal", "item": "1.8", "titulo": "Verificação de melhor canal da rede Wi-Fi", "tipo": "sim_nao"},
                    {"id": "canal_24", "item": "1.8.1", "titulo": "Melhor canal da rede 2.4Ghz", "tipo": "canal24", "condicao": {"campo": "verificou_melhor_canal", "valor": "Sim"}},
                    {"id": "canal_5", "item": "1.8.2", "titulo": "Melhor canal da rede 5Ghz", "tipo": "canal5", "condicao": {"campo": "verificou_melhor_canal", "valor": "Sim"}},
                    {"id": "fixacao", "item": "1.9", "titulo": "Forma que o equipamento foi fixado (antena, roteador e fonte POE)", "tipo": "texto"},
                    {"id": "config_padrao", "item": "1.10", "titulo": "Configurações da antena e do roteador dentro do padrão", "tipo": "sim_nao"},
                    {"id": "acesso_remoto", "item": "1.11", "titulo": "Verificação do acesso remoto", "tipo": "sim_nao"},
                    {"id": "pos_venda", "item": "1.12", "titulo": "Realizado o pós vendas imediato", "tipo": "sim_nao"},
                    {"id": "motivo_sem_pos_venda", "item": "1.12.1", "titulo": "Motivo do não pós-venda", "tipo": "texto", "condicao": {"campo": "pos_venda", "valor": "Não"}},
                ],
            },
            {
                "titulo": "SEÇÃO 2 - ORGANIZAÇÃO ESTÉTICA DO PADRÃO DE INSTALAÇÃO",
                "campos": [
                    {"id": "energia", "item": "2.1", "titulo": "Método de instalação em T, tomada ou filtro de linha", "tipo": "energia"},
                    {"id": "organizacao", "item": "2.2", "titulo": "Organização da instalação ou reorganização", "tipo": "sim_nao"},
                ],
            },
            {
                "titulo": "SEÇÃO 3 - MATERIAL UTILIZADO/RETIRADO",
                "campos": [
                    {"id": "materiais_utilizados", "item": "3.1", "titulo": "Material utilizado", "tipo": "texto"},
                    {"id": "materiais_retirados", "item": "3.1.1", "titulo": "Material retirado", "tipo": "texto"},
                    {"id": "material_linkado", "item": "3.2", "titulo": "Material linkado no MK de acordo com o utilizado/retirado", "tipo": "sim_nao"},
                ],
            },
        ],
    },
    "Fibra Assistência": {
        "codigo": "fibra_assistencia",
        "secoes": [
            {
                "titulo": "SEÇÃO 1 - PADRÃO DE FINALIZAÇÃO",
                "campos": [
                    {"id": "cabo_wifi", "item": "1.1", "titulo": "Informação dos equipamentos pelo cabo e Wi-Fi", "tipo": "texto"},
                    {"id": "local_instalacao", "item": "1.2", "titulo": "Local da instalação dos equipamentos", "tipo": "local_sugestao"},
                    {"id": "mapeamento_wifi", "item": "1.3", "titulo": "Feito mapeamento de todo o local pelo WiFiman", "tipo": "sim_nao"},
                    {"id": "iptv_tvbox", "item": "1.4", "titulo": "Verificação de IPTV/TVBOX", "tipo": "sim_nao"},
                    {"id": "sinal_fibra", "item": "1.5", "titulo": "Medição de sinal da Fibra", "tipo": "sinal"},
                    {"id": "houve_dano", "item": "1.6", "titulo": "Informado se houve dano no local", "tipo": "sim_nao"},
                    {"id": "descricao_dano", "item": "1.6.1", "titulo": "Descrição do dano no local", "tipo": "texto", "condicao": {"campo": "houve_dano", "valor": "Sim"}},
                    {"id": "orientacao_24_5", "item": "1.7", "titulo": "Orientado o cliente sobre a rede 2.4Ghz e 5.8Ghz", "tipo": "sim_nao"},
                    {"id": "teste_realizado", "item": "1.8", "titulo": "Realização de teste de velocidade", "tipo": "sim_nao"},
                    {"id": "teste_velocidade", "item": "1.8.1", "titulo": "Valor do teste de velocidade", "tipo": "speed", "condicao": {"campo": "teste_realizado", "valor": "Sim"}},
                    {"id": "verificou_melhor_canal", "item": "1.9", "titulo": "Verificação de melhor canal da rede Wi-Fi", "tipo": "sim_nao"},
                    {"id": "canal_24", "item": "1.9.1", "titulo": "Melhor canal da rede 2.4Ghz", "tipo": "canal24", "condicao": {"campo": "verificou_melhor_canal", "valor": "Sim"}},
                    {"id": "canal_5", "item": "1.9.2", "titulo": "Melhor canal da rede 5Ghz", "tipo": "canal5", "condicao": {"campo": "verificou_melhor_canal", "valor": "Sim"}},
                    {"id": "config_padrao", "item": "1.10", "titulo": "Configurações do roteador dentro do padrão", "tipo": "sim_nao"},
                    {"id": "acesso_remoto", "item": "1.11", "titulo": "Verificação do acesso remoto", "tipo": "sim_nao"},
                    {"id": "equipamentos_atualizados", "item": "1.12", "titulo": "Verificação de equipamentos atualizados (ONU e roteador)", "tipo": "sim_nao"},
                    {"id": "problema_procedimento", "item": "1.13", "titulo": "Problema do cliente e procedimento realizado no local", "tipo": "texto"},
                ],
            },
            {
                "titulo": "SEÇÃO 2 - ORGANIZAÇÃO ESTÉTICA DO PADRÃO DE INSTALAÇÃO",
                "campos": [
                    {"id": "energia", "item": "2.1", "titulo": "Método de instalação em T, tomada ou filtro de linha", "tipo": "energia"},
                    {"id": "organizacao", "item": "2.2", "titulo": "Organização da instalação ou reorganização", "tipo": "sim_nao"},
                ],
            },
            {
                "titulo": "SEÇÃO 3 - MATERIAL UTILIZADO/RETIRADO",
                "campos": [
                    {"id": "materiais_utilizados", "item": "3.1", "titulo": "Material utilizado", "tipo": "texto"},
                    {"id": "materiais_retirados", "item": "3.1.1", "titulo": "Material retirado", "tipo": "texto"},
                    {"id": "material_linkado", "item": "3.2", "titulo": "Material linkado no MK de acordo com o utilizado/retirado", "tipo": "sim_nao"},
                ],
            },
        ],
    },
    "Fibra Instalação / Mudança": {
        "codigo": "fibra_instalacao",
        "secoes": [
            {
                "titulo": "SEÇÃO 1 - PADRÃO DE FINALIZAÇÃO",
                "campos": [
                    {"id": "cabo_wifi", "item": "1.1", "titulo": "Informação dos equipamentos pelo cabo e Wi-Fi", "tipo": "texto"},
                    {"id": "local_instalacao", "item": "1.2", "titulo": "Local da instalação dos equipamentos", "tipo": "local_sugestao"},
                    {"id": "mapeamento_wifi", "item": "1.3", "titulo": "Feito mapeamento de todo o local pelo WiFiman", "tipo": "sim_nao"},
                    {"id": "iptv_tvbox", "item": "1.4", "titulo": "Verificação de IPTV/TVBOX", "tipo": "sim_nao"},
                    {"id": "sinal_cto", "item": "1.5", "titulo": "Medição de sinal da Fibra na CTO", "tipo": "sinal"},
                    {"id": "sinal_fibra", "item": "1.5.1", "titulo": "Medição de sinal da Fibra na casa do cliente", "tipo": "sinal"},
                    {"id": "houve_dano", "item": "1.6", "titulo": "Informado se houve dano no local", "tipo": "sim_nao"},
                    {"id": "descricao_dano", "item": "1.6.1", "titulo": "Descrição do dano no local", "tipo": "texto", "condicao": {"campo": "houve_dano", "valor": "Sim"}},
                    {"id": "orientacao_24_5", "item": "1.7", "titulo": "Orientado o cliente sobre a rede 2.4Ghz e 5.8Ghz", "tipo": "sim_nao"},
                    {"id": "teste_realizado", "item": "1.8", "titulo": "Realização de teste de velocidade", "tipo": "sim_nao"},
                    {"id": "teste_velocidade", "item": "1.8.1", "titulo": "Valor do teste de velocidade", "tipo": "speed", "condicao": {"campo": "teste_realizado", "valor": "Sim"}},
                    {"id": "verificou_melhor_canal", "item": "1.9", "titulo": "Verificação de melhor canal da rede Wi-Fi", "tipo": "sim_nao"},
                    {"id": "canal_24", "item": "1.9.1", "titulo": "Melhor canal da rede 2.4Ghz", "tipo": "canal24", "condicao": {"campo": "verificou_melhor_canal", "valor": "Sim"}},
                    {"id": "canal_5", "item": "1.9.2", "titulo": "Melhor canal da rede 5Ghz", "tipo": "canal5", "condicao": {"campo": "verificou_melhor_canal", "valor": "Sim"}},
                    {"id": "fixacao", "item": "1.10", "titulo": "Forma que o equipamento foi fixado (Roteador + ONU)", "tipo": "texto"},
                    {"id": "config_padrao", "item": "1.11", "titulo": "Configurações do roteador dentro do padrão", "tipo": "sim_nao"},
                    {"id": "acesso_remoto", "item": "1.12", "titulo": "Verificação do acesso remoto", "tipo": "sim_nao"},
                    {"id": "pos_venda", "item": "1.13", "titulo": "Realizado o pós vendas imediato", "tipo": "sim_nao"},
                    {"id": "motivo_sem_pos_venda", "item": "1.13.1", "titulo": "Motivo do não pós-venda", "tipo": "texto", "condicao": {"campo": "pos_venda", "valor": "Não"}},
                    {"id": "retirada_cabo_antigo", "item": "1.14", "titulo": "Em mudança de endereço, foi retirado o cabo da instalação antiga", "tipo": "texto"},
                ],
            },
            {
                "titulo": "SEÇÃO 2 - ORGANIZAÇÃO ESTÉTICA DO PADRÃO DE INSTALAÇÃO",
                "campos": [
                    {"id": "energia", "item": "2.1", "titulo": "Método de instalação em T, tomada ou filtro de linha", "tipo": "energia"},
                    {"id": "organizacao", "item": "2.2", "titulo": "Organização da instalação ou reorganização", "tipo": "sim_nao"},
                ],
            },
            {
                "titulo": "SEÇÃO 3 - MATERIAL UTILIZADO/RETIRADO",
                "campos": [
                    {"id": "materiais_utilizados", "item": "3.1", "titulo": "Material utilizado", "tipo": "texto"},
                    {"id": "materiais_retirados", "item": "3.1.1", "titulo": "Material retirado", "tipo": "texto"},
                    {"id": "material_linkado", "item": "3.2", "titulo": "Material linkado no MK de acordo com o utilizado/retirado", "tipo": "sim_nao"},
                ],
            },
        ],
    },
    "Segundo Ponto / Troca Roteador": {
        "codigo": "segundo_ponto",
        "secoes": [
            {
                "titulo": "SEÇÃO 1 - PADRÃO DE FINALIZAÇÃO",
                "campos": [
                    {"id": "modelo_segundo_roteador", "item": "1.1", "titulo": "Modelo do roteador do segundo ponto (SSID e senha)", "tipo": "roteador_sugestao"},
                    {"id": "ssid_segundo_roteador", "item": "1.1.1", "titulo": "SSID do segundo ponto", "tipo": "texto"},
                    {"id": "senha_segundo_roteador", "item": "1.1.2", "titulo": "Senha do segundo ponto", "tipo": "texto"},
                    {"id": "local_instalacao", "item": "1.2", "titulo": "Local da instalação dos equipamentos", "tipo": "local_sugestao"},
                    {"id": "config_padrao", "item": "1.3", "titulo": "Configurações do roteador dentro do padrão (primeiro e segundo ponto)", "tipo": "sim_nao"},
                    {"id": "passagem_cabo", "item": "1.4", "titulo": "Houve passagem de cabo de rede com testes", "tipo": "sim_nao"},
                    {"id": "teste_realizado", "item": "1.5", "titulo": "Realização de teste de velocidade", "tipo": "sim_nao"},
                    {"id": "teste_velocidade", "item": "1.5.1", "titulo": "Valor do teste de velocidade", "tipo": "speed", "condicao": {"campo": "teste_realizado", "valor": "Sim"}},
                    {"id": "sinal_fibra", "item": "1.6", "titulo": "Medição de sinal da Fibra", "tipo": "sinal"},
                    {"id": "houve_dano", "item": "1.7", "titulo": "Informado se houve dano no local", "tipo": "sim_nao"},
                    {"id": "descricao_dano", "item": "1.7.1", "titulo": "Descrição do dano no local", "tipo": "texto", "condicao": {"campo": "houve_dano", "valor": "Sim"}},
                    {"id": "orientacao_24_5", "item": "1.8", "titulo": "Orientado o cliente sobre a rede 2.4Ghz e 5.8Ghz", "tipo": "sim_nao"},
                    {"id": "verificou_melhor_canal", "item": "1.9", "titulo": "Verificação de melhor canal da rede Wi-Fi", "tipo": "sim_nao"},
                    {"id": "canal_24", "item": "1.9.1", "titulo": "Melhor canal da rede 2.4Ghz", "tipo": "canal24", "condicao": {"campo": "verificou_melhor_canal", "valor": "Sim"}},
                    {"id": "canal_5", "item": "1.9.2", "titulo": "Melhor canal da rede 5Ghz", "tipo": "canal5", "condicao": {"campo": "verificou_melhor_canal", "valor": "Sim"}},
                    {"id": "fixacao", "item": "1.10", "titulo": "Forma que o equipamento foi fixado", "tipo": "texto"},
                    {"id": "equipamentos_atualizados", "item": "1.11", "titulo": "Verificação dos equipamentos atualizados (ONU + Roteador)", "tipo": "sim_nao"},
                    {"id": "acesso_remoto", "item": "1.12", "titulo": "Verificação do acesso remoto do primeiro ponto", "tipo": "sim_nao"},
                    {"id": "mapeamento_primeiro_segundo", "item": "1.13", "titulo": "Feito mapeamento de todo o local pelo WiFiman do primeiro e segundo ponto", "tipo": "sim_nao"},
                ],
            },
            {
                "titulo": "SEÇÃO 2 - ORGANIZAÇÃO ESTÉTICA DO PADRÃO DE INSTALAÇÃO",
                "campos": [
                    {"id": "energia", "item": "2.1", "titulo": "Método de instalação em T, tomada ou filtro de linha", "tipo": "energia"},
                    {"id": "organizacao", "item": "2.2", "titulo": "Organização da instalação ou reorganização", "tipo": "sim_nao"},
                ],
            },
            {
                "titulo": "SEÇÃO 3 - MATERIAL UTILIZADO/RETIRADO",
                "campos": [
                    {"id": "materiais_utilizados", "item": "3.1", "titulo": "Material utilizado", "tipo": "texto"},
                    {"id": "materiais_retirados", "item": "3.1.1", "titulo": "Material retirado", "tipo": "texto"},
                    {"id": "material_linkado", "item": "3.2", "titulo": "Material linkado no MK de acordo com o utilizado/retirado", "tipo": "sim_nao"},
                ],
            },
        ],
    },
    "Link Loss / Sinal Irregular": {
        "codigo": "link_loss",
        "secoes": [
            {
                "titulo": "SEÇÃO 1 - PADRÃO DE FINALIZAÇÃO",
                "campos": [
                    {"id": "motivo_link_loss", "item": "1.1", "titulo": "Motivo do Link Loss e resolução do problema", "tipo": "texto"},
                    {"id": "local_instalacao", "item": "1.2", "titulo": "Local da instalação dos equipamentos", "tipo": "local_sugestao"},
                    {"id": "compatibilidade_roteador", "item": "1.3", "titulo": "Verificação do modelo do roteador e compatibilidade com o plano", "tipo": "texto"},
                    {"id": "teste_realizado", "item": "1.4", "titulo": "Realização de teste de velocidade", "tipo": "sim_nao"},
                    {"id": "teste_velocidade", "item": "1.4.1", "titulo": "Valor do teste de velocidade", "tipo": "speed", "condicao": {"campo": "teste_realizado", "valor": "Sim"}},
                    {"id": "sinal_fibra", "item": "1.5", "titulo": "Medição de sinal da Fibra", "tipo": "sinal"},
                    {"id": "houve_dano", "item": "1.6", "titulo": "Informado se houve dano no local", "tipo": "sim_nao"},
                    {"id": "descricao_dano", "item": "1.6.1", "titulo": "Descrição do dano no local", "tipo": "texto", "condicao": {"campo": "houve_dano", "valor": "Sim"}},
                    {"id": "verificou_melhor_canal", "item": "1.7", "titulo": "Verificação de melhor canal da rede Wi-Fi", "tipo": "sim_nao"},
                    {"id": "canal_24", "item": "1.7.1", "titulo": "Melhor canal da rede 2.4Ghz", "tipo": "canal24", "condicao": {"campo": "verificou_melhor_canal", "valor": "Sim"}},
                    {"id": "canal_5", "item": "1.7.2", "titulo": "Melhor canal da rede 5Ghz", "tipo": "canal5", "condicao": {"campo": "verificou_melhor_canal", "valor": "Sim"}},
                    {"id": "config_padrao", "item": "1.8", "titulo": "Configurações do roteador dentro do padrão", "tipo": "sim_nao"},
                    {"id": "equipamentos_atualizados", "item": "1.9", "titulo": "Verificação de equipamentos atualizados (ONU e Roteador)", "tipo": "sim_nao"},
                    {"id": "acesso_remoto", "item": "1.10", "titulo": "Verificação do acesso remoto", "tipo": "sim_nao"},
                ],
            },
            {
                "titulo": "SEÇÃO 2 - ORGANIZAÇÃO ESTÉTICA DO PADRÃO DE INSTALAÇÃO",
                "campos": [
                    {"id": "energia", "item": "2.1", "titulo": "Método de instalação em T, tomada ou filtro de linha", "tipo": "energia"},
                    {"id": "organizacao", "item": "2.2", "titulo": "Organização da instalação ou reorganização", "tipo": "sim_nao"},
                ],
            },
            {
                "titulo": "SEÇÃO 3 - MATERIAL UTILIZADO/RETIRADO",
                "campos": [
                    {"id": "materiais_utilizados", "item": "3.1", "titulo": "Material utilizado", "tipo": "texto"},
                    {"id": "materiais_retirados", "item": "3.1.1", "titulo": "Material retirado", "tipo": "texto"},
                    {"id": "material_linkado", "item": "3.2", "titulo": "Material linkado no MK de acordo com o utilizado/retirado", "tipo": "sim_nao"},
                ],
            },
        ],
    },
}