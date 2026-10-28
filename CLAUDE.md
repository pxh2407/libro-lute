# Libro LUTE · 15 anni di NOI — sfogliatore web

App HTML-CSS-JS (statica, senza librerie) per leggere online il libro "LUTE · 15 anni di NOI" (LUTE Milazzo, marzo 2026, 211 pagine). Creata il 2026-10-28.

## File
- `index.html`, `style.css`, `app.js` — l'app. Cache busting `?v=N` in index.html: incrementarlo a ogni modifica.
- `dati.js` — **generato** da `crea_pagine.py`: dimensioni delle pagine, voci dell'indice (titolo, autore, pagina stampata), zone cliccabili sulle pagine dell'indice. Non modificarlo a mano.
- `pagine/001.webp` … `211.webp` — le pagine del PDF in immagine (1100 px di larghezza, ~24 MB in tutto).
- `crea_pagine.py` — rifà immagini e dati.js dal PDF `C:\Users\Filippo\Desktop\Libro Lute..pdf` (`python crea_pagine.py`). Da lanciare se cambia il PDF.

## Come funziona
- Pagine una sotto l'altra (caricate man mano che si scorre). Barra in alto: Indice, pagina precedente/successiva, casella "Pag." per andare a un numero, ingrandimento (solo computer).
- Indice laterale (sul telefono si apre sopra le pagine): Copertina, Le sedi della LUTE, Indice del libro, le 48 voci, Quarta di copertina. La voce del capitolo che si sta leggendo è evidenziata.
- Sulle pagine dell'indice stampato (PDF 6-10) ogni titolo è cliccabile e porta alla sua pagina.
- **Numeri di pagina:** l'app usa i numeri stampati nel libro. Pagina del PDF = numero stampato + 1 (verificato su tutte le pagine numerate). Copertina = PDF 1.
- Indirizzo per pagina: `#pagina-43` (si può condividere un link a un capitolo). Copertina: `#copertina`.
- Frecce ← → della tastiera: pagina precedente/successiva.

## Note
- Refuso nell'indice stampato: "Una grade famiglia" (pag. 111); il capitolo si intitola "Una grande famiglia". Nell'indice laterale è corretto (`CORREZIONI` in crea_pagine.py); l'immagine della pagina dell'indice resta com'è.
- Pagina 3 del libro: "Vietata la riproduzione totale o parziale … i diritti sono riservati all'autore": prima di pubblicarlo online serve il consenso.
- Anteprima locale: configurazione `libro-lute` (porta 8795) in `ATTICO PER INTERNO\.claude\launch.json`.
- Non ancora pubblicato online (nessun repository).
