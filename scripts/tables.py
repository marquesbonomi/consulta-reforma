import pdfplumber, sys, json
pdf = pdfplumber.open(sys.argv[1])
out=[]
for pn in range(260, 284):
    p = pdf.pages[pn-1]
    for t in p.extract_tables():
        for r in t:
            out.append([pn]+[(c or "").replace("\n"," ").strip() for c in r])
json.dump(out, open("rows.json","w"), ensure_ascii=False)
print(len(out))
