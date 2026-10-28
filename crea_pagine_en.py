# Versione inglese: crea pagine-en/001.webp ... e dati-en.js dal PDF tradotto.
# I numeri dell'indice inglese sono copiati da quello italiano e non corrispondono alle pagine del PDF inglese:
# l'inizio di ogni capitolo si trova cercando le pagine con il titolo in grande.
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
from titolo_inglese import titolo_inglese
titolo_inglese(d)   # copertina e frontespizio: "15 anni di NOI" -> "15 Years of US"

cartella = os.path.join(QUI, "pagine-en")
os.makedirs(cartella, exist_ok=True)
dimensioni = []
for i, p in enumerate(d):
    z = LARGHEZZA / p.rect.width
    pix = p.get_pixmap(matrix=pymupdf.Matrix(z, z))
    Image.frombytes("RGB", (pix.width, pix.height), pix.samples).save(
        os.path.join(cartella, f"{i + 1:03d}.webp"), "WEBP", quality=80, method=6)
    dimensioni.append([pix.width, pix.height])
print("immagini:", len(dimensioni))

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

dati = {"pagine": dimensioni, "indice": indice, "zone": zone}
with open(os.path.join(QUI, "dati-en.js"), "w", encoding="utf-8") as f:
    testo = json.dumps(dati, ensure_ascii=False, indent=1)
    testo = re.sub(r"\[\s+(\d+),\s+(\d+)\s+\]", r"[\1, \2]", testo)
    testo = re.sub(r"\{\s+(\"x\"[^}]*?)\s+\}", lambda m: "{" + re.sub(r"\s+", " ", m.group(1)) + "}", testo)
    f.write("// Generato da crea_pagine_en.py: non modificare a mano\n")
    f.write("const LIBRO_EN = " + testo + ";\n")
print("dati-en.js scritto")
