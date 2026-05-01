import json
from pathlib import Path

def ensure_file(path, default):
    p=Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists(): p.write_text(json.dumps(default,ensure_ascii=False,indent=2),encoding='utf-8')

def read_json(path, default):
    ensure_file(path, default)
    try: return json.loads(Path(path).read_text(encoding='utf-8'))
    except Exception: return default

def write_json(path, data):
    p=Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

def append_json(path, item):
    data=read_json(path, [])
    if not isinstance(data, list): data=[]
    data.append(item); write_json(path, data)
