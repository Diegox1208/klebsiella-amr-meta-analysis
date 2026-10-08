# -*- coding: utf-8 -*-
"""Build Tables 1 and 2 as Word files from results/ and data/."""
import csv, os, zipfile, re
from xml.sax.saxutils import escape

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(PROJ, "results")

def run(text, bold=False, italic=False, size=18, sup=False):
    rpr = "<w:rPr><w:rFonts w:ascii=\"Arial\" w:hAnsi=\"Arial\" w:cs=\"Arial\"/>" + ("<w:b/>" if bold else "") + ("<w:i/>" if italic else "")
    rpr += "<w:sz w:val=\"%d\"/><w:szCs w:val=\"%d\"/>%s</w:rPr>" % (size, size, "<w:vertAlign w:val=\"superscript\"/>" if sup else "")
    return "<w:r>%s<w:t xml:space=\"preserve\">%s</w:t></w:r>" % (rpr, escape(text))
def rich(text, size=18, bold=False):
    out = []
    for j, part in enumerate(re.split(r"\^(.+?)\^", text)):
        if j % 2 == 1: out.append(run(part, bold=bold, size=size, sup=True)); continue
        out += [run(p, bold=bold, italic=(i % 2 == 1), size=size) for i, p in enumerate(re.split(r"\*(.+?)\*", part)) if p]
    return "".join(out)
def para(text, size=18, bold=False, after=80):
    return "<w:p><w:pPr><w:spacing w:after=\"%d\" w:line=\"240\" w:lineRule=\"auto\"/></w:pPr>%s</w:p>" % (after, rich(text, size, bold))
def cell(text, width, shade=None, bold=False, size=17, align=None):
    tcpr = "<w:tcPr><w:tcW w:w=\"%d\" w:type=\"dxa\"/>" % width + ("<w:shd w:val=\"clear\" w:color=\"auto\" w:fill=\"%s\"/>" % shade if shade else "") + "<w:vAlign w:val=\"center\"/></w:tcPr>"
    jc = "<w:jc w:val=\"%s\"/>" % align if align else ""
    return "<w:tc>%s<w:p><w:pPr><w:spacing w:before=\"30\" w:after=\"30\"/>%s</w:pPr>%s</w:p></w:tc>" % (tcpr, jc, rich(text, size, bold))
def table(widths, header, rows, aligns=None):
    total = sum(widths); aligns = aligns or [None] * len(widths)
    borders = "".join("<w:%s w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"000000\"/>" % b for b in ("top", "bottom", "insideH"))
    x = ["<w:tbl><w:tblPr><w:tblW w:w=\"%d\" w:type=\"dxa\"/><w:tblBorders>%s</w:tblBorders><w:tblLayout w:type=\"fixed\"/></w:tblPr>" % (total, borders),
         "<w:tblGrid>%s</w:tblGrid>" % "".join("<w:gridCol w:w=\"%d\"/>" % w for w in widths),
         "<w:tr><w:trPr><w:tblHeader/></w:trPr>%s</w:tr>" % "".join(cell(h, w, bold=True, align=a) for h, w, a in zip(header, widths, aligns))]
    for r in rows:
        bold = r[0].startswith("Total") or r[0].startswith("Overall")
        x.append("<w:tr>%s</w:tr>" % "".join(cell(v, w, bold=bold, align=a) for v, w, a in zip(r, widths, aligns)))
    x.append("</w:tbl>"); return "".join(x)
def docx(path, body):
    sect = "<w:sectPr><w:pgSz w:w=\"11906\" w:h=\"16838\"/><w:pgMar w:top=\"1134\" w:right=\"1134\" w:bottom=\"1134\" w:left=\"1134\" w:header=\"708\" w:footer=\"708\" w:gutter=\"0\"/></w:sectPr>"
    doc = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><w:document xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\"><w:body>%s%s</w:body></w:document>" % (body, sect)
    ct = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\"><Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/><Default Extension=\"xml\" ContentType=\"application/xml\"/><Override PartName=\"/word/document.xml\" ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml\"/></Types>"
    rels = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\"><Relationship Id=\"rId1\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" Target=\"word/document.xml\"/></Relationships>"
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct); z.writestr("_rels/.rels", rels); z.writestr("word/document.xml", doc)

res = {r["id"]: r for r in csv.DictReader(open(os.path.join(PROJ, "results/tabla1_2_v3.csv"), encoding="utf-8"))}
base = {r["id"]: r for r in csv.DictReader(open(os.path.join(PROJ, "data/main_dataset_v3.csv"), encoding="utf-8-sig"))}
META = [
 ("16", "2005", "Morales et al.",            "2000",                     "Metropolitan Lima",       "Clinical samples, unspecified", "Cefotaxime",       "Non-susceptible", "Before 2010", False, True),
 ("2",  "2012", "García et al.",        "2008–2009",           "Metropolitan Lima",       "Blood",                        "ESBL phenotype",   "ESBL-positive",   "Before 2010", False, True),
 ("1",  "2013", "Luján-Roca et al.",    "2003",                     "Metropolitan Lima",       "Urine",                        "Cefotaxime",       "Resistant",       "Before 2010", False, True),
 ("3",  "2016", "García et al.",        "2008–2011",           "Metropolitan Lima and Callao", "Blood, neonatal",        "ESBL phenotype",   "ESBL-positive",   "2010 or later", False, False),
 ("18", "2016", "Fernández-Mogollón et al.", "2014",           "Chiclayo",                "Urine, blood, respiratory and wound", "Ceftriaxone", "Non-susceptible", "Not stated", True, True),
 ("19", "2017", "Méndez Chacón et al.", "2002–2011",      "Metropolitan Lima",       "Urine",                        "ESBL phenotype",   "ESBL-positive",   "Not stated",  False, True),
 ("15", "2018", "Falconí-Sarmiento et al.", "2016",                   "Metropolitan Lima",       "Blood",                        "ESBL phenotype",   "ESBL-positive",   "Not stated",  False, True),
 ("5",  "2019", "Miranda et al.",            "2014–2016",           "Metropolitan Lima",       "Urine",                        "Ceftriaxone, cefotaxime and ceftazidime", "Non-susceptible", "2010 or later", True, True),
 ("14", "2019", "Gonzales et al.",           "2012–2013",           "Metropolitan Lima",       "Urine, blood, respiratory and other", "ESBL phenotype", "ESBL-positive", "Not stated", False, True),
 ("12", "2020", "Quispe et al.",             "2017–2018",           "Metropolitan Lima",       "Blood, neonatal",              "Cefotaxime",       "Non-susceptible", "2010 or later", False, True),
 ("4",  "2021", "Flores-Paredes et al.",     "2009–2010, 2012–2014", "Metropolitan Lima",  "Clinical samples, unspecified", "Ceftriaxone",     "Non-susceptible", "2010 or later", True, True),
 ("11", "2021", "Pérez-Lazo et al.",    "2015–2018",           "Metropolitan Lima",       "Not stated",                   "Ceftazidime",      "Unclear‡",   "2010 or later", True, True),
 ("13", "2022", "Chilón-Chávez et al.", "2019–2020",      "Lambayeque",              "Respiratory, urine and blood", "Ceftriaxone",      "Non-susceptible", "2010 or later", False, True),
 ("9",  "2023", "Rondon et al.",             "2019",                     "National, 9 regions",     "Blood and urine",              "Class, drug not named", "Resistant",  "Not stated",  False, True),
 ("6",  "2023", "Krapp et al.",              "2017–2019",           "National, 12 regions",    "Blood",                        "Ceftriaxone",      "Resistant",       "2010 or later", False, True),
 ("17", "2024", "Sosa-Flores et al.",        "2020–2021",           "Chiclayo",                "Blood, neonatal",              "Cefotaxime",       "Resistant",       "2010 or later", True, True),
]
REF = {"2": 14, "1": 24, "3": 15, "15": 28, "5": 25, "14": 26, "12": 27, "4": 7, "11": 9, "13": 31, "9": 10, "6": 8, "16": 29, "19": 30, "18": 32, "17": 33}
rondon_n = int(base["9"]["n_tested"]) + int(base["10"]["n_tested"]); rondon_r = int(base["9"]["n_resistant"]) + int(base["10"]["n_resistant"])

TIER = lambda agent: "3" if agent.startswith("ESBL") else ("2" if agent.startswith("Class") else "1")
rows1 = []; tot_n = tot_r = 0
for id_, py, au, col, reg, samp, agent, cat, bp, deriv, prim in META:
    if id_ == "9": n, r = rondon_n, rondon_r
    else: n, r = int(base[id_]["n_tested"]), int(base[id_]["n_resistant"])
    mark = "" if prim else "\u00a7"
    rows1.append([f"{py} {au}^{REF[id_]}^{mark}", col, reg, samp, f"{n:,}", f"{r:,}" + ("†" if deriv else ""), agent, cat, TIER(agent), bp])
    if prim: tot_n += n; tot_r += r
n_prim = sum(1 for m in META if m[10]); n_rep = len(META)
rows1.append([f"Total, {n_prim} studies", "", "", "", f"{tot_n:,}", f"{tot_r:,}", "", "", "", ""])
NUM = {9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen"}
res_sum = {r["analisis"]: r for r in csv.DictReader(open(os.path.join(PROJ, "results/resumen_resultados_v3.csv"), encoding="utf-8"))}
sens = {r["Escenario"]: r for r in csv.DictReader(open(os.path.join(PROJ, "results/sensibilidad_extraccion_v3.csv"), encoding="utf-8"))}
G = res_sum["3GC principal"]; f2 = lambda v: f"{float(v):.2f}"
S_noproxy = next(v for k, v in sens.items() if "Sin proxy" in k); S_both = next(v for k, v in sens.items() if "Ambos informes" in k)
S_2016 = next(v for k, v in sens.items() if "2016 en lugar" in k); S_ctx = next(v for k, v in sens.items() if "Solo cefotaxima" in k)

body1 = para(f"Table 1. Characteristics of the {NUM[n_rep]} reports from the {NUM[n_prim]} included studies.", size=20, bold=True, after=120)
body1 += table([1700, 1050, 1100, 1250, 620, 700, 1150, 1000, 400, 668],
               ["Publication year \u2013 Author", "Collection years", "Region", "Specimen", "Isolates tested, N", "3GC resistant, N", "Cephalosporin", "Category reported", "Tier", "Breakpoints"],
               rows1, aligns=[None, None, None, None, "right", "right", None, None, "center", None])
body1 += para("", after=40)
body1 += para("3GC, third-generation cephalosporins. ESBL, extended-spectrum beta-lactamase. Non-susceptible, resistant plus intermediate. Counts refer to the isolates tested for the cephalosporin listed and follow the category reported by each study. Where only the ESBL phenotype was reported, ESBL-positive isolates were counted as resistant. Tier 1, resistance to a named cephalosporin. Tier 2, resistance to the class without naming the drug. Tier 3, ESBL phenotype used as a surrogate. Breakpoints, whether the interpretive criteria used were published before or after the 2010 CLSI revision. † Count calculated from the reported percentage. ‡ The article reports resistance in its table and non-susceptibility in its methods. § Secondary report of the García et al. 2012 study, not included in the total. Rondon et al. reported 8 of 11 blood isolates and 31 of 63 urine isolates, combined here.", size=15, after=0)
docx(os.path.join(OUT, "Table1_v3.docx"), body1)

rows2 = []
for id_, py, au, col, reg, samp, agent, cat, bp, deriv, prim in META:
    if not prim: continue
    r = res[id_]
    rows2.append([f"{py} {au}^{REF[id_]}^", f"{int(r['cases']):,}", f"{int(r['total']):,}", f"{float(r['prop']):.2f}", f"{float(r['ci_low']):.2f} to {float(r['ci_high']):.2f}", f"{float(r['weight']):.1f}%"])
rows2.append(["Overall, random effects", f"{tot_r:,}", f"{tot_n:,}", f2(G["prev"]), f"{f2(G['ic_inf'])} to {f2(G['ic_sup'])}", "100.0%"])
body2 = para("Table 2. Pooled prevalence of 3GC resistance in *K. pneumoniae* isolates in Peru (random-effects model).", size=20, bold=True, after=120)
body2 += table([2600, 1100, 1100, 1300, 1900, 1638], ["Publication year \u2013 Author", "Cases", "Total", "Proportion", "95% CI", "Weight"], rows2,
               aligns=[None, "right", "right", "right", None, "right"])
body2 += para("", after=40)
body2 += para(f"Random-effects model on logit-transformed proportions. Heterogeneity I² = {100*float(G['I2']):.1f}%, τ² = {float(G['tau2']):.4f}, p < 0.0001, with a 95% prediction interval of {f2(G['pi_inf'])} to {f2(G['pi_sup'])}. In sensitivity analyses of data-extraction choices the pooled proportion was {f2(S_both['Prevalencia'])}, 95% CI {f2(S_both['IC_inf'])} to {f2(S_both['IC_sup'])}, with both García reports, k = {S_both['k']}. It was {f2(S_2016['Prevalencia'])}, 95% CI {f2(S_2016['IC_inf'])} to {f2(S_2016['IC_sup'])}, with the 2016 report instead of the 2012 report, k = {S_2016['k']}. It was {f2(S_noproxy['Prevalencia'])}, 95% CI {f2(S_noproxy['IC_inf'])} to {f2(S_noproxy['IC_sup'])}, without the three studies that reported only the ESBL phenotype, k = {S_noproxy['k']}, and {f2(S_ctx['Prevalencia'])}, 95% CI {f2(S_ctx['IC_inf'])} to {f2(S_ctx['IC_sup'])}, in the studies reporting cefotaxime, k = {S_ctx['k']}. CI, confidence interval. k, number of studies.", size=15, after=0)
docx(os.path.join(OUT, "Table2_v3.docx"), body2)

for n in ("Table1_v3.docx", "Table2_v3.docx"):
    import xml.dom.minidom
    with zipfile.ZipFile(os.path.join(OUT, n)) as z: xml.dom.minidom.parseString(z.read("word/document.xml"))
    print(n, "OK")
print("Tabla 1: total", tot_n, "casos", tot_r)
