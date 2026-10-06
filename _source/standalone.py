# -*- coding: utf-8 -*-
"""Merakit seluruh situs menjadi SATU file HTML (CSS, JS, gambar, dan semua halaman di dalamnya).
Navigasi memakai hash (#/blog, #/kontak, dst.), jadi cukup dibuka dengan klik dua kali."""
import os, re, io, json, base64, tempfile, sys
os.environ['OUT'] = tempfile.mkdtemp()          # keluaran multi-file dibuang, yang dipakai hanya PAGES
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B
from PIL import Image

SRC = B.SRC
TARGET = os.environ.get('TARGET', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_build', 'emeterai-standalone.html'))

# ---------- jalankan semua generator halaman ----------
B.home(); B.about(); B.blog_index(); [B.article_page(a) for a in B.ARTICLES]
B.contact(); B.login(); B.register(); B.notfound(); B.legals()

# ---------- gambar -> data URI (PNG dikecilkan jadi WebP) ----------
IMG_DIR = os.path.join(SRC, 'assets/img')
def data_uri(fn):
    p = os.path.join(IMG_DIR, fn)
    if fn.endswith('.png'):
        buf = io.BytesIO(); Image.open(p).save(buf, 'WEBP', quality=88, method=6)
        return 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()
    mime = 'image/webp' if fn.endswith('.webp') else 'image/svg+xml'
    return f'data:{mime};base64,' + base64.b64encode(open(p, 'rb').read()).decode()

USED = set()
def fix_src(m):
    USED.add(m.group(3))
    return f'data-img="{m.group(3)}"'

def fix_href(h, rel):
    if re.match(r'(https?:|mailto:|tel:|#)', h) or h == '': return h
    while h.startswith('../'): h = h[3:]
    anchor = ''
    if '#' in h: h, anchor = h.split('#', 1); anchor = '#' + anchor
    q = ''
    if '?' in h: h, q = h.split('?', 1); q = '?' + q
    route = '/' if h in ('index.html', '') else '/' + re.sub(r'\.html$', '', h)
    return '#' + route + q + anchor

def spa(html_, rel=''):
    html_ = re.sub(r'(src=")((?:\.\./)?assets/img/)([^"]+)(")', fix_src, html_)
    html_ = re.sub(r'href="([^"]*)"', lambda m: 'href="' + fix_href(m.group(1), rel) + '"', html_)
    return html_

# ---------- shell: header + footer ----------
header_html = spa(B.header('', None))
footer_html = spa(B.footer(''))

# ---------- template per halaman ----------
tpls = []
for path, pg in B.PAGES.items():
    route = '/' if path == '' else '/' + re.sub(r'\.html$', '', path)
    body = spa(pg['body'], pg['rel'])
    tpls.append(f'<template data-route="{route}" data-title="{B.esc(pg["title"])}" data-desc="{B.esc(pg["desc"])}" '
                f'data-nav="{pg["active"] or ""}" data-foot="{1 if pg["foot"] else 0}">{body}</template>')

# ---------- aset ----------
css = open(os.path.join(SRC, 'assets/css/styles.css'), encoding='utf-8').read()
js = open(os.path.join(SRC, 'assets/js/app.js'), encoding='utf-8').read()
imgs = {n: data_uri(n) for n in sorted(USED)}
fav = 'data:image/svg+xml;base64,' + base64.b64encode(open(os.path.join(IMG_DIR, 'favicon.svg'), 'rb').read()).decode()

ROUTER = r'''
(function () {
  var APP = window.LOGOIPSUM_APP, IMG = window.LOGOIPSUM_IMG;
  var main = document.getElementById('main'), foot = document.querySelector('.site-footer'), notice = document.querySelector('.notice');
  var descMeta = document.querySelector('meta[name="description"]');
  var current = null, rendered = false;

  function parse() {
    var h = location.hash.slice(1), anchor = '';
    var i = h.indexOf('#'); if (i > -1) { anchor = h.slice(i + 1); h = h.slice(0, i); }
    var q = ''; i = h.indexOf('?'); if (i > -1) { q = h.slice(i + 1); h = h.slice(0, i); }
    if (!h || h.charAt(0) !== '/') h = '/';
    if (h.length > 1) h = h.replace(/\/+$/, '');
    return { route: h, qs: q, anchor: anchor };
  }
  function scrollToAnchor(id) {
    var el = id && document.getElementById(id);
    if (el) { el.scrollIntoView({ block: 'start' }); } else { window.scrollTo({ top: 0, behavior: 'instant' }); }
  }
  function setNav(route) {
    var base = route === '/' ? '/' : '/' + route.split('/')[1];
    Array.prototype.forEach.call(document.querySelectorAll('.nav a, .mobile-panel nav a'), function (a) {
      var t = a.getAttribute('href').slice(1);
      if (t === base) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    });
  }
  function render(p) {
    var tpl = document.querySelector('template[data-route="' + p.route + '"]');
    var is404 = !tpl; if (is404) tpl = document.querySelector('template[data-route="/404"]');
    APP.teardown(); APP.closeMenu();
    main.innerHTML = ''; main.appendChild(tpl.content.cloneNode(true));
    Array.prototype.forEach.call(main.querySelectorAll('img[data-img]'), function (im) { im.src = IMG[im.getAttribute('data-img')]; });
    document.title = tpl.getAttribute('data-title');
    if (descMeta) descMeta.setAttribute('content', tpl.getAttribute('data-desc'));
    var showFoot = tpl.getAttribute('data-foot') === '1'; foot.style.display = showFoot ? '' : 'none'; if (notice) notice.style.display = showFoot ? '' : 'none';
    window.LOGOIPSUM_QS = p.qs ? '?' + p.qs : '';
    setNav(is404 ? '/404' : p.route);
    main.classList.remove('page-enter'); void main.offsetWidth; main.classList.add('page-enter');
    if (rendered) { document.documentElement.classList.add('is-routing'); setTimeout(function () { document.documentElement.classList.remove('is-routing'); }, 520); }
    APP.page(); rendered = true;
    if (window.LOGOIPSUM_NAVSYNC) window.LOGOIPSUM_NAVSYNC(true);
    if (window.LOGOIPSUM_PROG) setTimeout(window.LOGOIPSUM_PROG, 60);
    requestAnimationFrame(function () { scrollToAnchor(p.anchor); });
  }
  function go() {
    var p = parse(), key = p.route + '?' + p.qs;
    if (key === current) { scrollToAnchor(p.anchor); return; }
    current = key; render(p);
  }

  APP.shell();
  window.addEventListener('hashchange', go);
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]'); if (!a || e.defaultPrevented) return;
    var h = a.getAttribute('href');
    if (h === '#') { e.preventDefault(); return; }
    if (h.indexOf('#/') === 0) { if (h === location.hash || (h === '#/' && !location.hash)) { e.preventDefault(); window.scrollTo({ top: 0 }); } return; }
    e.preventDefault();                             /* anchor di dalam halaman (daftar isi, "Lihat caranya", lewati ke konten) */
    var el = document.getElementById(h.slice(1));
    if (el) { el.scrollIntoView({ block: 'start' }); if (h === '#main') el.focus({ preventScroll: true }); }
  });
  go();
})();
'''

html = f'''<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{B.esc(B.PAGES[""]["title"])}</title>
<meta name="description" content="{B.esc(B.PAGES[""]["desc"])}">
<meta name="color-scheme" content="light only">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="{fav}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
<style>
{css}
#main:focus{{outline:0}}
</style>
</head>
<body>
{B.SPRITE}
{B.LOADER}
{header_html}
<main id="main" tabindex="-1"></main>
{footer_html}
{chr(10).join(tpls)}
<script>window.LOGOIPSUM_SPA=true;window.LOGOIPSUM_IMG={json.dumps(imgs)};</script>
<script>
{js}
</script>
<script>{ROUTER}</script>
</body>
</html>
'''
os.makedirs(os.path.dirname(TARGET), exist_ok=True)
open(TARGET, 'w', encoding='utf-8').write(html)
print('ok', TARGET, round(len(html.encode()) / 1024), 'KB', len(tpls), 'halaman', len(imgs), 'gambar')
