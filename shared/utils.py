import re
from datetime import datetime
from zoneinfo import ZoneInfo


def escape_html(value):
    if value is None:
        return "-"
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").strip() or "-"


def now_hm():
    try:
        return datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%H:%M")
    except Exception:
        return datetime.now().strftime("%H:%M")


def calc_time(start, end):
    try:
        a = datetime.strptime(start, "%H:%M")
        b = datetime.strptime(end, "%H:%M")
        mins = int((b - a).total_seconds() // 60)
        if mins < 0:
            mins += 24 * 60
        return f"{mins // 60} h {mins % 60} min"
    except Exception:
        return "-"


def valid_hour(text):
    return bool(re.match(r"^([01]\d|2[0-3]):[0-5]\d$", str(text).strip()))


def normalize_signal(text):
    t = str(text or "").strip().lower().replace("dbm", "").strip()
    if not t or t == "-":
        return "-"
    try:
        float(t.replace(",", ".").replace("-", ""))
        if not t.startswith("-"):
            t = "-" + t
        return t.replace(",", ".") + " dBm"
    except Exception:
        return text


def normalize_speed(text):
    t = str(text or "").strip().lower().replace("mbps", "").strip()
    if not t or t == "-":
        return "-"
    return f"{t} Mbps"


def format_materials_free(text):
    text = str(text or "").strip()
    if not text:
        return "-"
    clean = re.sub(r"\s+", " ", text)
    matches = list(re.finditer(r"(\d+)\s*[xX]?\s+([^0-9]+?)(?=(\s+\d+\s*[xX]?\s+)|$)", clean))
    if not matches:
        return text
    out = []
    for m in matches:
        qty = m.group(1).strip()
        desc = m.group(2).strip()
        if desc:
            out.append(f"{qty}x {desc}")
    return "\n".join(out) if out else text
