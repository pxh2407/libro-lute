# Crea copertina.jpg (1200x630): l'immagine che compare quando si condivide il link (WhatsApp, Facebook...).
# Uso: python crea_copertina.py   (dopo crea_pagine.py)
import os
from PIL import Image, ImageDraw, ImageFont

QUI = os.path.dirname(os.path.abspath(__file__))
MARRONE, CREMA, VERDE = (27, 94, 63), (255, 255, 255), (222, 190, 110)  # verde, bianco e oro del sito LUTE
FONT = r"C:\Windows\Fonts\georgia.ttf"
FONT_I = r"C:\Windows\Fonts\georgiai.ttf"

W, H = 1200, 630
img = Image.new("RGB", (W, H), MARRONE)
cop = Image.open(os.path.join(QUI, "pagine", "001.webp")).convert("RGB")
h = H - 60
cop = cop.resize((round(cop.width * h / cop.height), h), Image.LANCZOS)
img.paste(cop, (50, 30))

d = ImageDraw.Draw(img)
x = 50 + cop.width + 60
d.text((x, 150), "LUTE", font=ImageFont.truetype(FONT, 84), fill=CREMA)
d.text((x, 250), "15 anni di NOI", font=ImageFont.truetype(FONT_I, 64), fill=CREMA)
d.line((x, 352, W - 60, 352), fill=(168, 132, 44), width=3)
d.text((x, 380), "Il libro da sfogliare online", font=ImageFont.truetype(FONT, 38), fill=VERDE)
d.text((x, 440), "Libera Università della Terza Età", font=ImageFont.truetype(FONT, 30), fill=CREMA)
d.text((x, 480), "Milazzo", font=ImageFont.truetype(FONT, 30), fill=CREMA)
img.save(os.path.join(QUI, "copertina.jpg"), quality=85)
print("copertina.jpg creata")
