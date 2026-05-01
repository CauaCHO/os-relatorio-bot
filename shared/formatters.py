import re
from datetime import datetime
from zoneinfo import ZoneInfo

def br_now_hm():
    try: return datetime.now(ZoneInfo('America/Sao_Paulo')).strftime('%H:%M')
    except Exception: return datetime.now().strftime('%H:%M')

def calcular_tempo(inicio,fim):
    try:
        h1=datetime.strptime(inicio,'%H:%M'); h2=datetime.strptime(fim,'%H:%M')
        mins=int((h2-h1).total_seconds()//60)
        if mins<0: mins+=1440
        return f'{mins//60} h {mins%60} min'
    except Exception: return '-'

def esc(x):
    if x is None: return '-'
    return str(x).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').strip() or '-'

def materiais(t):
    t=str(t or '-').strip()
    if t=='-': return '-'
    clean=re.sub(r'\s+',' ',t)
    ms=list(re.finditer(r'(\d+)\s*[xX]?\s+([^0-9]+?)(?=(\s+\d+\s*[xX]?\s+)|$)', clean))
    if not ms: return t
    return '\n'.join([f"{m.group(1)}x {m.group(2).strip()}" for m in ms if m.group(2).strip()]) or t

def sinal(t):
    t=str(t or '-').lower().replace('dbm','').strip()
    if t in ['','-']: return '-'
    try:
        float(t.replace(',','.').replace('-',''))
        if not t.startswith('-'): t='-'+t
        return t.replace(',','.')+' dBm'
    except Exception: return t

def speed(t):
    t=str(t or '-').lower().replace('mbps','').strip()
    return '-' if t in ['','-'] else f'{t} Mbps'

def fmt(tipo,val):
    return materiais(val) if tipo=='materiais' else sinal(val) if tipo=='sinal' else speed(val) if tipo=='speed' else esc(val)
