// Sfogliatore del libro "LUTE · 15 anni di NOI" in italiano e in inglese: pagine una sotto l'altra, indice cliccabile.
// I dati (dimensioni delle pagine, voci dell'indice, zone cliccabili) sono in dati.js (IT) e dati-en.js (EN).
// Numeri di pagina: in entrambe le lingue "pagina N" = pagina N+1 del PDF (copertina = PDF 1).
(function () {
  // ---------- le due edizioni, con gli stessi campi
  function paginaIndice(zone) { return Math.min.apply(null, Object.keys(zone).map(Number)); }
  var EDIZIONI = {
    it: {
      cartella: 'pagine',
      pagine: LIBRO.pagine,
      indice: LIBRO.indice.map(function (v) { return { titolo: v.titolo, autore: v.autore, pdf: v.pag + LIBRO.scarto }; }),
      zone: LIBRO.zone, campoZona: function (z) { return z.pag + LIBRO.scarto; },
      sedi: 4,
      testi: {
        titolo: 'LUTE · <em>15 anni di NOI</em>', titoloPagina: 'LUTE · 15 anni di NOI',
        indice: 'Indice', pag: 'Pag.', copertina: 'Copertina', sedi: 'Le sedi della LUTE', indiceLibro: 'Indice del libro',
        quarta: 'Quarta di copertina', pagina: 'Pagina', vai: 'Vai alla pagina', prima: 'Pagina precedente', dopo: 'Pagina successiva',
        chiudi: "Chiudi l'indice", meno: 'Pagine più piccole', piu: 'Pagine più grandi',
        suggerimento: 'Tocca un titolo dell’indice per andare alla sua pagina'
      }
    },
    en: {
      cartella: 'pagine-en',
      pagine: LIBRO_EN.pagine,
      indice: LIBRO_EN.indice,
      zone: LIBRO_EN.zone, campoZona: function (z) { return z.pdf; },
      sedi: 4,
      testi: {
        titolo: 'LUTE · <em>15 Years of Us</em>', titoloPagina: 'LUTE · 15 Years of Us',
        indice: 'Contents', pag: 'Page', copertina: 'Cover', sedi: 'The venues of LUTE', indiceLibro: 'Table of contents',
        quarta: 'Back cover', pagina: 'Page', vai: 'Go to page', prima: 'Previous page', dopo: 'Next page',
        chiudi: 'Close the contents', meno: 'Smaller pages', piu: 'Larger pages',
        suggerimento: 'Tap a title in the contents to go to its page'
      }
    }
  };
  var ZOOM = [520, 640, 760, 900, 1050, 1200];
  var VERSIONE_PAGINE = 3;   // da aumentare quando si rifanno le immagini delle pagine

  var libro = document.getElementById('libro');
  var elenco = document.getElementById('elenco');
  var numPag = document.getElementById('numPag');
  var velo = document.getElementById('velo');
  var btnIndice = document.getElementById('btnIndice');
  var schermoPiccolo = window.matchMedia('(max-width: 1000px)');

  var lingua, ed, TOT, figure = [], linkVoci = [], corrente = 1;

  function idPagina(pdf) { return pdf === 1 ? 'copertina' : 'pagina-' + (pdf - 1); }
  function pdfDaNumero(n) { return Math.min(TOT, Math.max(1, n + 1)); }
  function etichetta(pdf) { return pdf === 1 ? '' : String(pdf - 1); }

  // ---------- disegna l'edizione nella lingua scelta
  function disegna() {
    var t = ed.testi;
    document.documentElement.lang = lingua;
    document.title = t.titoloPagina;
    document.getElementById('titolo').innerHTML = t.titolo;
    document.getElementById('etichettaIndice').textContent = t.indice;
    document.getElementById('titoloIndice').textContent = t.indice;
    document.getElementById('etichettaPag').textContent = t.pag;
    numPag.setAttribute('aria-label', t.vai);
    document.getElementById('btnPrima').setAttribute('aria-label', t.prima);
    document.getElementById('btnDopo').setAttribute('aria-label', t.dopo);
    document.getElementById('btnChiudi').setAttribute('aria-label', t.chiudi);
    document.getElementById('zoomMeno').setAttribute('aria-label', t.meno);
    document.getElementById('zoomPiu').setAttribute('aria-label', t.piu);
    document.querySelectorAll('.lingue button').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.lingua === lingua));
    });
    document.getElementById('totPag').textContent = '/ ' + (TOT - 1);

    // pagine
    var primaIndice = paginaIndice(ed.zone);
    var frammento = document.createDocumentFragment();
    figure = [];
    ed.pagine.forEach(function (dim, i) {
      var pdf = i + 1;
      if (pdf === primaIndice) {
        var s = document.createElement('p');
        s.className = 'suggerimento';
        s.textContent = t.suggerimento;
        frammento.appendChild(s);
      }
      var f = document.createElement('figure');
      f.className = 'pagina';
      f.id = idPagina(pdf);
      var img = document.createElement('img');
      img.src = ed.cartella + '/' + String(pdf).padStart(3, '0') + '.webp?v=' + VERSIONE_PAGINE;
      img.width = dim[0];
      img.height = dim[1];
      img.alt = pdf === 1 ? t.copertina : t.pagina + ' ' + etichetta(pdf);
      img.decoding = 'async';
      if (pdf > 2) img.loading = 'lazy';
      f.appendChild(img);
      (ed.zone[pdf] || []).forEach(function (z) {
        var dest = ed.campoZona(z);
        var voce = ed.indice.filter(function (v) { return v.pdf === dest; })[0];
        var a = document.createElement('a');
        a.className = 'zona';
        a.href = '#' + idPagina(dest);
        a.style.left = z.x + '%';
        a.style.top = z.y + '%';
        a.style.width = z.w + '%';
        a.style.height = z.h + '%';
        a.setAttribute('aria-label', (voce ? voce.titolo + ', ' : '') + t.pagina.toLowerCase() + ' ' + etichetta(dest));
        f.appendChild(a);
      });
      figure.push(f);
      frammento.appendChild(f);
    });
    libro.replaceChildren(frammento);

    // indice laterale: inizio del libro, voci dell'indice, fine
    var voci = [
      { titolo: t.copertina, pdf: 1 },
      { titolo: t.sedi, pdf: ed.sedi },
      { titolo: t.indiceLibro, pdf: primaIndice },
      { separa: true }
    ].concat(ed.indice.map(function (v) { return { titolo: v.titolo, autore: v.autore, pdf: v.pdf, num: true }; }),
             [{ separa: true }, { titolo: t.quarta, pdf: TOT }]);
    elenco.replaceChildren();
    linkVoci = [];
    voci.forEach(function (v) {
      var li = document.createElement('li');
      if (v.separa) { li.className = 'separa'; li.setAttribute('aria-hidden', 'true'); elenco.appendChild(li); return; }
      var a = document.createElement('a');
      a.href = '#' + idPagina(v.pdf);
      a.dataset.pdf = v.pdf;
      var s = document.createElement('span');
      s.className = 'voce__titolo';
      s.textContent = v.titolo;
      a.appendChild(s);
      if (v.autore) {
        s = document.createElement('span');
        s.className = 'voce__autore';
        s.textContent = v.autore;
        a.appendChild(s);
      }
      if (v.num) {
        s = document.createElement('span');
        s.className = 'voce__pag';
        s.textContent = etichetta(v.pdf);
        a.appendChild(s);
      }
      li.appendChild(a);
      elenco.appendChild(li);
      linkVoci.push(a);
    });
  }

  // ---------- cambio di lingua: si resta allo stesso punto del capitolo che si sta leggendo
  function capitoloDi(e, pdf) {
    var k = -1;
    e.indice.forEach(function (v, i) { if (v.pdf <= pdf) k = i; });
    return k;
  }
  function pdfCorrispondente(da, a, pdf) {
    if (pdf === da.pagine.length) return a.pagine.length;          // quarta di copertina
    var k = capitoloDi(da, pdf);
    if (k < 0) return pdf;                                          // pagine iniziali: uguali
    var fine = k + 1 < a.indice.length ? a.indice[k + 1].pdf - 1 : a.pagine.length - 1;
    return Math.min(a.indice[k].pdf + (pdf - da.indice[k].pdf), fine);
  }
  function scegliLingua(l, primaVolta) {
    if (!EDIZIONI[l] || l === lingua) return;
    var precedente = ed, pdf = corrente;
    lingua = l;
    ed = EDIZIONI[l];
    TOT = ed.pagine.length;
    try { localStorage.setItem('libro_lute_lingua', l); } catch (e) {}
    if (/[?&]lang=/.test(location.search)) {
      history.replaceState(null, '', location.pathname + location.search.replace(/([?&]lang=)[a-z]+/, '$1' + l) + location.hash);
    }
    disegna();
    if (!primaVolta) vaiA(pdfCorrispondente(precedente, ed, pdf), false);
  }
  document.querySelectorAll('.lingue button').forEach(function (b) {
    b.addEventListener('click', function () { scegliLingua(b.dataset.lingua); });
  });

  // ---------- apertura e chiusura dell'indice
  function indiceAperto() {
    return schermoPiccolo.matches ? document.body.classList.contains('indice-aperto')
                                  : !document.body.classList.contains('senza-indice');
  }
  function mostraIndice(si) {
    if (schermoPiccolo.matches) {
      document.body.classList.toggle('indice-aperto', si);
      velo.hidden = !si;
      if (si) {
        var att = elenco.querySelector('[aria-current="true"]');
        if (att) att.scrollIntoView({ block: 'center' });
      }
    } else {
      document.body.classList.toggle('senza-indice', !si);
    }
    btnIndice.setAttribute('aria-expanded', String(si));
  }
  btnIndice.addEventListener('click', function () { mostraIndice(!indiceAperto()); });
  document.getElementById('btnChiudi').addEventListener('click', function () { mostraIndice(false); });
  velo.addEventListener('click', function () { mostraIndice(false); });
  schermoPiccolo.addEventListener('change', function () {
    document.body.classList.remove('indice-aperto', 'senza-indice');
    velo.hidden = true;
    btnIndice.setAttribute('aria-expanded', String(!schermoPiccolo.matches));
  });
  btnIndice.setAttribute('aria-expanded', String(!schermoPiccolo.matches));

  // ---------- spostamenti
  function vaiA(pdf, dolce) {
    pdf = Math.min(TOT, Math.max(1, pdf));
    var f = figure[pdf - 1];
    f.scrollIntoView({ behavior: dolce ? 'smooth' : 'auto', block: 'start' });
    history.replaceState(null, '', location.pathname + location.search + '#' + f.id);
    aggiorna(pdf);
  }
  function pdfDaId(id) {
    if (id === 'copertina') return 1;
    var m = /^pagina-(\d+)$/.exec(id);
    return m ? pdfDaNumero(parseInt(m[1], 10)) : 0;
  }

  // tutti i link interni (indice laterale e zone sulle pagine dell'indice)
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a) return;
    var pdf = pdfDaId(a.getAttribute('href').slice(1));
    if (!pdf) return;
    e.preventDefault();
    if (schermoPiccolo.matches) mostraIndice(false);
    vaiA(pdf, Math.abs(pdf - corrente) <= 2);
  });

  document.getElementById('btnPrima').addEventListener('click', function () { vaiA(corrente - 1, true); });
  document.getElementById('btnDopo').addEventListener('click', function () { vaiA(corrente + 1, true); });
  document.getElementById('vai').addEventListener('submit', function (e) {
    e.preventDefault();
    var n = parseInt(numPag.value, 10);
    if (!isNaN(n)) vaiA(n <= 0 ? 1 : pdfDaNumero(n), false);
    numPag.blur();
  });
  numPag.addEventListener('focus', function () { numPag.select(); });
  numPag.addEventListener('blur', function () { numPag.value = etichetta(corrente); });

  document.addEventListener('keydown', function (e) {
    if (e.target === numPag) return;
    if (e.key === 'ArrowRight') { vaiA(corrente + 1, true); e.preventDefault(); }
    else if (e.key === 'ArrowLeft') { vaiA(corrente - 1, true); e.preventDefault(); }
    else if (e.key === 'Escape' && schermoPiccolo.matches) mostraIndice(false);
  });

  // ---------- ingrandimento (computer): la pagina corrente resta al suo posto
  var livello = ZOOM.indexOf(760);
  try { var salvato = parseInt(localStorage.getItem('libro_lute_zoom'), 10); if (ZOOM[salvato]) livello = salvato; } catch (e) {}
  function applicaZoom() {
    document.documentElement.style.setProperty('--larghezza', ZOOM[livello] + 'px');
    try { localStorage.setItem('libro_lute_zoom', livello); } catch (e) {}
  }
  function cambiaZoom(d) {
    var pdf = corrente;
    livello = Math.min(ZOOM.length - 1, Math.max(0, livello + d));
    applicaZoom();
    figure[pdf - 1].scrollIntoView({ block: 'start' });
  }
  document.getElementById('zoomMeno').addEventListener('click', function () { cambiaZoom(-1); });
  document.getElementById('zoomPiu').addEventListener('click', function () { cambiaZoom(1); });
  applicaZoom();

  // ---------- pagina corrente: quella che occupa la parte alta dello schermo
  function aggiorna(pdf) {
    corrente = pdf;
    if (document.activeElement !== numPag) numPag.value = etichetta(pdf);
    var attiva = null;
    linkVoci.forEach(function (a) { if (+a.dataset.pdf <= pdf) attiva = a; });
    linkVoci.forEach(function (a) { a.setAttribute('aria-current', String(a === attiva)); });
  }
  function calcola() {
    var y = window.innerHeight * 0.35;
    var lo = 0, hi = figure.length - 1;
    while (lo < hi) {
      var mid = (lo + hi + 1) >> 1;
      if (figure[mid].getBoundingClientRect().top <= y) lo = mid; else hi = mid - 1;
    }
    return lo + 1;
  }
  var inAttesa = false, timerHash;
  window.addEventListener('scroll', function () {
    if (inAttesa) return;
    inAttesa = true;
    requestAnimationFrame(function () {
      inAttesa = false;
      var pdf = calcola();
      if (pdf !== corrente) aggiorna(pdf);
      clearTimeout(timerHash);
      timerHash = setTimeout(function () {
        history.replaceState(null, '', location.pathname + location.search + '#' + idPagina(corrente));
      }, 400);
    });
  }, { passive: true });

  // ---------- all'apertura: lingua dall'indirizzo (?lang=en), poi la provenienza, poi quella salvata, poi quella del telefono
  // Provenienza: dal sito lutemilazzo.org non tradotto (sito Erasmus in italiano) -> italiano;
  // dal sito LUTE tradotto da Google (sito Erasmus in un'altra lingua) -> inglese.
  var m = /[?&]lang=(it|en)(?![a-z])/.exec(location.search);
  var iniziale = m && m[1];
  var da = '';
  try { da = document.referrer ? new URL(document.referrer).hostname : ''; } catch (e) {}
  if (!iniziale && /(^|\.)lutemilazzo\.org$/.test(da)) iniziale = 'it';
  if (!iniziale && /(^|\.)translate\.goog$|^translate\.google\./.test(da)) iniziale = 'en';
  if (!iniziale) { try { iniziale = localStorage.getItem('libro_lute_lingua'); } catch (e) {} }
  if (!EDIZIONI[iniziale]) iniziale = /^it/i.test(navigator.language || '') ? 'it' : 'en';
  scegliLingua(iniziale, true);

  var dalHash = pdfDaId(location.hash.slice(1));
  if (dalHash > 1) vaiA(dalHash, false); else aggiorna(1);
  window.addEventListener('hashchange', function () {
    var pdf = pdfDaId(location.hash.slice(1));
    if (pdf) vaiA(pdf, false);
  });
})();
