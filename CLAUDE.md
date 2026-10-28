# Libro LUTE · 15 anni di NOI — sfogliatore web

App HTML-CSS-JS (statica, senza librerie) per leggere online il libro "LUTE · 15 anni di NOI" (LUTE Milazzo, marzo 2026, 211 pagine). Creata il 2026-10-28.

**Online:** https://pxh2407.github.io/libro-lute/ (sito a sé, scelto dall'utente il 2026-10-28). Link a un capitolo: aggiungere `#pagina-N` (es. `…/libro-lute/#pagina-43`).

## Stile LUTE (2026-10-28)
- Colori del sito lutemilazzo.org: barra verde `#1b5e3f` con filo oro `#a8842c` in basso, verde scuro `#123f2a`, bianco; pulsante lingua attivo e voce d'indice attiva in oro. Variabili in cima a `style.css`.
- Logo LUTE (`logo.png`, ricavato da `CLAUDE\Logo Lute.png`) su riquadro bianco nella barra, come nel sito. Sotto 760 px resta solo il logo, senza titolo.
- Anche `copertina.jpg` (anteprima del link) è verde, bianca e oro.

## Versione inglese (2026-10-28)
- Selettore **IT | EN** nella barra in alto. Lingua: `?lang=en` nell'indirizzo, poi quella scelta e salvata (`localStorage libro_lute_lingua`), poi quella del telefono (italiano → IT, altrimenti EN).
- Il libro inglese è un PDF a parte fornito dall'utente: `C:\Users\Filippo\Desktop\Book 15 Years Lute.pdf` (217 pagine). `python crea_pagine_en.py` crea `pagine-en/` e `dati-en.js`.
- ⚠️ I numeri di pagina dell'indice stampato inglese sono COPIATI da quello italiano e non corrispondono al PDF inglese (i capitoli cadono più avanti; anche i numeri in testa alle pagine hanno salti). Lo script trova l'inizio dei capitoli dalle pagine con il titolo in caratteri grandi (48 = 48 voci, controllato). Nell'app, in entrambe le lingue, "pagina N" = pagina N+1 del PDF.
- **Prime pagine inglesi rifatte dalle italiane** (2026-10-28): nel PDF inglese la copertina ha lo sfondo grigio invece che crema, il titolo era rimasto "15 anni di NOI" e nei cerchi di pag. 4 ("The venues of the LUTE") i nomi dei paesi erano storpiati ("SAINT HIPPUS DEL MELA", "SPA DAFORA"...). `titolo_inglese.py` (usato da crea_pagine_en.py) prende le pagg. 1, 2 e 4 del PDF italiano: sulle prime due cancella "15 anni" e "di NOI" e scrive "15 Years of US" (Georgia, stesso colore); sulla 4 copre l'intestazione e scrive "THE VENUES OF LUTE" (Times); i nomi dei paesi restano in italiano. I PDF non vengono modificati. `VERSIONE_PAGINE` in app.js va aumentata quando si rifanno le immagini.
- **Indice inglese SENZA numeri di pagina** (2026-10-28, richiesta dell'utente): crea_pagine_en.py toglie dalle immagini dell'indice stampato numeri, "P." e segni » (erano copiati dall'italiano e sbagliati); anche l'indice laterale inglese non mostra numeri (`numeriIndice: false` in app.js). Si va al capitolo toccando titolo o nome dell'autore. L'edizione italiana resta con i numeri. Nella pag. 6 dell'indice le righe "by …" si sovrapponevano ai titoli già nel PDF: titoli e autori di quella pagina sono riscritti (Times / Times corsivo), autore 14 pt sotto il titolo. Sulle pagg. 9-10 il segno » è staccato dal numero.
- Cambiando lingua si resta nello stesso capitolo, alla stessa distanza dal suo inizio.
- **Arrivo dal sito Erasmus → sito LUTE → menu Documenti (2026-10-28, richiesta dell'utente; NON toccare il sito Erasmus né lutemilazzo.org):**
  - lingua Erasmus diversa dall'italiano: il sito LUTE è tradotto da Google e anche il libro si apre dentro il traduttore (`pxh2407-github-io.translate.goog/libro-lute/?_x_tr_tl=pl`). Uno script in testa a index.html esce dal traduttore e apre `https://pxh2407.github.io/libro-lute/?lang=en` (o `?lang=it` se la traduzione era verso l'italiano);
  - lingua Erasmus italiana: il libro arriva da `lutemilazzo.org` non tradotto → app.js sceglie l'italiano (dalla provenienza, `document.referrer`). Se si arriva da `translate.goog` senza passare dallo script → inglese.
  - Ordine di scelta della lingua: `?lang=` → provenienza → lingua salvata → lingua del telefono.
- Una prima traduzione fatta da Claude è stata abbandonata quando è arrivato il PDF inglese.

## File
- `pagine-en/`, `dati-en.js`, `crea_pagine_en.py` — lo stesso per l'edizione inglese.
- `index.html`, `style.css`, `app.js` — l'app. Cache busting `?v=N` in index.html: incrementarlo a ogni modifica.
- `dati.js` — **generato** da `crea_pagine.py`: dimensioni delle pagine, voci dell'indice (titolo, autore, pagina stampata), zone cliccabili sulle pagine dell'indice. Non modificarlo a mano.
- `pagine/001.webp` … `211.webp` — le pagine del PDF in immagine (1100 px di larghezza, ~24 MB in tutto).
- `crea_pagine.py` — rifà immagini e dati.js dal PDF `C:\Users\Filippo\Desktop\Libro Lute..pdf` (`python crea_pagine.py`). Da lanciare se cambia il PDF.
- `copertina.jpg` (1200×630) — anteprima del link (meta `og:*` in index.html) e icona della scheda; si rifà con `python crea_copertina.py`.
- `.nojekyll` — GitHub Pages pubblica i file così come sono.

## Come funziona
- Pagine una sotto l'altra (caricate man mano che si scorre). Barra in alto: Indice, pagina precedente/successiva, casella "Pag." per andare a un numero, ingrandimento (solo computer).
- Indice laterale (sul telefono si apre sopra le pagine): Copertina, Le sedi della LUTE, Indice del libro, le 48 voci, Quarta di copertina. La voce del capitolo che si sta leggendo è evidenziata.
- Sulle pagine dell'indice stampato (PDF 6-10) ogni titolo è cliccabile e porta alla sua pagina.
- **Numeri di pagina:** l'app usa i numeri stampati nel libro. Pagina del PDF = numero stampato + 1 (verificato su tutte le pagine numerate). Copertina = PDF 1.
- Indirizzo per pagina: `#pagina-43` (si può condividere un link a un capitolo). Copertina: `#copertina`.
- Frecce ← → della tastiera: pagina precedente/successiva.
- **Freccia "torna all'indice"** (2026-10-28): pulsante tondo verde con bordo oro in basso a destra (`#btnCima`, `.in-cima`), porta alla prima pagina dell'indice stampato (su richiesta dell'utente: NON alla copertina); nascosta prima dell'indice e sulla sua prima pagina, e quando l'indice laterale è aperto sul telefono. Etichetta "Torna all'indice" / "Back to contents".

## Note
- Refuso nell'indice stampato: "Una grade famiglia" (pag. 111); il capitolo si intitola "Una grande famiglia". Nell'indice laterale è corretto (`CORREZIONI` in crea_pagine.py); l'immagine della pagina dell'indice resta com'è.
- Pagina 3 del libro: "Vietata la riproduzione totale o parziale … i diritti sono riservati all'autore" (segnalato all'utente prima della pubblicazione).
- Anteprima locale: configurazione `libro-lute` (porta 8795) in `ATTICO PER INTERNO\.claude\launch.json`.

## Pubblicazione
- Repo https://github.com/pxh2407/libro-lute (pubblico, branch `main`), GitHub Pages dal branch `main`, cartella principale.
- Dopo ogni modifica: aggiornare questo file, incrementare `?v=N` in index.html, commit e `git push`.
- Se GitHub Pages resta in coda o fallisce: controllare `pages/builds/latest` con l'API e, se serve, `POST pages/builds` (token da `git credential fill`; `gh` non è installato).
