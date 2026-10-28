# Copertina e frontespizio dell'edizione inglese: nel PDF il titolo è rimasto in italiano ("15 anni di NOI", disegnato
# a tracciati). Qui si cancellano "15 anni" e "di NOI" (si tiene "LUTE") e si scrive "15 Years of US" con lo stesso colore.
# Usato da crea_pagine_en.py prima di creare le immagini (il PDF originale non viene modificato).
import pymupdf

FONT_CORSIVO = r"C:\Windows\Fonts\georgiaz.ttf"   # Georgia grassetto corsivo, simile a "15 anni"
FONT_TONDO = r"C:\Windows\Fonts\georgia.ttf"       # Georgia, simile a "di NOI"

# per pagina: zona da cancellare, colore, posizione delle due righe (x sinistra, x destra, linea di base, altezza)
PAGINE = {
    1: {"cancella": (110, 205, 318, 338), "colore": (0.341, 0.220, 0.110),
        "riga2": (127, 309, 260, 44), "riga3": (116, 305, 335, 53)},
    2: {"cancella": (120, 276, 312, 396), "colore": (0.694, 0.702, 0.714),
        "riga2": (136, 303, 323, 41), "riga3": (126, 300, 392, 50)},
}

def scrivi(page, testo, fontfile, nome, x0, x1, base, altezza, colore):
    # dimensione tale che le maiuscole siano alte come quelle originali, centrato fra x0 e x1
    f = pymupdf.Font(fontfile=fontfile)
    size = altezza / f.ascender * 0.98
    larg = f.text_length(testo, fontsize=size)
    if larg > (x1 - x0) * 1.08:
        size *= (x1 - x0) * 1.08 / larg
        larg = f.text_length(testo, fontsize=size)
    x = (x0 + x1) / 2 - larg / 2
    page.insert_text((x, base), testo, fontsize=size, fontname=nome, fontfile=fontfile, color=colore)

def titolo_inglese(doc):
    for n, c in PAGINE.items():
        p = doc[n - 1]
        p.add_redact_annot(pymupdf.Rect(*c["cancella"]))
        p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                           graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED, text=pymupdf.PDF_REDACT_TEXT_REMOVE)
        x0, x1, base, alt = c["riga2"]
        scrivi(p, "15 Years", FONT_CORSIVO, "corsivo", x0, x1, base, alt, c["colore"])
        # "of US": "of" piccolo come "di", "US" grande come "NOI"
        x0, x1, base, alt = c["riga3"]
        fo, fu = pymupdf.Font(fontfile=FONT_TONDO), pymupdf.Font(fontfile=FONT_TONDO)
        s_of, s_us = alt * 0.62 / fo.ascender, alt / fu.ascender * 0.98
        l_of, l_us = fo.text_length("of ", fontsize=s_of), fu.text_length("US", fontsize=s_us)
        x = (x0 + x1) / 2 - (l_of + l_us) / 2
        p.insert_text((x, base - alt * 0.38), "of", fontsize=s_of, fontname="tondo", fontfile=FONT_TONDO, color=c["colore"])
        p.insert_text((x + l_of, base), "US", fontsize=s_us, fontname="tondo", fontfile=FONT_TONDO, color=c["colore"])

if __name__ == "__main__":
    # prova: crea anteprima_titolo.png con le due pagine
    from PIL import Image
    d = pymupdf.open(r"C:\Users\Filippo\Desktop\Book 15 Years Lute.pdf")
    titolo_inglese(d)
    ims = []
    for n in (1, 2):
        pix = d[n - 1].get_pixmap(dpi=110)
        ims.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
    f = Image.new("RGB", (ims[0].width + ims[1].width + 10, max(i.height for i in ims)), "white")
    f.paste(ims[0], (0, 0)); f.paste(ims[1], (ims[0].width + 10, 0))
    f.save("anteprima_titolo.png")
    print("anteprima_titolo.png")
