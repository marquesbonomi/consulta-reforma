import pdfplumber, sys, re
pdf = pdfplumber.open(sys.argv[1])
for i, p in enumerate(pdf.pages):
    t = p.extract_text() or ""
    for m in re.finditer(r"^\s*ANEXO ([IVX]+)\s*$", t, re.M):
        print(i+1, m.group(1))
