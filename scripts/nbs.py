# Lê a NBS 2.0 (texto extraído com pdftotext -layout) e grava [código, descrição] em nbs.json.
import re, json, sys
lines = open(sys.argv[1]).read().split("\n")
COD = re.compile(r"^\s{0,8}(1\.\d{4}(?:\.\d{1,2}){0,2})\s{2,}(\S.*)$")
CAP = re.compile(r"^\s*Capítulo (\d{1,2}) - (.+)$")
rows, cur, caps = [], None, {}
inicio = next(i for i, l in enumerate(lines) if "NBS 2.0" in l and "DESCRIÇÃO" in l)
cap = None
for l in lines[:inicio]:          # nomes dos capítulos no sumário (podem quebrar linha)
    m = CAP.match(l)
    if m: cap = m.group(1); caps[cap] = m.group(2).strip(); continue
    if cap and l.strip() and not l.lstrip().startswith(("SEÇÃO", "(Fl.", "Capítulo", "FORMAÇÃO", "REGRAS")): caps[cap] += " " + l.strip()
    elif not l.strip() or l.lstrip().startswith(("SEÇÃO", "(Fl.")): cap = None
for l in lines[inicio:]:
    m = COD.match(l)
    if m:
        cur = [m.group(1), re.sub(r"\s+", " ", m.group(2)).strip()]; rows.append(cur); continue
    t = l.strip()
    if cur and t and re.match(r"^\s{12,}\S", l) and not t.startswith(("(Fl.", "NBS 2.0", "Notas", "SEÇÃO", "Capítulo")):
        cur[1] += " " + re.sub(r"\s+", " ", t)
    elif not t or t.startswith(("(Fl.", "Notas", "Capítulo", "SEÇÃO")):
        cur = None
out = [["1." + k.zfill(2), v] for k, v in sorted(caps.items(), key=lambda x: int(x[0]))] + rows
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, separators=(",", ":"))
from collections import Counter
print(len(out), Counter(len(re.sub(r"\D", "", r[0])) for r in out))
