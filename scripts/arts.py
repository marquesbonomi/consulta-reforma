import re, json, sys
src=open(sys.argv[1]).read()
lines=[l for l in src.split("\n") if not re.fullmatch(r"\s*\d{1,3}\s*", l)]
# skip sumário: start at second occurrence of the doc title
txt="\n".join(lines)
start=txt.find("LIVRO I - DAS NORMAS COMUNS", txt.find("LIVRO II - DAS NORMAS ESPECÍFICAS")+10)
txt=txt[start:]
txt=re.sub(r"[ \t]+"," ",txt)
parts=re.split(r"\n ?(?=Art\. \d+(?:-[A-Z])?\. )", txt)
arts={}
for p in parts:
    m=re.match(r"Art\. (\d+(?:-[A-Z])?)\. ", p)
    if m and m.group(1) not in arts:
        body=re.split(r"\n ?(?:CAPÍTULO|Seção|Subseção|TÍTULO|LIVRO) [IVXL]+ -", p)[0]
        body=re.sub(r"(?<![.;:])\n(?![ ]?(§|[IVXL]+ -|[a-z]\)|Parágrafo))"," ",body)
        arts[m.group(1)]=re.sub(r" +"," ",body).strip()
json.dump(arts, open(sys.argv[2],"w"), ensure_ascii=False, indent=0)
print(len(arts), min(map(lambda k:int(k.split('-')[0]),arts)), max(map(lambda k:int(k.split('-')[0]),arts)))
