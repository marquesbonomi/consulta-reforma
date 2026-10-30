import json, re
rows = json.load(open("rows.json"))
arts = json.load(open("reg_arts.json"))

ANEXOS = [  # (romano, idx inicio em rows, tratamento, reducao, art LC, art Reg, titulo curto)
 ("I",0,"zero",1.0,"125","199","Cesta Básica Nacional de Alimentos"),
 ("II",28,"red60",.6,"129","204","Serviços de educação"),
 ("III",38,"red60",.6,"130","205","Serviços de saúde"),
 ("IV",70,"red60",.6,"131","206","Dispositivos médicos"),
 ("V",182,"red60",.6,"132","207","Dispositivos de acessibilidade (PcD)"),
 ("VI",213,"red60",.6,"133, § 1º","208, § 1º","Nutrição enteral/parenteral e fórmulas para erros inatos do metabolismo"),
 ("VII",295,"red60",.6,"135","210","Alimentos destinados ao consumo humano"),
 ("VIII",313,"red60",.6,"136","211","Higiene pessoal e limpeza (baixa renda)"),
 ("IX",322,"red60",.6,"138","213","Insumos agropecuários e aquícolas"),
 ("X",361,"red60",.6,"139","215","Produções artísticas, culturais, de eventos, jornalísticas e audiovisuais"),
 ("XI",421,"red60",.6,"142","218","Soberania, segurança nacional, da informação e cibernética"),
 ("XII",469,"zero",1.0,"144","220","Dispositivos médicos (alíquota zero)"),
 ("XIII",492,"zero",1.0,"145","221","Dispositivos de acessibilidade PcD (alíquota zero)"),
 ("XV",501,"zero",1.0,"148","224","Produtos hortícolas, frutas e ovos"),
]
ENDS = [a[1] for a in ANEXOS[1:]] + [509]

NBS = r"(?<![\d.])1\.\d{4}(?:\.\d{1,2}){0,2}(?![\d])"
NCM = r"(?<![\d.])(?:\d{4}\.\d{4}|\d{4}(?:\.\d{1,2}){1,2}|\d{2}\.\d{2}(?:\.\d{2}){0,2})(?![\d])"
BARE = r"(?<![\d.])\d{4}(?![\d.])"

def codes(text, bare=False):
    out=[]
    for m in re.finditer(NBS, text): out.append(("nbs", m.group(0)))
    t = re.sub(NBS, " ", text)
    for m in re.finditer(NCM, t): out.append(("ncm", m.group(0)))
    if bare:
        t2 = re.sub(NCM, " ", t)
        for m in re.finditer(BARE, t2): out.append(("ncm", m.group(0)))
    for m in re.finditer(r"[Cc]apítulos? ((?:\d{1,2}(?:, | e )?)+)", text):
        for n in re.findall(r"\d{1,2}", m.group(1)): out.append(("ncm", n.zfill(2)))
    return out

def split_pos_exc(text, bare=False):
    pos, exc = [], []
    text = re.sub(r"\((exceto[^()\d]*)\)", lambda m: "("+m.group(1).replace("exceto","excl.")+")", text)
    for seg in text.split(";"):
        i = seg.find("exceto")
        if i < 0: pos += codes(seg, bare)
        else:
            pos += codes(seg[:i], bare); exc += codes(seg[i:], bare)
    return pos, exc

def norm(c): return re.sub(r"\D","",c)

itens=[]
for (rom,ini,trat,red,lc,reg,tit),fim in zip(ANEXOS,ENDS):
    cur=None; grupo=""
    for r in rows[ini+1:fim]:
        n=r[1].replace(" ",""); d=r[2] if len(r)>2 else ""; c=r[3] if len(r)>3 else ""
        if n=="":
            if cur: cur["d"]=(cur["d"]+" "+d).strip(); cur["cc"]=(cur["cc"]+" "+c).strip()
            continue
        if d.isupper() and not c:   # cabeçalho de grupo (ex.: "1 - ACESSÓRIOS...")
            grupo=d.capitalize(); cur=None; continue
        cur={"a":rom,"n":n,"d":d,"cc":c,"g":grupo}; itens.append(cur)
for it in itens:
    p1,e1 = split_pos_exc(it["d"])
    p2,e2 = split_pos_exc(it["cc"], bare=True)
    seen=set(); P=[]
    for k,v in p1+p2:
        if (k,norm(v)) not in seen: seen.add((k,norm(v))); P.append([k,v])
    X=[[k,v] for k,v in e1+e2]
    it["p"]=P; it["x"]=X
    it["pend"]= "pendente" in it["cc"]
    del it["cc"]

# Imposto Seletivo (Anexo XVII)
IS=[]
r=rows[559:]
for i in range(0,len(r)-1,2):
    lab=r[i][1]; txt=r[i+1][1]
    p,e=split_pos_exc(txt, bare=True)
    IS.append({"a":"XVII","n":str(i//2+1),"d":lab+": "+txt,"g":"Imposto Seletivo","p":[list(x) for x in p],"x":[list(x) for x in e],"pend":False})
itens+=IS
# saúde menstrual (art. 223 Reg / 147 LC) tem NCM no próprio artigo
itens.append({"a":"art223","n":"1","d":"Tampões higiênicos, absorventes higiênicos internos ou externos (descartáveis ou reutilizáveis), calcinhas absorventes e coletores menstruais, do código 9619.00.00 da NCM/SH, que atendam às normas da Anvisa","g":"","p":[["ncm","9619.00.00"]],"x":[],"pend":False})

def art(n, lim=2200):
    t=arts.get(n,"")
    m=re.search(r"\n ?Art\. \d+", t[10:]);  t=t[:m.start()+10] if m else t
    return t[:lim]+(" […]" if len(t)>lim else "")

FONTES={a[0]:{"trat":a[2],"red":a[3],"lc":a[4],"reg":a[5],"tit":a[6]} for a in ANEXOS}
FONTES["XVII"]={"trat":"is","red":0,"lc":"409","reg":"—","tit":"Bens sujeitos ao Imposto Seletivo"}
FONTES["art223"]={"trat":"zero","red":1.0,"lc":"147","reg":"223","tit":"Cuidados básicos à saúde menstrual"}
for k,f in FONTES.items():
    f["texto"]=art(f["reg"].split(",")[0]) if f["reg"]!="—" else ""

PROF=["administradores","advogados","arquitetos e urbanistas","assistentes sociais","bibliotecários","biólogos","contabilistas (contadores e técnicos em contabilidade)","economistas","economistas domésticos","profissionais de educação física","engenheiros e agrônomos","estatísticos","médicos veterinários e zootecnistas","museólogos","químicos","profissionais de relações públicas","técnicos industriais","técnicos agrícolas"]
A=[]
def add(t,trat,red,reg,lc,kw="",regs=None,obs="",vig="",texto=None,aba=""):
    A.append({"t":t,"trat":trat,"red":red,"reg":reg,"lc":lc,"kw":kw,"obs":obs,"vig":vig,"aba":aba,"texto":texto if texto is not None else "\n\n".join(art(r) for r in (regs or [reg]))})

def lc_art(n):
    t=open("lc.txt").read()
    t="\n".join(l for l in t.split("\n") if not re.fullmatch(r"\s*\d{1,3}\s*", l))
    i=t.index("Art. %s. "%n); j=t.index("Art. %d. "%(int(n)+1), i)
    body=re.split(r"\n\s*(?:CAPÍTULO|Seção|TÍTULO|LIVRO) [IVXL]+\s*\n", t[i:j])[0]
    body=re.sub(r"[ \t]+"," ",body)
    body=re.sub(r"(?<![.;:])\n(?![ ]?(§|[IVXL]+ -|[a-z]\)|Parágrafo))"," ",body)
    return re.sub(r"\n ","\n",body).strip()
LC381=lc_art("381"); LC383=lc_art("383")
for p in PROF:
    add("Serviços de "+p,"red30",.3,"202","127","profissão regulamentada conselho profissional serviço intelectual "+p,
        obs="Pessoa física: serviço ligado à habilitação. Pessoa jurídica: sócios habilitados no conselho, sem sócio PJ, sem participar de outra PJ e só a atividade da habilitação (art. 202, § 1º).")
add("Medicamentos registrados na Anvisa ou de farmácia de manipulação","red60",.6,"208","133","remédio farmácia drogaria medicamento",obs="Indústria/importador precisa ter compromisso com União e CGIBS ou seguir a CMED (§ 2º). Os de alíquota zero estão no art. 222.")
add("Medicamentos de alíquota zero (doenças raras, oncologia, diabetes, HIV/IST, cardiovasculares, Farmácia Popular)","zero",1.0,"222","146","remédio farmácia medicamento câncer oncologia diabetes",obs="A lista nominal é fixada por ato conjunto (art. 222, § 3º).")
add("Produtos agropecuários, aquícolas, pesqueiros, florestais e extrativistas in natura","red60",.6,"212","137","rural agro produtor in natura grão pesca peixe madeira",obs="In natura = sem industrialização e sem embalagem de apresentação (§ 1º).")
add("Comunicação institucional para a administração pública","red60",.6,"216","140","publicidade agência marketing redes sociais assessoria de imprensa governo")
add("Atividades desportivas (educação desportiva, clubes, sócio-torcedor)","red60",.6,"217","141","esporte clube academia futebol ingresso")
add("Bens e serviços de soberania e segurança nacional/cibernética","red60",.6,"218","142","segurança da informação cibernética militar defesa",obs="Ver também os itens do Anexo XI.")
add("Automóveis para PcD, TEA ou taxistas","zero",1.0,"225","149","carro veículo taxi táxi deficiência autismo",obs="Fabricação nacional, 4 portas no mínimo; demais requisitos nos arts. 225 a 231.")
add("Serviços de pesquisa e desenvolvimento de ICT sem fins lucrativos","zero",1.0,"232","156","pesquisa ciência tecnologia inovação fundação de apoio")
add("Transporte público coletivo urbano, semiurbano e metropolitano (rodoviário e metroviário)","isento",1.0,"233","157","ônibus metrô transporte urbano")
add("Reabilitação urbana de zonas históricas e áreas críticas","red60",.6,"234","158","obra imóvel centro histórico urbanismo",obs="Projeto precisa ser aprovado pela comissão tripartite (art. 235).")
add("Bens imóveis: venda, construção e demais operações","red50",.5,"379","261","imobiliária incorporação loteamento construtora venda de imóvel",regs=["379","359"],obs="Há ainda redutores de ajuste e social na base de cálculo (arts. 364 a 378).")
add("Bens imóveis: locação, cessão onerosa e arrendamento","red70",.7,"379","261","aluguel locação imóvel administradora de imóveis",obs="Parágrafo único do art. 379.")
add("Bares, restaurantes, lanchonetes, padarias, cafeterias, sorveterias","red40",.4,"400","275","restaurante bar alimentação lanchonete padaria",regs=["396","400"],obs="Regime específico; não vale para bebidas não alcoólicas industrializadas.")
add("Hotelaria, parques de diversão e parques temáticos","red40",.4,"405","281","hotel pousada parque turismo hospedagem",regs=["402","405"])
add("Transporte coletivo intermunicipal/interestadual (rodoviário, ferroviário, hidroviário) e aéreo regional","red40",.4,"416","285 a 287","ônibus viagem passagem transporte aéreo regional carga aérea",regs=["416"],obs="Transporte público ferroviário e hidroviário urbano/metropolitano: redução de 100% (art. 416, II).")
add("Agências de turismo","regesp",None,"417","288","turismo viagem agência passagem",regs=["417","418"],obs="Regime específico: a base de cálculo exclui os valores repassados aos fornecedores intermediados.")
add("Sociedades cooperativas (operações com associados)","zero",1.0,"391","271","cooperativa cooperado associado",regs=["391","392"],obs="Regime opcional; alíquota zero só nas operações do art. 391.")
add("Serviços financeiros (crédito, câmbio, seguros, arranjos de pagamento, consórcio, fundos etc.)","regesp",None,"269","181 e 182","banco financeira seguro seguradora consórcio factoring fintech pagamento",obs="Regime específico com base de cálculo própria e alíquotas próprias.")
add("Planos de assistência à saúde","regesp",None,"330","234","plano de saúde operadora seguradora")
add("Concursos de prognósticos, apostas e fantasy sport","regesp",None,"347","244","loteria aposta bet")
add("Combustíveis (incidência monofásica)","regesp",None,"259","172","gasolina diesel etanol combustível posto",obs="Alíquota específica por unidade de medida (art. 262).")
add("Sociedade Anônima do Futebol (SAF)","regesp",None,"421","292 e 293","futebol clube SAF",regs=["421","422"],obs="Recolhimento unificado (TEF).")
add("Compra de produtor rural não contribuinte","credpres",None,"239","164 a 168","rural agro produtor crédito presumido",regs=["239","245"],obs="Produtor com receita abaixo de R$ 3,6 milhões não é contribuinte; o comprador pode ter crédito presumido (art. 245).",vig="O crédito presumido só vale a partir de 1º/01/2027 (art. 617, II, do regulamento, na redação da Resolução CGIBS nº 13/2026).")
add("Frete de transportador autônomo pessoa física ou MEI","credpres",None,"250","169","frete caminhoneiro transporte de carga crédito presumido",vig="O crédito presumido só vale a partir de 1º/01/2027 (art. 617, II, do regulamento, na redação da Resolução CGIBS nº 13/2026).")
add("Compra de resíduos para reciclagem de pessoa física ou cooperativa","credpres",None,"256","170","reciclagem sucata resíduo catador crédito presumido",vig="O crédito presumido só vale a partir de 1º/01/2027 (art. 617, II, do regulamento, na redação da Resolução CGIBS nº 13/2026).")
add("Compra de bens móveis usados de pessoa física para revenda","credpres",None,"258","171","usado seminovo revenda brechó veículo usado crédito presumido",vig="O crédito presumido só vale a partir de 1º/01/2027 (art. 617, II, do regulamento, na redação da Resolução CGIBS nº 13/2026).")
add("Crédito presumido de CBS sobre o estoque em 1º/01/2027 (9,25%)","credpres",None,"—","381","estoque inventário lucro presumido cumulativo monofásico substituição tributária pis cofins transição 9,25 crédito presumido",
    obs="Para empresas no regime regular da CBS, sobre o estoque de 1º/01/2027 que não gerou crédito de PIS/Cofins (lucro presumido/cumulativo, monofásicos e ST, ou vedação parcial). Apurar até 30/06/2027 e usar em 12 parcelas só contra a CBS. Veja a aba \"Crédito do estoque\".",
    texto=LC381+"\n\n"+LC383, aba="estoque")
add("Exportação de bens e serviços","imune",1.0,"90","79","exportação exterior",regs=["90"])
add("Imunidades (entes públicos, templos, partidos, entidades de educação e assistência sem fins lucrativos, livros, jornais etc.)","imune",1.0,"10","9º","imunidade igreja templo livro jornal partido sindicato ONG",regs=["10"])
add("Zona Franca de Manaus e Áreas de Livre Comércio","regesp",None,"432","439 e seguintes","manaus suframa zona franca área de livre comércio",regs=["432","434","516"],obs="Benefícios detalhados nos arts. 514 a 531.",vig="Parte dos benefícios tem início adiado: arts. 515, 525 e 526 a partir de 1º/01/2027; arts. 517, 518, 520 a 522, 528 e 529 a partir de 1º/01/2029 (art. 617 do regulamento, na redação da Resolução CGIBS nº 13/2026).")

NORMAS=[
 ["LC 214/2025 (texto atualizado, com a LC 227/2026)","Institui IBS, CBS e Imposto Seletivo; anexos com NCM/NBS","base"],
 ["Resolução CGIBS nº 6, de 30/04/2026","Regulamento do IBS","base"],
 ["Resolução CGIBS nº 13, de 22/07/2026","Altera o art. 617 do regulamento: datas de início de créditos presumidos e de parte da Zona Franca","aplicada"],
 ["Resolução CGIBS nº 14, de 29/07/2026","Percentual da arrecadação do IBS que financia o Comitê Gestor em 2027","sem efeito"],
 ["Resoluções CGIBS nº 1, 2, 3, 4, 5, 8, 9, 11, 16, 17 e 18 de 2026","Funcionamento interno do Comitê Gestor: comissões, eleição, regimento, estrutura, processo eletrônico, licitações, competências e pessoal","sem efeito"],
 ["Resoluções CGIBS nº 7, 10, 12 e 15 de 2026","Orçamento do Comitê Gestor para 2026 e 2027","sem efeito"],
]
json.dump({"fontes":FONTES,"itens":itens,"ativ":A,"normas":NORMAS,"lc381":LC381,"lc383":LC383}, open("data.json","w"), ensure_ascii=False, separators=(",",":"))
from collections import Counter
print(len(itens), Counter(i["a"] for i in itens)); print(len(A))
print([ (i["n"],i["p"],i["x"]) for i in itens if i["a"]=="I"][18:20])
print(sum(1 for i in itens if not i["p"] and not i["pend"]), [ (i["a"],i["n"],i["d"][:60]) for i in itens if not i["p"]][:15])
