# Lê a TIPI (texto extraído com pdftotext -layout) e devolve alíquota de IPI por código e os "Ex".
import re, json, sys
lines=open(sys.argv[1]).read().split("\n")
CODE=re.compile(r"^\s{0,8}(\d{4}\.\d{2}\.\d{2}|\d{4}\.\d{2}(?:\.\d)?|\d{4}\.\d|\d{2}\.\d{2})(?:\s{2,}(.*))?$")
EX=re.compile(r"^\s{0,30}Ex\s*(\d{2,3})\s*-\s*(.*)$")
RATE=re.compile(r"\s{2,}(NT|\d{1,3}(?:,\d{1,2})?)\s*$")
out={}; ex={}; cur=None; pend=None
for l in lines:
    m=CODE.match(l)
    e=EX.match(l) if not m else None
    if m:
        cur=m.group(1); r=RATE.search(m.group(2) or "")
        if r: out[cur]=r.group(1); pend=None
        else: pend=("c",cur)
        continue
    if e and cur:
        r=RATE.search(e.group(2)); key=(cur,e.group(1)); ex.setdefault(cur,[]).append([e.group(1),RATE.sub("",e.group(2)).strip(),r.group(1) if r else None])
        pend=None if r else ("e",cur)
        continue
    if pend:
        r=RATE.search(l)
        if r and len(l.strip())<len(l):
            if pend[0]=="c": out[pend[1]]=r.group(1)
            else: ex[pend[1]][-1][2]=r.group(1)
            # continuação da descrição do Ex
        if pend and pend[0]=="e" and ex[pend[1]][-1][2] is None:
            ex[pend[1]][-1][1]+= " "+RATE.sub("",l).strip()
        if r: pend=None
json.dump({"ipi":out,"ex":ex},open(sys.argv[2],"w"),ensure_ascii=False)
print(len(out), sum(len(v) for v in ex.values()), sum(1 for v in ex.values() for x in v if x[2] is None))
