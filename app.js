// Sfogliatore del libro "LUTE · 15 anni di NOI": pagine una sotto l'altra, indice cliccabile.
// I dati (dimensioni delle pagine, voci dell'indice, zone cliccabili) sono in dati.js.
(function () {
  var TOT = LIBRO.pagine.length;          // pagine del PDF (1 = copertina)
  var SCARTO = LIBRO.scarto;              // pagina del PDF = numero stampato + SCARTO
  var ULTIMA_STAMPATA = TOT - SCARTO;
  var ZOOM = [520, 640, 760, 900, 1050, 1200];

  var libro = document.getElementById('libro');
  var elenco = document.getElementById('elenco');
  var numPag = document.getElementById('numPag');
  var velo = document.getElementById('velo');
  var btnIndice = document.getElementById('btnIndice');
  var schermoPiccolo = window.matchMedia('(max-width: 1000px)');

  // numero stampato <-> pagina del PDF; la copertina (PDF 1) ha id "copertina"
  function idPagina(pdf) { return pdf === 1 ? 'copertina' : 'pagina-' + (pdf - SCARTO); }
  function pdfDaStampata(n) { return Math.min(TOT, Math.max(1, n + SCARTO)); }
  function etichetta(pdf) { return pdf === 1 ? '' : String(pdf - SCARTO); }

  // ---------- pagine
  var figure = [];
  var frammento = document.createDocumentFragment();
  LIBRO.pagine.forEach(function (dim, i) {
    var pdf = i + 1;
    if (LIBRO.zone[pdf] && pdf === Math.min.apply(null, Object.keys(LIBRO.zone).map(Number))) {
      var s = document.createElement('p');
      s.className = 'suggerimento';
      s.textContent = 'Tocca un titolo dell’indice per andare alla sua pagina';
      frammento.appendChild(s);
    }
    var f = document.createElement('figure');
    f.className = 'pagina';
    f.id = idPagina(pdf);
    f.dataset.pdf = pdf;
    var img = document.createElement('img');
    img.src = 'pagine/' + String(pdf).padStart(3, '0') + '.webp';
    img.width = dim[0];
    img.height = dim[1];
    img.alt = pdf === 1 ? 'Copertina' : 'Pagina ' + etichetta(pdf);
    img.decoding = 'async';
    if (pdf > 2) img.loading = 'lazy';
    f.appendChild(img);
    (LIBRO.zone[pdf] || []).forEach(function (z) {
      var voce = LIBRO.indice.filter(function (v) { return v.pag === z.pag; })[0];
      var a = document.createElement('a');
      a.className = 'zona';
      a.href = '#pagina-' + z.pag;
      a.style.left = z.x + '%';
      a.style.top = z.y + '%';
      a.style.width = z.w + '%';
      a.style.height = z.h + '%';
      a.setAttribute('aria-label', (voce ? voce.titolo + ', ' : '') + 'pagina ' + z.pag);
      f.appendChild(a);
    });
    figure.push(f);
    frammento.appendChild(f);
  });
  libro.appendChild(frammento);
  document.getElementById('totPag').textContent = '/ ' + ULTIMA_STAMPATA;

  // ---------- indice laterale: inizio del libro, voci dell'indice, fine
  var voci = [
    { titolo: 'Copertina', pdf: 1 },
    { titolo: 'Le sedi della LUTE', pdf: 4 },
    { titolo: 'Indice del libro', pdf: Math.min.apply(null, Object.keys(LIBRO.zone).map(Number)) },
    { separa: true }
  ];
  LIBRO.indice.forEach(function (v) {
    voci.push({ titolo: v.titolo, autore: v.autore, pdf: pdfDaStampata(v.pag), pag: v.pag });
  });
  voci.push({ separa: true }, { titolo: 'Quarta di copertina', pdf: TOT });

  var linkVoci = [];
  voci.forEach(function (v) {
    var li = document.createElement('li');
    if (v.separa) { li.className = 'separa'; li.setAttribute('aria-hidden', 'true'); elenco.appendChild(li); return; }
    var a = document.createElement('a');
    a.href = '#' + idPagina(v.pdf);
    a.dataset.pdf = v.pdf;
    var t = document.createElement('span');
    t.className = 'voce__titolo';
    t.textContent = v.titolo;
    a.appendChild(t);
    if (v.autore) {
      var au = document.createElement('span');
      au.className = 'voce__autore';
      au.textContent = v.autore;
      a.appendChild(au);
    }
    if (v.pag) {
      var p = document.createElement('span');
      p.className = 'voce__pag';
      p.textContent = v.pag;
      a.appendChild(p);
    }
    li.appendChild(a);
    elenco.appendChild(li);
    linkVoci.push(a);
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
    history.replaceState(null, '', '#' + f.id);
    aggiorna(pdf);
  }
  function pdfDaId(id) {
    if (id === 'copertina') return 1;
    var m = /^pagina-(\d+)$/.exec(id);
    return m ? pdfDaStampata(parseInt(m[1], 10)) : 0;
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
    if (!isNaN(n)) vaiA(n <= 0 ? 1 : pdfDaStampata(n), false);
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
  var corrente = 1;
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
      timerHash = setTimeout(function () { history.replaceState(null, '', '#' + idPagina(corrente)); }, 400);
    });
  }, { passive: true });

  // ---------- all'apertura: pagina dall'indirizzo (es. #pagina-23), altrimenti copertina
  var iniziale = pdfDaId(location.hash.slice(1));
  if (iniziale > 1) vaiA(iniziale, false); else aggiorna(1);
  window.addEventListener('hashchange', function () {
    var pdf = pdfDaId(location.hash.slice(1));
    if (pdf) vaiA(pdf, false);
  });
})();
