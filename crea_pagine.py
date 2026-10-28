# Crea le immagini delle pagine (pagine/001.webp ...) e dati.js a partire dal PDF del libro.
# Uso: python crea_pagine.py   (rifà tutto: da lanciare se cambia il PDF)
import os, re, json, sys, unicodedata
import pymupdf
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
PDF = r"C:\Users\Filippo\Desktop\Libro Lute..pdf"
QUI = os.path.dirname(os.path.abspath(__file__))
LARGHEZZA = 1100            # pixel di larghezza di ogni pagina
PAGINE_INDICE = range(6, 11)  # pagine del PDF che contengono l'indice
SCARTO = 1                  # pagina del PDF = numero stampato + 1

d = pymupdf.open(PDF)

# ---------- immagini delle pagine
cartella = os.path.join(QUI, "pagine")
os.makedirs(cartella, exist_ok=True)
dimensioni = []
for i, p in enumerate(d):
    z = LARGHEZZA / p.rect.width
    pix = p.get_pixmap(matrix=pymupdf.Matrix(z, z))
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    img.save(os.path.join(cartella, f"{i + 1:03d}.webp"), "WEBP", quality=80, method=6)
    dimensioni.append([pix.width, pix.height])
print("immagini:", len(dimensioni))

# ---------- indice: titoli, autori, pagina e zona cliccabile su ogni pagina dell'indice
def righe(p):
    out = []
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            t = "".join(s["text"] for s in l["spans"]).strip()
            if t:
                out.append((l["bbox"], t))
    return out

indice, zone = [], {}
for n in PAGINE_INDICE:
    p = d[n - 1]
    tutte = righe(p)
    sinistra = sorted([r for r in tutte if r[0][0] < 300 and r[1] != "INDICE"], key=lambda r: r[0][1])
    numeri = sorted([r for r in tutte if r[0][0] > 330 and re.search(r"\d", r[1])], key=lambda r: r[0][1])
    zone[n] = []
    for k, (bb, t) in enumerate(numeri):
        pag = int(re.search(r"\d+", t).group())
        y_fine = numeri[k + 1][0][1] if k + 1 < len(numeri) else 1e9
        gruppo = [r for r in sinistra if bb[1] - 3 <= r[0][1] < y_fine - 3]
        titolo = [g[1] for g in gruppo if not g[1].startswith("di ")]
        autore = next((g[1][3:] for g in gruppo if g[1].startswith("di ")), "")
        indice.append({"titolo": " – ".join(titolo), "autore": autore, "pag": pag})
        x0 = min(g[0][0] for g in gruppo) - 4
        y0 = bb[1] - 3
        x1 = bb[2] + 4
        y1 = max(g[0][3] for g in gruppo) + 1
        W, H = p.rect.width, p.rect.height
        zone[n].append({"x": round(x0 / W * 100, 2), "y": round(y0 / H * 100, 2),
                        "w": round((x1 - x0) / W * 100, 2), "h": round((y1 - y0) / H * 100, 2), "pag": pag})

# "Prefazione La grande..." -> "Prefazione – La grande..."; refusi dell'indice stampato (il titolo giusto è nel capitolo)
CORREZIONI = {"Una grade famiglia": "Una grande famiglia"}
for v in indice:
    v["titolo"] = re.sub(r"^Prefazione ", "Prefazione – ", v["titolo"])
    v["titolo"] = CORREZIONI.get(v["titolo"], v["titolo"])

# controllo: il titolo deve comparire nella pagina indicata
def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return re.sub(r"[^a-z0-9 ]", " ", "".join(c for c in s if not unicodedata.combining(c)))
for v in indice:
    testo = norm(d[v["pag"] + SCARTO - 1].get_text())
    parole = [w for w in norm(v["titolo"].split(" – ")[-1]).split() if len(w) > 3][:3]
    if not all(w in testo for w in parole):
        print("DA CONTROLLARE:", v["pag"], v["titolo"], parole)
print("voci dell'indice:", len(indice))

dati = {"pagine": dimensioni, "scarto": SCARTO, "indice": indice, "zone": zone}
with open(os.path.join(QUI, "dati.js"), "w", encoding="utf-8") as f:
    f.write("// Generato da crea_pagine.py: non modificare a mano\n")
    testo = json.dumps(dati, ensure_ascii=False, indent=1)
    testo = re.sub(r"\[\s+(\d+),\s+(\d+)\s+\]", r"[\1, \2]", testo)  # [larghezza, altezza] su una riga
    testo = re.sub(r"\{\s+(\"x\"[^}]*?)\s+\}", lambda m: "{" + re.sub(r"\s+", " ", m.group(1)) + "}", testo)  # zone su una riga
    f.write("const LIBRO = " + testo + ";\n")
print("dati.js scritto")
