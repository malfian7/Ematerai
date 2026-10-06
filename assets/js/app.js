/* E-Materai — interaksi. Vanilla JS, tanpa dependensi. */
(function () {
  'use strict';
  var doc = document, root = doc.documentElement;
  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- Konfigurasi: isi endpoint saat backend siap. Kosong = mode demo. ---- */
  var CONFIG = window.LOGOIPSUM_CONFIG || {
    endpoints: { login: '', register: '', reset: '', contact: '' },
    whatsapp: '6281234567890'
  };

  var SPA = !!window.LOGOIPSUM_SPA; /* true pada versi satu-file (routing lewat #) */
  function qparam(n) { return new URLSearchParams(SPA ? (window.LOGOIPSUM_QS || '') : location.search).get(n); }
  var cleanups = [];

  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }

  /* ---- Toast ---- */
  var toastEl, toastT;
  function toast(msg) {
    if (!toastEl) { toastEl = doc.createElement('div'); toastEl.className = 'toast'; toastEl.setAttribute('role', 'status'); doc.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add('show');
    clearTimeout(toastT); toastT = setTimeout(function () { toastEl.classList.remove('show'); }, 3200);
  }

  var header, menuBtn, panel;
  function closeMenu() { if (!panel) return; panel.classList.remove('is-open'); doc.body.classList.remove('menu-open'); menuBtn.setAttribute('aria-expanded', 'false'); menuBtn.setAttribute('aria-label', 'Buka menu'); }
  function initShell() {
  /* ---- Header & menu mobile ---- */
  header = $('.site-header');
  function onScroll() { if (header) header.classList.toggle('is-scrolled', window.scrollY > 4); }
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  menuBtn = $('.menu-btn'); panel = $('.mobile-panel');
  if (menuBtn && panel) {
    menuBtn.addEventListener('click', function () {
      var open = !panel.classList.contains('is-open');
      panel.classList.toggle('is-open', open); doc.body.classList.toggle('menu-open', open);
      menuBtn.setAttribute('aria-expanded', open); menuBtn.setAttribute('aria-label', open ? 'Tutup menu' : 'Buka menu');
      menuBtn.querySelector('use').setAttribute('href', open ? '#i-x' : '#i-menu');
    });
    doc.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeMenu(); menuBtn.querySelector('use').setAttribute('href', '#i-menu'); } });
    window.addEventListener('resize', function () { if (innerWidth > 900) closeMenu(); });
  }

    root.classList.add('js');

    /* Loader awal: tampil sebentar, lalu memudar. Ada batas waktu agar tidak pernah menahan halaman. */
    var loader = $('.loader'), t0 = Date.now();
    var ready = function () {
      if (root.classList.contains('is-ready')) return;
      var wait = reduce ? 0 : Math.max(0, 420 - (Date.now() - t0));
      setTimeout(function () {
        root.classList.add('is-ready');
        if (loader) { loader.classList.add('done'); setTimeout(function () { if (loader.parentNode) loader.parentNode.removeChild(loader); }, 500); }
      }, wait);
    };
    if (doc.readyState === 'complete') ready(); else window.addEventListener('load', ready);
    setTimeout(ready, 1600);

    /* Progres baca + tombol kembali ke atas */
    var bar = doc.createElement('div'); bar.className = 'scroll-progress'; bar.setAttribute('aria-hidden', 'true'); doc.body.appendChild(bar);
    var top = doc.createElement('button'); top.type = 'button'; top.className = 'to-top'; top.setAttribute('aria-label', 'Kembali ke atas');
    top.innerHTML = '<svg class="icon" aria-hidden="true"><use href="#i-arrow-up"/></svg>'; doc.body.appendChild(top);
    top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });
    var ticking = false;
    var prog = function () {
      ticking = false;
      var h = doc.documentElement.scrollHeight - innerHeight, y = window.scrollY;
      bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, y / h) : 0) + ')';
      top.classList.toggle('show', y > 900);
    };
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(prog); } }, { passive: true });
    window.addEventListener('resize', prog); prog();
    window.LOGOIPSUM_PROG = prog;

    /* Riak (ripple) saat tombol ditekan */
    if (!reduce) doc.addEventListener('pointerdown', function (e) {
      var el = e.target.closest && e.target.closest('.btn, .uc-tab, .ck-opt, .filter, .step-tab, .icon-btn, .presets button');
      if (!el || el.disabled || e.button !== 0) return;
      var r = el.getBoundingClientRect(), d = Math.max(r.width, r.height) * 2.2;
      var s = doc.createElement('span'); s.className = 'ripple';
      s.style.width = s.style.height = d + 'px';
      s.style.left = (e.clientX - r.left - d / 2) + 'px'; s.style.top = (e.clientY - r.top - d / 2) + 'px';
      el.appendChild(s); setTimeout(function () { if (s.parentNode) s.parentNode.removeChild(s); }, 650);
    });

    /* Indikator geser di navbar */
    var nav = $('.nav');
    if (nav) {
      var ind = doc.createElement('span'); ind.className = 'nav-ind'; ind.setAttribute('aria-hidden', 'true'); nav.appendChild(ind);
      var moveTo = function (a, instant) {
        if (!a) { ind.style.opacity = '0'; return; }
        if (instant) ind.style.transition = 'none';
        ind.style.width = a.offsetWidth + 'px'; ind.style.transform = 'translateX(' + a.offsetLeft + 'px)'; ind.style.opacity = '1';
        if (instant) { ind.offsetWidth; ind.style.transition = ''; }
      };
      var current = function () { return $('a[aria-current="page"]', nav); };
      $$('a', nav).forEach(function (a) { a.addEventListener('mouseenter', function () { moveTo(a); }); a.addEventListener('focus', function () { moveTo(a); }); });
      nav.addEventListener('mouseleave', function () { moveTo(current()); });
      window.LOGOIPSUM_NAVSYNC = function (animate) { moveTo(current(), animate !== true); };
      window.addEventListener('resize', function () { moveTo(current(), true); });
      requestAnimationFrame(function () { moveTo(current(), true); });
      if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(function () { moveTo(current(), true); });
    }

    /* Bilah loading saat pindah halaman (versi multi-file) */
    if (!SPA) doc.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href]');
      if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || a.target === '_blank') return;
      var h = a.getAttribute('href');
      if (!h || h.charAt(0) === '#' || /^(mailto:|tel:|https?:)/.test(h)) return;
      if (a.pathname === location.pathname && a.hash) return;
      root.classList.add('is-leaving');
    });
    window.addEventListener('pageshow', function () { root.classList.remove('is-leaving'); });
    $$('[data-year]').forEach(function (e) { e.textContent = new Date().getFullYear(); });
  }

  function initPage() {
    cleanups.forEach(function (f) { f(); }); cleanups = [];
  /* ---- Persiapan animasi masuk ---- */
  $$('.section .section-head, .head-row').forEach(function (h) { if (!h.closest('.reveal')) h.classList.add('reveal'); });
  $$('.cards, .values, .doc-grid, .ck-opts, .uc-docs').forEach(function (g) {
    Array.prototype.forEach.call(g.children, function (c, i) { if (!c.style.getPropertyValue('--i')) c.style.setProperty('--i', Math.min(i, 6)); });
  });
  $$('.cards > .post').forEach(function (p) { p.classList.add('reveal'); });

  /* Kerangka gambar (skeleton) sampai gambar selesai dimuat */
  $$('.post-img img, .uc-img img, .article-hero img, .figure-stamp img').forEach(function (img) {
    var box = img.parentNode; box.classList.add('sk');
    var done = function () { box.classList.add('is-loaded'); };
    if (img.complete && img.naturalWidth) done(); else { img.addEventListener('load', done); img.addEventListener('error', done); }
  });

  /* ---- Reveal saat scroll ---- */
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target; el.classList.add('in'); io.unobserve(el);
        var fin = function (ev) { if (ev && ev.target !== el) return; el.classList.remove('reveal', 'in'); el.style.removeProperty('transition-delay'); el.removeEventListener('transitionend', fin); };
        el.addEventListener('transitionend', fin); setTimeout(fin, 1400);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    $$('.reveal').forEach(function (el) { io.observe(el); }); cleanups.push(function () { io.disconnect(); });
  } else { $$('.reveal').forEach(function (el) { el.classList.add('in'); }); }

  /* ---- Stepper "Cara pembubuhan" ---- */
  var tabs = $$('.step-tab');
  if (tabs.length) {
    var panels = $$('.stage-panel'), list = $('.step-list');
    var cur = 0, timer, userTouched = false;
    var show = function (i, byUser) {
      cur = i; if (byUser) { userTouched = true; clearInterval(timer); if (list) list.classList.remove('is-auto'); }
      tabs.forEach(function (t, k) { t.setAttribute('aria-selected', k === i); t.tabIndex = k === i ? 0 : -1; });
      panels.forEach(function (p, k) { p.classList.toggle('is-on', k === i); });
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { show(i, true); });
      t.addEventListener('keydown', function (e) {
        var n = e.key === 'ArrowDown' || e.key === 'ArrowRight' ? 1 : e.key === 'ArrowUp' || e.key === 'ArrowLeft' ? -1 : 0;
        if (n) { e.preventDefault(); var j = (i + n + tabs.length) % tabs.length; show(j, true); tabs[j].focus(); }
      });
    });
    show(0); cleanups.push(function () { clearInterval(timer); });
    var sec = $('#cara');
    if (sec && 'IntersectionObserver' in window && !reduce) {
      new IntersectionObserver(function (es, o) {
        if (es[0].isIntersecting) { o.disconnect(); if (userTouched) return; if (list) list.classList.add('is-auto'); show(cur); timer = setInterval(function () { if (userTouched) return clearInterval(timer); show((cur + 1) % tabs.length); }, 5200); }
      }, { threshold: .5 }).observe(sec);
    }
  }

  /* ---- Geser posisi meterai (demo) ---- */
  var dp = $('.docpage'), ds = $('.drag-stamp');
  if (dp && ds) {
    var drag = null;
    ds.addEventListener('pointerdown', function (e) {
      var r = ds.getBoundingClientRect(); drag = { dx: e.clientX - r.left, dy: e.clientY - r.top };
      ds.setPointerCapture(e.pointerId); e.preventDefault();
    });
    ds.addEventListener('pointermove', function (e) {
      if (!drag) return;
      var p = dp.getBoundingClientRect(), s = ds.getBoundingClientRect();
      var x = Math.min(Math.max(e.clientX - drag.dx - p.left, 6), p.width - s.width - 6);
      var y = Math.min(Math.max(e.clientY - drag.dy - p.top, 6), p.height - s.height - 6);
      ds.style.left = x + 'px'; ds.style.top = y + 'px'; ds.style.bottom = 'auto';
    });
    var end = function () { if (drag && !reduce) { ds.classList.remove('stamped'); ds.offsetWidth; ds.classList.add('stamped'); } drag = null; };
    ds.addEventListener('pointerup', end); ds.addEventListener('pointercancel', end);
    ds.addEventListener('keydown', function (e) {
      var step = e.shiftKey ? 24 : 8, k = e.key, p = dp.getBoundingClientRect(), s = ds.getBoundingClientRect();
      var x = s.left - p.left, y = s.top - p.top;
      if (k === 'ArrowLeft') x -= step; else if (k === 'ArrowRight') x += step; else if (k === 'ArrowUp') y -= step; else if (k === 'ArrowDown') y += step; else return;
      e.preventDefault();
      ds.style.left = Math.min(Math.max(x, 6), p.width - s.width - 6) + 'px';
      ds.style.top = Math.min(Math.max(y, 6), p.height - s.height - 6) + 'px'; ds.style.bottom = 'auto';
    });
  }

  /* ---- Tab keperluan ---- */
  var ucTabs = $$('.uc-tab');
  if (ucTabs.length) {
    var ucShow = function (i, focus) {
      ucTabs.forEach(function (t, k) {
        var on = k === i; t.setAttribute('aria-selected', on); t.tabIndex = on ? 0 : -1;
        var pnl = doc.getElementById(t.getAttribute('aria-controls')); if (pnl) pnl.hidden = !on;
      });
      if (focus) ucTabs[i].focus();
    };
    ucTabs.forEach(function (t, i) {
      t.addEventListener('click', function () { ucShow(i); });
      t.addEventListener('keydown', function (e) {
        var n = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (e.key === 'Home') { e.preventDefault(); return ucShow(0, true); }
        if (e.key === 'End') { e.preventDefault(); return ucShow(ucTabs.length - 1, true); }
        if (n) { e.preventDefault(); ucShow((i + n + ucTabs.length) % ucTabs.length, true); }
      });
    });
  }

  /* ---- Bilah CTA seluler ---- */
  var sticky = $('.sticky-cta'), heroEl = $('.hero'), footEl = $('.site-footer');
  if (sticky && heroEl && 'IntersectionObserver' in window) {
    var heroOut = false, footIn = false;
    var sync = function () { var on = heroOut && !footIn; sticky.classList.toggle('show', on); doc.body.classList.toggle('has-sticky', on); };
    var so2 = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.target === heroEl) heroOut = !e.isIntersecting; else footIn = e.isIntersecting; }); sync();
    });
    so2.observe(heroEl); if (footEl) so2.observe(footEl);
    cleanups.push(function () { so2.disconnect(); doc.body.classList.remove('has-sticky'); });
  }

  /* ---- Cek dokumen ---- */
  var ck = $('#checker');
  if (ck) {
    var R = {
      pernyataan: ['yes', 'Perlu e-Meterai', 'Surat pernyataan termasuk dokumen yang dikenai Bea Meterai. Satu e-Meterai untuk satu dokumen.', ['beli']],
      lamaran: ['maybe', 'Ikuti ketentuan instansi', 'Surat lamaran biasa tidak selalu wajib bermeterai, tetapi banyak seleksi CPNS, PPPK, dan BUMN memintanya, terutama untuk surat pernyataan. Cek pengumuman resminya, lalu bubuhkan sebelum mengunggah.', ['beli', 'cpns']],
      perjanjian: ['yes', 'Perlu e-Meterai', 'Surat perjanjian dan kontrak, termasuk rangkapnya, dikenai Bea Meterai. Letakkan e-Meterai di dekat tanda tangan.', ['beli', 'letak']],
      kuasa: ['yes', 'Perlu e-Meterai', 'Surat kuasa termasuk surat yang sejenis dengan perjanjian dan pernyataan, sehingga dikenai Bea Meterai.', ['beli']],
      akta: ['yes', 'Dikenai Bea Meterai', 'Akta notaris dan akta PPAT beserta salinan dan kutipannya dikenai Bea Meterai. Biasanya pembubuhannya diurus oleh kantor notaris atau PPAT.', ['tanya']],
      kuitansi: ['maybe', 'Tergantung nilainya', 'Kuitansi dan tanda terima bernilai besar wajib bermeterai, sedangkan yang nilainya kecil tidak. Batas nilainya diatur dalam UU Bea Meterai. Kalau ragu, tanyakan ke tim kami.', ['beli', 'tanya']],
      ijazah: ['no', 'Tidak perlu e-Meterai', 'Segala bentuk ijazah termasuk dokumen yang tidak dikenai Bea Meterai.', ['bebas']],
      gaji: ['no', 'Tidak perlu e-Meterai', 'Tanda terima gaji, uang pensiun, dan tunjangan termasuk dokumen yang tidak dikenai Bea Meterai.', ['bebas']]
    };
    var BADGE = { yes: 'badge-ok', no: 'badge-grey', maybe: 'badge-warn' };
    var BTXT = { yes: 'Wajib', no: 'Dikecualikan', maybe: 'Tergantung' };
    var res = $('.ck-result', ck), empty = $('.ck-empty', ck), links = $('.ck-links', ck);
    var render = function (key) {
      var r = R[key]; if (!r) return;
      res.className = 'ck-result ' + r[0]; res.hidden = false; empty.classList.add('off');
      var bd = $('.badge', res); bd.className = 'badge ' + BADGE[r[0]]; bd.textContent = BTXT[r[0]];
      $('b', res).textContent = r[1]; $('p', res).textContent = r[2];
      var acts = $('.ck-acts', res); acts.innerHTML = '';
      r[3].forEach(function (k) { var a = $('[data-k="' + k + '"]', links); if (a) acts.appendChild(a.cloneNode(true)); });
    };
    $$('[data-doc]', ck).forEach(function (b) {
      b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', function () {
        $$('[data-doc]', ck).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
        var d = b.getAttribute('data-doc');
        render(d);
      });
    });
  }

  /* ---- Filter blog ---- */
  var posts = $$('[data-cat]');
  if (posts.length && $('#blog-search')) {
    var cat = 'semua', q = '', empty = $('.empty'), count = $('#blog-count');
    var apply = function () {
      var n = 0;
      posts.forEach(function (p) {
        var ok = (cat === 'semua' || p.getAttribute('data-cat') === cat) && (!q || p.getAttribute('data-text').indexOf(q) > -1);
        p.hidden = !ok; if (ok) n++;
        p.classList.remove('post-feature');
      });
      var first = posts.filter(function (p) { return !p.hidden; })[0];
      if (first && cat === 'semua' && !q) first.classList.add('post-feature');
      empty.classList.toggle('show', n === 0);
      if (count) count.textContent = n + ' artikel';
    };
    $$('.filter').forEach(function (f) {
      f.addEventListener('click', function () {
        $$('.filter').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        f.setAttribute('aria-pressed', 'true'); cat = f.getAttribute('data-f'); apply();
      });
    });
    $('#blog-search').addEventListener('input', function (e) { q = e.target.value.trim().toLowerCase(); apply(); });
    apply();
  }

  /* ---- TOC scrollspy ---- */
  var tocLinks = $$('.toc a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {}; tocLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var so = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { tocLinks.forEach(function (a) { a.classList.remove('is-on'); }); map[e.target.id].classList.add('is-on'); }
      });
    }, { rootMargin: '-90px 0px -70% 0px' });
    Object.keys(map).forEach(function (id) { var h = doc.getElementById(id); if (h) so.observe(h); }); cleanups.push(function () { so.disconnect(); });
  }

  /* ---- Share ---- */
  $$('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var url = location.href;
      var ok = function () { toast('Tautan disalin'); b.classList.add('is-done'); setTimeout(function () { b.classList.remove('is-done'); }, 1600); };
      (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(ok, function () {
        var t = doc.createElement('textarea'); t.value = url; doc.body.appendChild(t); t.select();
        try { doc.execCommand('copy'); ok(); } catch (e) { toast('Salin manual dari bilah alamat'); }
        doc.body.removeChild(t);
      });
    });
  });
  $$('[data-share]').forEach(function (a) {
    var u = encodeURIComponent(location.href), t = encodeURIComponent(doc.title), k = a.getAttribute('data-share');
    a.href = k === 'wa' ? 'https://wa.me/?text=' + t + '%20' + u
      : k === 'li' ? 'https://www.linkedin.com/sharing/share-offsite/?url=' + u
      : k === 'x' ? 'https://twitter.com/intent/tweet?text=' + t + '&url=' + u
      : 'https://www.facebook.com/sharer/sharer.php?u=' + u;
  });

  /* ==================== Form ==================== */
  var MSG = {
    required: 'Kolom ini wajib diisi.',
    email: 'Tulis alamat email yang valid, misalnya nama@email.com.',
    emailOrPhone: 'Masukkan email atau nomor ponsel yang valid.',
    phone: 'Nomor ponsel 9–13 digit, tanpa angka 0 di depan.',
    min8: 'Kata sandi minimal 8 karakter.',
    match: 'Konfirmasi kata sandi belum sama.',
    consent: 'Centang persetujuan untuk melanjutkan.',
    min10: 'Pesan minimal 10 karakter agar kami paham kebutuhan Anda.'
  };
  var rules = {
    required: function (v) { return v.trim() ? '' : MSG.required; },
    email: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) ? '' : MSG.email; },
    emailOrPhone: function (v) { v = v.trim(); return (/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) || /^(\+?62|0)?8\d{8,12}$/.test(v.replace(/[\s-]/g, ''))) ? '' : MSG.emailOrPhone; },
    phone: function (v) { return /^8\d{7,12}$/.test(v.replace(/[\s-]/g, '')) ? '' : MSG.phone; },
    min8: function (v) { return v.length >= 8 ? '' : MSG.min8; },
    min10: function (v) { return v.trim().length >= 10 ? '' : MSG.min10; },
    match: function (v, el) { var o = $(el.getAttribute('data-match')); return v === o.value && v ? '' : MSG.match; },
    consent: function (v, el) { return el.checked ? '' : MSG.consent; }
  };
  function validateField(el) {
    var list = (el.getAttribute('data-v') || '').split(' ').filter(Boolean), err = '';
    var val = el.type === 'checkbox' ? '' : el.value;
    var optional = el.hasAttribute('data-optional') && !val.trim();
    if (!optional) for (var i = 0; i < list.length && !err; i++) err = rules[list[i]](val, el);
    var f = el.closest('.field') || el.closest('.check-field');
    if (f) {
      f.classList.toggle('invalid', !!err);
      var m = $('.err span', f); if (m) m.textContent = err;
    }
    el.setAttribute('aria-invalid', err ? 'true' : 'false');
    return !err;
  }
  function validateAll(scope) {
    var bad = null;
    $$('[data-v]', scope).forEach(function (el) { if (el.closest('[hidden]')) return; if (!validateField(el) && !bad) bad = el; });
    if (bad) bad.focus();
    return !bad;
  }
  function wire(form) {
    $$('[data-v]', form).forEach(function (el) {
      var ev = el.type === 'checkbox' ? 'change' : 'blur';
      el.addEventListener(ev, function () { validateField(el); });
      el.addEventListener('input', function () { if (el.getAttribute('aria-invalid') === 'true') validateField(el); });
    });
    $$('.toggle', form).forEach(function (b) {
      b.addEventListener('click', function () {
        var inp = b.parentNode.querySelector('input'), on = inp.type === 'password';
        inp.type = on ? 'text' : 'password'; b.setAttribute('aria-pressed', on);
        b.setAttribute('aria-label', on ? 'Sembunyikan kata sandi' : 'Tampilkan kata sandi');
      });
    });
  }
  function submit(form, kind, payload, onOk) {
    var btn = $('[type=submit]', form) || $('.js-submit', form), alert = $('.alert', form);
    btn.classList.add('is-loading'); btn.disabled = true;
    var url = CONFIG.endpoints[kind];
    var done = function (ok, msg) {
      btn.classList.remove('is-loading'); btn.disabled = false;
      if (alert) { alert.className = 'alert show ' + (ok ? 'ok' : 'bad'); $('span', alert).textContent = msg; }
      if (ok && onOk) onOk();
    };
    if (!url) { // mode demo
      setTimeout(function () { done(true, 'Mode demo: formulir sudah tervalidasi, tetapi belum terhubung ke server. Isi alamat endpoint di assets/js/app.js.'); }, 800);
      return;
    }
    fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json().catch(function () { return {}; }); })
      .then(function () { done(true, 'Berhasil.'); })
      .catch(function () { done(false, 'Permintaan belum berhasil. Periksa koneksi Anda lalu coba lagi.'); });
  }
  function data(form) { var o = {}; $$('input,select,textarea', form).forEach(function (e) { if (e.name && e.type !== 'password') o[e.name] = e.type === 'checkbox' ? e.checked : e.value; }); return o; }

  /* Masuk / lupa kata sandi */
  var login = $('#form-login');
  if (login) {
    wire(login);
    login.addEventListener('submit', function (e) { e.preventDefault(); if (validateAll(login)) submit(login, 'login', data(login)); });
    var reset = $('#form-reset');
    wire(reset);
    reset.addEventListener('submit', function (e) { e.preventDefault(); if (validateAll(reset)) submit(reset, 'reset', data(reset)); });
    var go = function (v) { $('#view-login').hidden = v !== 'login'; $('#view-reset').hidden = v !== 'reset'; var f = $(v === 'login' ? '#view-login input' : '#view-reset input'); if (f) f.focus(); };
    $$('[data-view]').forEach(function (b) { b.addEventListener('click', function (e) { e.preventDefault(); go(b.getAttribute('data-view')); }); });
  }

  /* Daftar (2 langkah) */
  var reg = $('#form-register');
  if (reg) {
    wire(reg);
    var step = 1, s1 = $('#step-1'), s2 = $('#step-2'), st = $$('.stepper .s'), line = $('.stepper .line');
    var setType = function (t) {
      var ent = t === 'enterprise';
      $$('.ent-only').forEach(function (e) { e.hidden = !ent; });
      $$('[data-ent-required]').forEach(function (e) { e.setAttribute('data-v', ent ? 'required' : ''); });
      var r = $('input[name=tipe][value=' + t + ']'); if (r) r.checked = true;
    };
    var qp = qparam('tipe');
    setType(qp === 'enterprise' ? 'enterprise' : 'personal');
    $$('input[name=tipe]').forEach(function (r) { r.addEventListener('change', function () { setType(r.value); }); });
    var goStep = function (n) {
      step = n; s1.hidden = n !== 1; s2.hidden = n !== 2;
      st[0].className = 's ' + (n === 1 ? 'on' : 'done'); st[1].className = 's ' + (n === 2 ? 'on' : '');
      st[0].querySelector('.dot').textContent = n === 1 ? '1' : '✓';
      line.style.setProperty('--p', n === 2 ? 1 : 0);
      var t = n === 1 ? s1 : s2; var h = $('h1,h2', t); if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
    };
    $('#to-2').addEventListener('click', function () { goStep(2); });
    $('#to-1').addEventListener('click', function () { goStep(1); });
    var pw = $('#reg-pw'), meter = $('.strength');
    pw.addEventListener('input', function () {
      var v = pw.value, s = 0;
      if (v.length >= 8) s++; if (/[a-z]/.test(v) && /[A-Z]/.test(v)) s++; if (/\d/.test(v)) s++; if (/[^A-Za-z0-9]/.test(v) || v.length >= 12) s++;
      meter.setAttribute('data-s', v ? s : 0);
      $('#pw-label').textContent = v ? ['', 'Lemah', 'Cukup', 'Baik', 'Kuat'][s] || 'Lemah' : '';
    });
    reg.addEventListener('submit', function (e) {
      e.preventDefault();
      if (step === 1) return goStep(2);
      if (validateAll(s2)) submit(reg, 'register', data(reg));
    });
  }

  /* Kontak */
  var contact = $('#form-contact');
  if (contact) {
    wire(contact);
    var ta = $('textarea', contact), cnt = $('#msg-count');
    ta.addEventListener('input', function () { cnt.textContent = ta.value.length + '/1000'; });
    var tp = qparam('topik'); if (tp) { var sel = $('select', contact); if (sel) sel.value = tp; }
    contact.addEventListener('submit', function (e) {
      e.preventDefault();
      if (validateAll(contact)) submit(contact, 'contact', data(contact), function () { contact.reset(); cnt.textContent = '0/1000'; });
    });
  }
  $$('[data-wa]').forEach(function (a) { a.href = 'https://wa.me/' + CONFIG.whatsapp + '?text=' + encodeURIComponent(a.getAttribute('data-wa')); });

  }

  /* ---- Mulai ---- */
  window.LOGOIPSUM_APP = { shell: initShell, page: initPage, teardown: function () { cleanups.forEach(function (f) { f(); }); cleanups = []; }, closeMenu: function () { closeMenu(); var u = menuBtn && menuBtn.querySelector('use'); if (u) u.setAttribute('href', '#i-menu'); } };
  if (!SPA) { initShell(); initPage(); }
})();
