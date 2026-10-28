# Versione inglese: crea pagine-en/001.webp ... e dati-en.js dal PDF tradotto.
# I numeri dell'indice inglese sono copiati da quello italiano e non corrispondono alle pagine del PDF inglese:
# l'inizio di ogni capitolo si trova cercando le pagine con il titolo in grande, e i numeri stampati nell'indice
# vengono tolti dalle immagini.
# Uso: python crea_pagine_en.py
import os, re, json, sys
import pymupdf
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
PDF = r"C:\Users\Filippo\Desktop\Book 15 Years Lute.pdf"
QUI = os.path.dirname(os.path.abspath(__file__))
LARGHEZZA = 1100
PAGINE_INDICE = range(6, 11)
PRIMA_PAGINA_TESTO = 12

d = pymupdf.open(PDF)
from titolo_inglese import pagine_iniziali_en
rifatte = pagine_iniziali_en()   # pagg. 1, 2, 4 rifatte dalle italiane (vedi titolo_inglese.py)

# pagine d'inizio dei capitoli: quelle con il titolo in caratteri grandi
inizi = []
for i in range(PRIMA_PAGINA_TESTO - 1, d.page_count):
    for b in d[i].get_text("dict")["blocks"]:
        if any(s["size"] >= 14 and len(s["text"].strip()) > 1 for l in b.get("lines", []) for s in l["spans"]):
            inizi.append(i + 1)
            break

# voci dell'indice, nell'ordine in cui sono stampate
def righe(p):
    out = []
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            t = "".join(s["text"] for s in l["spans"]).strip()
            if t:
                out.append((l["bbox"], t))
    return sorted(out, key=lambda r: r[0][1])

voci = []
for n in PAGINE_INDICE:
    sinistra = [r for r in righe(d[n - 1]) if r[0][0] < 300 and r[1] != "CONTENTS"]
    for bb, t in sinistra:
        if t.startswith("by "):
            voci[-1]["autore"] = t[3:].rstrip(", ")
            voci[-1]["y1"] = max(voci[-1]["y1"], bb[3])
        elif voci and voci[-1]["n"] == n and not voci[-1]["autore"] and bb[1] - voci[-1]["y_ult"] < 18:
            voci[-1]["titolo"] += " " + t
            voci[-1]["y1"] = bb[3]; voci[-1]["y_ult"] = bb[1]
        else:
            voci.append({"n": n, "titolo": t, "autore": "", "x0": bb[0], "y0": bb[1], "y1": bb[3], "y_ult": bb[1]})

assert len(voci) == len(inizi), (len(voci), len(inizi), inizi)
indice, zone = [], {}
for v, pdf in zip(voci, inizi):
    v["titolo"] = re.sub(r"^Foreword ", "Foreword – ", v["titolo"])
    v["titolo"] = v["titolo"].replace("Milazzo Milazzo as", "Milazzo – Milazzo as")  # titolo e sottotitolo
    indice.append({"titolo": v["titolo"], "autore": v["autore"], "pdf": pdf})
    W, H = d[v["n"] - 1].rect.width, d[v["n"] - 1].rect.height
    x0, y0, x1, y1 = v["x0"] - 4, v["y0"] - 3, 373, v["y1"] + 1
    zone.setdefault(v["n"], []).append({"x": round(x0 / W * 100, 2), "y": round(y0 / H * 100, 2),
                                        "w": round((x1 - x0) / W * 100, 2), "h": round((y1 - y0) / H * 100, 2), "pdf": pdf})
for v in indice:
    print(v["pdf"], v["titolo"], "–", v["autore"])


# numeri di pagina nell'indice stampato: quelli del PDF erano copiati dall'edizione italiana e sbagliati.
# Su richiesta dell'utente (2026-10-28) si tolgono del tutto, insieme a "P." e ai segni »: nell'app si va al
# capitolo toccando il titolo o il nome dell'autore.
NUMERI_FONT = r"C:\Windows\Fonts\times.ttf"   # simile al Minion del libro
colonna_numeri = []
for n in PAGINE_INDICE:
    for b in d[n - 1].get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if s["bbox"][0] > 320 and s["text"].strip():
                    colonna_numeri.append((n, s))
assert sum(1 for _, s in colonna_numeri if re.search(r"\d", s["text"])) == len(indice)

# pag. 6 dell'indice: nel PDF le righe "by ..." risalgono man mano e dalla 5ª voce si sovrappongono ai titoli.
# Si riscrivono titoli e autori della pagina, ogni autore 14 punti sotto il suo titolo.
SOVRAPPOSTI = 6
NUMERI_FONT_CORSIVO = r"C:\Windows\Fonts\timesi.ttf"
da_riscrivere = []
for b in d[SOVRAPPOSTI - 1].get_text("dict")["blocks"]:
    for l in b.get("lines", []):
        for s in l["spans"]:
            if s["bbox"][0] < 300 and s["text"].strip() and s["text"].strip() != "CONTENTS":
                da_riscrivere.append(s)
da_riscrivere.sort(key=lambda s: s["origin"][1])

for n in PAGINE_INDICE:
    for _, s in [x for x in colonna_numeri if x[0] == n]:
        d[n - 1].add_redact_annot(pymupdf.Rect(s["bbox"]))
    if n == SOVRAPPOSTI:
        for s in da_riscrivere:
            d[n - 1].add_redact_annot(pymupdf.Rect(s["bbox"]))
    d[n - 1].apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)

ultima_base = None
for s in da_riscrivere:
    autore = s["text"].strip().startswith("by ")
    base = ultima_base + 14 if autore and ultima_base else s["origin"][1]
    if not autore:
        ultima_base = base
    d[SOVRAPPOSTI - 1].insert_text((s["origin"][0], base), s["text"].strip().rstrip(","), fontsize=s["size"],
                                   fontname="corsivo" if autore else "numeri",
                                   fontfile=NUMERI_FONT_CORSIVO if autore else NUMERI_FONT,
                                   color=pymupdf.sRGB_to_pdf(s["color"]))

print("numeri tolti dall'indice:", len(colonna_numeri), "pezzi di testo")

cartella = os.path.join(QUI, "pagine-en")
os.makedirs(cartella, exist_ok=True)
dimensioni = []
for i, p in enumerate(d):
    p = rifatte.get(i + 1, p)
    z = LARGHEZZA / p.rect.width
    pix = p.get_pixmap(matrix=pymupdf.Matrix(z, z))
    Image.frombytes("RGB", (pix.width, pix.height), pix.samples).save(
        os.path.join(cartella, f"{i + 1:03d}.webp"), "WEBP", quality=80, method=6)
    dimensioni.append([pix.width, pix.height])
print("immagini:", len(dimensioni))

dati = {"pagine": dimensioni, "indice": indice, "zone": zone}
with open(os.path.join(QUI, "dati-en.js"), "w", encoding="utf-8") as f:
    testo = json.dumps(dati, ensure_ascii=False, indent=1)
    testo = re.sub(r"\[\s+(\d+),\s+(\d+)\s+\]", r"[\1, \2]", testo)
    testo = re.sub(r"\{\s+(\"x\"[^}]*?)\s+\}", lambda m: "{" + re.sub(r"\s+", " ", m.group(1)) + "}", testo)
    f.write("// Generato da crea_pagine_en.py: non modificare a mano\n")
    f.write("const LIBRO_EN = " + testo + ";\n")
print("dati-en.js scritto")
