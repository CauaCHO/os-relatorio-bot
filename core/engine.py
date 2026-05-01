import json
from pathlib import Path
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from config import CHAT_ID, RELATORIOS_FILE, PENDENCIAS_FILE, CONFIG_FILE, CONFIG_PASSWORD, CONFIG_ALLOWED_USERS, CONFIG_ALLOWED_IDS
from shared.keyboards import kb, MENU, CONFIRM, SIM_NAO, SEGUNDO_PONTO
from shared.storage import read_json, write_json, append_json
from shared.formatters import esc, fmt, br_now_hm, calcular_tempo
SESSIONS={}
def load_models(): return json.loads(Path('models/assistencias.json').read_text(encoding='utf-8'))
def app_config():
    d={'allowed_config_users':CONFIG_ALLOWED_USERS,'allowed_config_ids':CONFIG_ALLOWED_IDS,'config_password':CONFIG_PASSWORD,'tecnicos':['Cauã Henrique','Jamildo Ferreira','Erick','Valdisney','Wellington Arouca','Wesley Texeira'],'roteadores':['ZTE H3601PE','ZTE H199A','Mercusys AC12G','Mercusys MR80X','TP-Link C20','TP-Link C5','TP-Link C6','Outros'],'locais':['Sala','Cozinha','Quarto','Escritório','Área externa','Outro'],'estoques':{'Estoque FND':{'cidade':'Fernandópolis','recebedores':['Cauã']},'Estoque VT':{'cidade':'Votuporanga','recebedores':['Giovani','Dwedinei','Leonardo']},'Estoque SJRP':{'cidade':'São José do Rio Preto','recebedores':['Kesli']}}}
    data=read_json(CONFIG_FILE,d); changed=False
    for k,v in d.items():
        if k not in data: data[k]=v; changed=True
    if changed: write_json(CONFIG_FILE,data)
    return data
def user_label(u): return f'@{u.username}' if u.username else (u.first_name or str(u.id))
async def send_group(context,text,user):
    if not CHAT_ID: return
    full=f'👤 <b>Preenchido por:</b> {esc(user_label(user))}\n\n'+text
    for i in range(0,len(full),3900): await context.bot.send_message(chat_id=CHAT_ID,text=full[i:i+3900],parse_mode='HTML')
async def start(update,context): await update.effective_message.reply_text('🚀 <b>Sistema Flash Reports v6</b>\n\nSelecione uma opção:',parse_mode='HTML',reply_markup=kb('menu',MENU,2))
async def assistencia_cmd(update,context): await show_assistencias(update.effective_message)
async def retirada_cmd(update,context): await start_simple(update,'retirada')
async def estoque_cmd(update,context): await start_simple(update,'estoque')
async def ausente_cmd(update,context): await start_simple(update,'ausente')
async def paralisada_cmd(update,context): await show_paralisada(update.effective_message)
async def pendencias_cmd(update,context): await show_pendencias(update.effective_message)
async def baixar_pendencia_cmd(update,context):
    if not context.args: await update.effective_message.reply_text('Use assim:\n/baixar_pendencia 123456'); return
    baixa_pendencia(context.args[0]); await update.effective_message.reply_text(f'✅ O.S. {context.args[0]} removida das pendências.')
async def config_cmd(update,context):
    cfg=app_config(); username=update.effective_user.username; uid=update.effective_user.id
    allowed=(username and username in [u.lstrip('@') for u in cfg['allowed_config_users']]) or str(uid) in [str(x) for x in cfg['allowed_config_ids']]
    if not allowed: await update.effective_message.reply_text(f'⛔ Sem permissão.\n\n👤 @{username or "-"}\n🆔 {uid}'); return
    SESSIONS[uid]={'module':'config','step':'senha'}; await update.effective_message.reply_text(f'🔐 Digite a senha do /config:\n\n👤 @{username or "-"}\n🆔 {uid}')
async def show_assistencias(message):
    opts=[(c,m['title']) for c,m in load_models().items()]
    await message.reply_text('🔧 Escolha o modelo de assistência:',reply_markup=kb('assist',opts,1))
async def show_paralisada(message): await message.reply_text('⏸️ Módulo O.S. Paralisada:',reply_markup=kb('paralisada_menu',[('nova','⏸️ Paralisar nova O.S.'),('lista','📋 Ver / desparalisar')],1))
async def show_pendencias(message):
    pend=read_json(PENDENCIAS_FILE,[])
    if not pend: await message.reply_text('✅ Nenhuma pendência/paralisada no momento.'); return
    lines=['📋 <b>Pendências / O.S. Paralisadas</b>','']; opts=[]
    for p in pend:
        lines.append(f"• O.S. {esc(p.get('os'))} — {esc(p.get('tipo'))}"); opts.append((str(p.get('os','-')),f"✅ Baixar {p.get('os','-')}"))
    await message.reply_text('\n'.join(lines),parse_mode='HTML',reply_markup=kb('baixar_pend',opts,1))
def baixa_pendencia(osn): write_json(PENDENCIAS_FILE,[p for p in read_json(PENDENCIAS_FILE,[]) if str(p.get('os'))!=str(osn)])
def salvar_pendencia(dados,tipo):
    pend=[p for p in read_json(PENDENCIAS_FILE,[]) if str(p.get('os'))!=str(dados.get('os'))]
    pend.append({'os':dados.get('os'),'tipo':tipo,'dados':dados}); write_json(PENDENCIAS_FILE,pend)
async def start_assistencia(update,code):
    m=load_models()[code]; SESSIONS[update.effective_user.id]={'module':'assistencia','model':m,'index':0,'data':{'tipo':m['title']}}
    await ask_current(update.effective_message,SESSIONS[update.effective_user.id])
async def start_simple(update,module,prefill=None):
    flows={'retirada':{'title':'🔧 RETIRADA DE EQUIPAMENTOS','fields':[['os','O.S','os','📌 Digite o número da O.S.:'],['equipamentos','Equipamentos recolhidos','materiais','📦 Informe equipamentos retirados da casa do cliente:'],['obs','Observações','texto','📝 Observações:']]},'estoque':{'title':'📦 ENTRADA DE EQUIPAMENTOS NO ESTOQUE','fields':[['os','O.S','os','📌 Digite o número da O.S.:'],['tipo_os','Tipo','texto','🔧 Tipo da retirada/troca/cancelamento:'],['equipamentos','Equipamentos recebidos','materiais','📦 Informe equipamentos recebidos:'],['destino','Destino','estoque_destino','🏢 Selecione o destino:'],['obs','Observações','texto','📝 Observações:']]},'ausente':{'title':'🚫 CLIENTE AUSENTE','fields':[['os','O.S','os','📌 Digite o número da O.S.:'],['tentativas','Tentativas de contato','texto','📞 Tentativas de contato:'],['situacao','Situação','texto','📌 Qual a situação?'],['obs','Observações','texto','📝 Observações:']]},'paralisada':{'title':'⏸️ O.S. PARALISADA','fields':[['os','O.S','os','📌 Digite o número da O.S.:'],['motivo','Motivo da paralisação','texto','⏸️ Motivo da paralisação:'],['situacao','Situação atual','texto','📌 Situação atual:'],['obs','Observações','texto','📝 Observações:']]}}
    SESSIONS[update.effective_user.id]={'module':module,'model':flows[module],'index':0,'data':prefill or {}}
    await ask_current(update.effective_message,SESSIONS[update.effective_user.id])
def get_fields(s):
    if s['module']=='assistencia': return [['os','O.S','os','📌 Digite o número da O.S.:'],['inicio','Hora iniciada','hora','⏰ Que horas começou? Exemplo: 15:30'],['tec_ext','Técnico externo','tecnico','👨‍🔧 Técnico externo:'],['tec_int','Técnico interno','tecnico','🧑‍💻 Técnico interno:']]+s['model']['fields']
    return s['model']['fields']
def cond_ok(f,data):
    if len(f)<5: return True
    k,v=f[4].split('=',1); return data.get(k)==v
async def ask_current(message,s):
    fields=get_fields(s)
    while s['index']<len(fields) and not cond_ok(fields[s['index']],s['data']): s['index']+=1
    if s['index']>=len(fields): await show_review(message,s); return
    f=fields[s['index']]; typ=f[2]
    if typ=='sim_nao': await message.reply_text(f[3],reply_markup=kb('answer',SIM_NAO,2))
    elif typ=='segundo_ponto': await message.reply_text(f[3],reply_markup=kb('answer',SEGUNDO_PONTO,2))
    elif typ=='tecnico': await message.reply_text(f[3],reply_markup=kb('answer',[(x,x) for x in app_config()['tecnicos']],1))
    elif typ=='roteador': await message.reply_text(f[3],reply_markup=kb('answer',[(x,x) for x in app_config()['roteadores']],1))
    elif typ=='local': await message.reply_text(f[3],reply_markup=kb('answer',[(x,x) for x in app_config()['locais']],2))
    elif typ=='estoque_destino': await message.reply_text(f[3],reply_markup=kb('answer',[(x,x) for x in app_config()['estoques'].keys()],1))
    else: await message.reply_text(f[3],reply_markup=ReplyKeyboardRemove())
async def show_review(message,s):
    lines=['📋 <b>Revisão antes do envio</b>','']
    for f in get_fields(s):
        if cond_ok(f,s['data']): lines.append(f'<b>{esc(f[1])}:</b> {esc(s["data"].get(f[0],"-"))}')
    await message.reply_text('\n'.join(lines),parse_mode='HTML'); await message.reply_text('Escolha uma opção:',reply_markup=kb('confirm',CONFIRM,1))
def build_report(s):
    data=s['data']; title=s['model']['title']; module=s['module']
    if module=='assistencia':
        data['fim']=data.get('fim') or br_now_hm(); tempo=calcular_tempo(data.get('inicio','-'),data.get('fim','-'))
        lines=[f'<b>{esc(title)}</b>','',f'<b>O.S:</b> {esc(data.get("os"))}',f'<b>Iniciada:</b> {esc(data.get("inicio"))}',f'<b>Finalizada:</b> {esc(data.get("fim"))}',f'<b>Tempo gasto:</b> {tempo}',f'<b>Técnico externo:</b> {esc(data.get("tec_ext"))}',f'<b>Técnico interno:</b> {esc(data.get("tec_int"))}','']
    else: lines=[f'<b>{esc(title)}</b>','']
    for f in get_fields(s):
        key,label,typ=f[0],f[1],f[2]
        if module=='assistencia' and key in ['inicio','tec_ext','tec_int']: continue
        if not cond_ok(f,data): continue
        if key=='os': lines += [f'<b>O.S:</b> {esc(data.get(key))}','']; continue
        lines += [f'<b>{esc(label)}:</b>',fmt(typ,data.get(key,'-')),'']
    if module=='retirada': lines.append('@FlashNetCobranca')
    if module=='ausente': lines.append('@flashnetagendamento')
    if module=='estoque':
        cfg=app_config()['estoques'].get(data.get('destino'),{})
        lines += [f'<b>Recebido por:</b> {esc(", ".join(cfg.get("recebedores",[])) or "-")}',f'<b>Cidade:</b> {esc(cfg.get("cidade","-"))}']
    return '\n'.join(lines).strip()
async def finalize(update,context,s):
    rep=build_report(s); await send_group(context,rep,update.effective_user)
    append_json(RELATORIOS_FILE,{'module':s['module'],'data':s['data'],'report':rep,'user':user_label(update.effective_user)})
    if s['module']=='paralisada': salvar_pendencia(s['data'],'O.S. paralisada')
    if s['module']=='ausente': salvar_pendencia(s['data'],'Cliente ausente')
    if s['module']=='assistencia' and s['data'].get('os'): baixa_pendencia(s['data'].get('os'))
    if s['module']=='retirada': await update.effective_message.reply_text('✅ Relatório enviado.\n\nDeseja gerar entrada no estoque?',reply_markup=kb('after_retirada',SIM_NAO,2)); return
    SESSIONS.pop(update.effective_user.id,None); await update.effective_message.reply_text('✅ Relatório enviado com sucesso.')
async def handle_callback(update,context):
    q=update.callback_query; await q.answer(); uid=q.from_user.id; prefix,value=q.data.split('|',1)
    if prefix=='menu':
        if value=='assistencias': await show_assistencias(q.message)
        elif value in ['retirada','estoque','ausente']: await start_simple(update,value)
        elif value=='paralisada': await show_paralisada(q.message)
        elif value=='pendencias': await show_pendencias(q.message)
        elif value=='config': await config_cmd(update,context)
        return
    if prefix=='assist': await start_assistencia(update,value); return
    if prefix=='paralisada_menu': await (start_simple(update,'paralisada') if value=='nova' else show_pendencias(q.message)); return
    if prefix=='baixar_pend': baixa_pendencia(value); await q.message.reply_text(f'✅ O.S. {value} removida das pendências.'); return
    if uid not in SESSIONS: return
    s=SESSIONS[uid]
    if prefix=='answer':
        f=get_fields(s)[s['index']]; val=value
        if f[2]=='sim_nao': val='Sim' if value=='sim' else 'Não'
        if f[2]=='segundo_ponto': val={'roteador':'Roteador','pc':'PC','tv':'TV','camera':'Câmera','outro':'Outro'}.get(value,value)
        s['data'][f[0]]=val; s['index']+=1; await ask_current(q.message,s); return
    if prefix=='confirm':
        if value=='enviar': await finalize(update,context,s)
        elif value=='cancelar': SESSIONS.pop(uid,None); await q.message.reply_text('❌ Fluxo cancelado.')
        elif value=='editar': await q.message.reply_text('✏️ Escolha o campo:',reply_markup=kb('edit',[(str(i),f[1][:55]) for i,f in enumerate(get_fields(s)) if cond_ok(f,s['data'])],1))
        return
    if prefix=='edit': s['index']=int(value); await ask_current(q.message,s); return
    if prefix=='after_retirada':
        old=s['data']; SESSIONS.pop(uid,None)
        if value=='sim': await start_simple(update,'estoque',{'os':old.get('os'), 'equipamentos':old.get('equipamentos')})
        else: await q.message.reply_text('👍 Fluxo finalizado.')
async def handle_message(update,context):
    uid=update.effective_user.id
    if uid not in SESSIONS: return
    s=SESSIONS[uid]; text=update.effective_message.text.strip()
    if s['module']=='config': await update.effective_message.reply_text('⚙️ /config v6 básico ativo. Ajustes avançados entram na próxima revisão.'); return
    f=get_fields(s)[s['index']]
    if f[2]=='os' and not text.isdigit(): await update.effective_message.reply_text('⚠️ Digite apenas números para a O.S.'); return
    if f[2]=='hora':
        import re
        if not re.match(r'^\d{2}:\d{2}$',text): await update.effective_message.reply_text('⚠️ Use HH:MM. Exemplo: 15:30'); return
    s['data'][f[0]]=text; s['index']+=1; await ask_current(update.effective_message,s)
