# Junta a Tabela NCM vigente (xlsx) com as alíquotas de IPI da TIPI (tipi.json) em ncm.json.
import json, sys, openpyxl
wb = openpyxl.load_workbook(sys.argv[1], read_only=True)
ws = wb.worksheets[0]
cab = [r[0] for i, r in enumerate(ws.iter_rows(values_only=True)) if i < 3]
tipi = json.load(open(sys.argv[2]))
rows = []
for i, r in enumerate(ws.iter_rows(values_only=True)):
    if i < 5 or not r[0]: continue
    c = str(r[0]).strip(); d = str(r[1] or "").strip()
    rows.append([c, d, tipi["ipi"].get(c)])
json.dump({"vig": cab[1], "atual": cab[2], "rows": rows, "ex": tipi["ex"]}, open(sys.argv[3], "w"), ensure_ascii=False, separators=(",", ":"))
print(len(rows), "códigos NCM;", sum(1 for x in rows if len(x[0].replace(".", "")) == 8 and x[2] is None), "folhas sem IPI")
