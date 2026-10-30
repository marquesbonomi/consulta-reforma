# Lê a estrutura da CNAE-Subclasses 2.3 (xlsx do IBGE) e grava [código, descrição] em cnae.json.
import json, sys, openpyxl
ws = openpyxl.load_workbook(sys.argv[1], read_only=True).worksheets[0]
rows = []
for i, r in enumerate(ws.iter_rows(values_only=True)):
    if i < 4: continue
    cod = next((str(c).strip() for c in r[:5] if c), None)
    desc = (r[5] or "").strip() if len(r) > 5 and r[5] else ""
    if cod and desc: rows.append([cod, desc])
json.dump(rows, open(sys.argv[2], "w"), ensure_ascii=False, separators=(",", ":"))
from collections import Counter
print(len(rows), Counter(len(c) for c, _ in rows))
