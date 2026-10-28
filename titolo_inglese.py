# Prime pagine dell'edizione inglese, rifatte partendo da quelle italiane (che sono corrette):
#  - pag. 1 copertina e pag. 2 frontespizio: nel PDF inglese lo sfondo della copertina è grigio invece che crema
#    e il titolo è rimasto "15 anni di NOI". Si prende la pagina italiana, si cancellano "15 anni" e "di NOI"
#    (disegnati a tracciati; si tiene "LUTE") e si scrive "15 Years of US" con lo stesso colore.
#  - pag. 4 "Le sedi della LUTE": nel PDF inglese i nomi nei cerchi sono storpiati (es. "SAINT HIPPUS DEL MELA").
#    Si prende la pagina italiana (i nomi dei paesi restano in italiano) e si traduce solo l'intestazione.
# Usato da crea_pagine_en.py. I PDF originali non vengono modificati.
import pymupdf

PDF_IT = r"C:\Users\Filippo\Desktop\Libro Lute..pdf"
FONT_CORSIVO = r"C:\Windows\Fonts\georgiaz.ttf"   # Georgia grassetto corsivo, simile a "15 anni"
FONT_TONDO = r"C:\Windows\Fonts\georgia.ttf"       # Georgia, simile a "di NOI"
FONT_INTESTAZIONE = r"C:\Windows\Fonts\times.ttf"  # come "LE SEDI DELLA LUTE"

# copertina e frontespizio: zona da cancellare, colore, righe (x sinistra, x destra, linea di base, altezza maiuscole)
TITOLO = {
    1: {"cancella": (110, 205, 318, 338), "colore": (0.341, 0.220, 0.110),
        "riga2": (127, 309, 260, 44), "riga3": (116, 305, 335, 53)},
    2: {"cancella": (120, 276, 312, 396), "colore": (0.694, 0.702, 0.714),
        "riga2": (136, 303, 323, 41), "riga3": (126, 300, 392, 50)},
}
# pagina delle sedi: intestazione (nell'immagine) da coprire e riscrivere
SEDI = {"pagina": 4, "copri": (85, 62, 340, 90), "testo": "THE VENUES OF LUTE", "base": 83, "altezza": 15,
        "colore": (0.19, 0.18, 0.185)}

def scrivi_centrato(page, testo, fontfile, nome, x0, x1, base, altezza, colore, allarga=1.08):
    f = pymupdf.Font(fontfile=fontfile)
    size = altezza / f.ascender * 0.98
    larg = f.text_length(testo, fontsize=size)
    if larg > (x1 - x0) * allarga:
        size *= (x1 - x0) * allarga / larg
        larg = f.text_length(testo, fontsize=size)
    page.insert_text(((x0 + x1) / 2 - larg / 2, base), testo, fontsize=size, fontname=nome, fontfile=fontfile, color=colore)

def titolo(p, c):
    p.add_redact_annot(pymupdf.Rect(*c["cancella"]))
    p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                       graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED, text=pymupdf.PDF_REDACT_TEXT_REMOVE)
    x0, x1, base, alt = c["riga2"]
    scrivi_centrato(p, "15 Years", FONT_CORSIVO, "corsivo", x0, x1, base, alt, c["colore"])
    # "of US": "of" piccolo e rialzato come "di", "US" grande come "NOI"
    x0, x1, base, alt = c["riga3"]
    f = pymupdf.Font(fontfile=FONT_TONDO)
    s_of, s_us = alt * 0.62 / f.ascender, alt / f.ascender * 0.98
    l_of, l_us = f.text_length("of ", fontsize=s_of), f.text_length("US", fontsize=s_us)
    x = (x0 + x1) / 2 - (l_of + l_us) / 2
    p.insert_text((x, base - alt * 0.38), "of", fontsize=s_of, fontname="tondo", fontfile=FONT_TONDO, color=c["colore"])
    p.insert_text((x + l_of, base), "US", fontsize=s_us, fontname="tondo", fontfile=FONT_TONDO, color=c["colore"])

def pagine_iniziali_en():
    """Restituisce {numero di pagina: pagina pronta} per le pagine iniziali dell'edizione inglese."""
    it = pymupdf.open(PDF_IT)
    doc = pymupdf.open()
    numeri = [1, 2, SEDI["pagina"]]
    for n in numeri:
        doc.insert_pdf(it, from_page=n - 1, to_page=n - 1)
    pagine = {n: doc[k] for k, n in enumerate(numeri)}
    for n, c in TITOLO.items():
        titolo(pagine[n], c)
    p = pagine[SEDI["pagina"]]
    p.draw_rect(pymupdf.Rect(*SEDI["copri"]), color=None, fill=(1, 1, 1))
    x0, _, x1, _ = SEDI["copri"]
    scrivi_centrato(p, SEDI["testo"], FONT_INTESTAZIONE, "times", x0, x1, SEDI["base"], SEDI["altezza"], SEDI["colore"], 0.95)
    pagine["_doc"] = doc   # tiene vivo il documento finché servono le pagine
    return pagine

if __name__ == "__main__":
    # prova: crea anteprima-pagine-iniziali-en.png
    from PIL import Image
    pg = pagine_iniziali_en()
    ims = []
    for n in (1, 2, 4):
        pix = pg[n].get_pixmap(dpi=100)
        ims.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
    f = Image.new("RGB", (sum(i.width for i in ims) + 20, max(i.height for i in ims)), "white")
    x = 0
    for i in ims:
        f.paste(i, (x, 0)); x += i.width + 10
    f.save("anteprima-pagine-iniziali-en.png")
    print("anteprima-pagine-iniziali-en.png")
