# -*- coding: utf-8 -*-
import os, re, json, html, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import ARTICLES, FAQ

OUT = os.environ.get('OUT', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_build'))
SRC = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

# ====== KONFIGURASI MEREK (ganti di sini; semua halaman ikut berubah) ======
BRAND = 'E-Materai'
LEGAL = 'PT Prawathiya Karsa Pradiptha'
BASE = 'https://e-materai.id'          # ganti dengan domain final
PHONE = '+62 812-3456-7890'              # placeholder
PHONE_RAW = '+6281234567890'
EMAIL = 'halo@e-materai.id'             # placeholder
ADDRESS = 'Jl. Transyogie, Cibubur, Kota Bekasi 14123'
HOURS = [('Senin–Jumat', '09.00–18.00'), ('Sabtu', '09.00–21.00')]
SOCIAL = [('facebook', 'Facebook', 'https://www.facebook.com/PT.PrawathiyaKarsaPradiptha'),
          ('instagram', 'Instagram', 'https://www.instagram.com/beyondtechid'),
          ('linkedin', 'LinkedIn', 'https://www.linkedin.com/company/ptprawathiyakarsapradiptha/posts/')]

E = html.escape
def esc(s): return E(s, quote=True)

# ---------- SVG ----------
SPRITE = '''<svg xmlns="http://www.w3.org/2000/svg" style="position:absolute;width:0;height:0;overflow:hidden" aria-hidden="true" focusable="false">
<defs>
<linearGradient id="lg-em" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4C8DFF"/><stop offset="1" stop-color="#1F5BE0"/></linearGradient>
<mask id="mk-perf" maskUnits="userSpaceOnUse" x="0" y="0" width="40" height="40"><rect x="2" y="2" width="36" height="36" rx="4" fill="#fff"/><circle cx="8" cy="2" r="1.7" fill="#000"/><circle cx="8" cy="38" r="1.7" fill="#000"/><circle cx="2" cy="8" r="1.7" fill="#000"/><circle cx="38" cy="8" r="1.7" fill="#000"/><circle cx="14" cy="2" r="1.7" fill="#000"/><circle cx="14" cy="38" r="1.7" fill="#000"/><circle cx="2" cy="14" r="1.7" fill="#000"/><circle cx="38" cy="14" r="1.7" fill="#000"/><circle cx="20" cy="2" r="1.7" fill="#000"/><circle cx="20" cy="38" r="1.7" fill="#000"/><circle cx="2" cy="20" r="1.7" fill="#000"/><circle cx="38" cy="20" r="1.7" fill="#000"/><circle cx="26" cy="2" r="1.7" fill="#000"/><circle cx="26" cy="38" r="1.7" fill="#000"/><circle cx="2" cy="26" r="1.7" fill="#000"/><circle cx="38" cy="26" r="1.7" fill="#000"/><circle cx="32" cy="2" r="1.7" fill="#000"/><circle cx="32" cy="38" r="1.7" fill="#000"/><circle cx="2" cy="32" r="1.7" fill="#000"/><circle cx="38" cy="32" r="1.7" fill="#000"/></mask>
</defs>
<symbol id="logo-mark" viewBox="0 0 40 40"><rect x="2" y="2" width="36" height="36" fill="url(#lg-em)" mask="url(#mk-perf)"/><rect x="7" y="7" width="26" height="26" rx="2.5" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="1" stroke-dasharray="2 2"/><path d="M12.4 19.6h12.6a6.5 6.5 0 10-2 4.8" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="31.2" cy="31.2" r="5" fill="#E4486F" stroke="#fff" stroke-width="1.5"/><path d="M29 31.3l1.6 1.6 2.9-3.2" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></symbol>
<symbol id="i-arrow-right" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></symbol>
<symbol id="i-arrow-up" viewBox="0 0 24 24"><path d="M12 19V5M6 11l6-6 6 6"/></symbol>
<symbol id="i-arrow-left" viewBox="0 0 24 24"><path d="M19 12H5M11 6l-6 6 6 6"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7"/></symbol>
<symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 4.5-3.2 8-8 9-4.8-1-8-4.5-8-9V6l8-3z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></symbol>
<symbol id="i-file" viewBox="0 0 24 24"><path d="M6 3h8l5 5v13H6z"/><path d="M14 3v5h5M9.5 13h6M9.5 17h6"/></symbol>
<symbol id="i-upload" viewBox="0 0 24 24"><path d="M12 16V4M7 9l5-5 5 5M4 16v4h16v-4"/></symbol>
<symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></symbol>
<symbol id="i-headset" viewBox="0 0 24 24"><path d="M4 13a8 8 0 0116 0M4 13v3a2 2 0 002 2h1v-5H4M20 13v3a2 2 0 01-2 2h-1v-5h3M17 18c0 2-2 3-5 3"/></symbol>
<symbol id="i-lock" viewBox="0 0 24 24"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 018 0v3"/></symbol>
<symbol id="i-chart" viewBox="0 0 24 24"><path d="M4 20V4M4 20h16M8 16v-5M12 16V8M16 16v-3"/></symbol>
<symbol id="i-user" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0116 0"/></symbol>
<symbol id="i-building" viewBox="0 0 24 24"><path d="M5 21V4a1 1 0 011-1h12a1 1 0 011 1v17M3 21h18M9 8h2M13 8h2M9 12h2M13 12h2M10 21v-4h4v4"/></symbol>
<symbol id="i-moon" viewBox="0 0 24 24"><path d="M20 14.5A8 8 0 019.5 4a8 8 0 1010.5 10.5z"/></symbol>
<symbol id="i-sun" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></symbol>
<symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></symbol>
<symbol id="i-x" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></symbol>
<symbol id="i-eye" viewBox="0 0 24 24"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></symbol>
<symbol id="i-eye-off" viewBox="0 0 24 24"><path d="M3 3l18 18M10.6 6.1A9.7 9.7 0 0112 6c6.5 0 10 6 10 6a17 17 0 01-3.2 3.9M6.6 6.7A17 17 0 002 12s3.5 7 10 7c1.6 0 3-.4 4.3-1M9.9 9.9a3 3 0 004.2 4.2"/></symbol>
<symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></symbol>
<symbol id="i-mail" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></symbol>
<symbol id="i-phone" viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21s7-6 7-12a7 7 0 10-14 0c0 6 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/></symbol>
<symbol id="i-link" viewBox="0 0 24 24"><path d="M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1"/></symbol>
<symbol id="i-chevron" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></symbol>
<symbol id="i-stamp" viewBox="0 0 24 24"><path d="M5 21h14M6 17h12v-3a4 4 0 00-3-3.9V8a3 3 0 10-6 0v3.1A4 4 0 006 14z"/></symbol>
<symbol id="i-wallet" viewBox="0 0 24 24"><path d="M3 7a2 2 0 012-2h13v4M3 7v10a2 2 0 002 2h15V9H5a2 2 0 01-2-2zM16 14h.01"/></symbol>
<symbol id="i-info" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/></symbol>
<symbol id="i-alert" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v6M12 16.5h.01"/></symbol>
<symbol id="i-briefcase" viewBox="0 0 24 24"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a1 1 0 011-1h4a1 1 0 011 1v2"/></symbol>
<symbol id="i-download" viewBox="0 0 24 24"><path d="M12 4v12M7 11l5 5 5-5M4 20h16"/></symbol>
<symbol id="i-chat" viewBox="0 0 24 24"><path d="M21 12a8 8 0 01-11.7 7L4 20l1.1-4.2A8 8 0 1121 12z"/></symbol>
<symbol id="i-gavel" viewBox="0 0 24 24"><path d="M14 4l6 6M12 6l6 6-4 4-6-6zM9 13l-5 5M3 21h8"/></symbol>
<symbol id="i-cap" viewBox="0 0 24 24"><path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5M22 9v6"/></symbol>
<symbol id="i-store" viewBox="0 0 24 24"><path d="M4 10v10h16V10M3 6l2-3h14l2 3v2a3 3 0 01-6 0 3 3 0 01-6 0 3 3 0 01-6 0z"/><path d="M10 20v-5h4v5"/></symbol>
<symbol id="i-qr" viewBox="0 0 24 24"><rect x="4" y="4" width="6" height="6" rx="1"/><rect x="14" y="4" width="6" height="6" rx="1"/><rect x="4" y="14" width="6" height="6" rx="1"/><path d="M14 14h2v2h-2zM18 14h2M14 18v2M17 17h3v3h-3z"/></symbol>
<symbol id="i-facebook" viewBox="0 0 24 24"><path d="M14 8h2V5h-2.5C11.5 5 10 6.5 10 8.5V11H8v3h2v6h3v-6h2.2l.5-3H13V8.7c0-.4.2-.7 1-.7z" class="icon-fill"/></symbol>
<symbol id="i-instagram" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="5"/><circle cx="12" cy="12" r="3.8"/><path d="M16.8 7.2h.01"/></symbol>
<symbol id="i-linkedin" viewBox="0 0 24 24"><path d="M7 10v8M7 6.5v.01M11 18v-8M11 13c0-2 1.3-3 3-3s3 1 3 3v5"/></symbol>
<symbol id="i-youtube" viewBox="0 0 24 24"><rect x="3" y="6" width="18" height="12" rx="4"/><path d="M10.5 9.5v5l4.2-2.5z"/></symbol>
<symbol id="i-x-social" viewBox="0 0 24 24"><path d="M5 5l14 14M19 5L5 19"/></symbol>
</svg>'''

def ic(name, cls='icon', extra=''):
    return f'<svg class="{cls}" aria-hidden="true" {extra}><use href="#i-{name}"/></svg>'

LOGO_MARK = '<svg class="mark" viewBox="0 0 40 40" aria-hidden="true"><use href="#logo-mark"/></svg>'

def brand(rel):
    return f'<a class="brand" href="{rel}index.html" aria-label="{BRAND}, ke beranda">{LOGO_MARK}<span class="wm"><b>E-</b>Materai</span></a>'

NAV = [('Cara pakai', 'index.html#cara', 'cara'), ('Cek dokumen', 'index.html#cek', 'cek'), ('Tentang', 'tentang.html', 'about'), ('Blog', 'blog.html', 'blog'), ('Kontak', 'kontak.html', 'contact')]

NOTICE = 'Mau daftar CPNS, PPPK, atau BUMN? Siapkan e-Meterai untuk surat lamaran sebelum mendekati batas waktu.'

def notice(rel):
    return f'<div class="notice"><div class="wrap"><span class="dot" aria-hidden="true"></span><span class="long">{NOTICE}</span><span class="short">Daftar CPNS atau PPPK? Siapkan e-Meterai dari sekarang.</span><a href="{rel}blog/cara-beli-emeterai-untuk-cpns-dan-pppk.html">Lihat panduannya</a></div></div>'

def header(rel, active, show_notice=False):
    links = ''.join(f'<a href="{rel}{h}"{" aria-current=\"page\"" if k==active else ""}>{t}</a>' for t, h, k in NAV)
    mlinks = ''.join(f'<a href="{rel}{h}"{" aria-current=\"page\"" if k==active else ""}>{t}{ic("arrow-right")}</a>' for t, h, k in NAV)
    return f'''<a class="skip" href="#main">Lewati ke konten</a>
{notice(rel) if show_notice else ""}
<header class="site-header"><div class="wrap header-in">
{brand(rel)}
<nav class="nav" aria-label="Navigasi utama">{links}</nav>
<div class="header-actions">
<a class="btn btn-ghost btn-sm" href="{rel}masuk.html">Masuk</a>
<a class="btn btn-primary btn-sm" href="{rel}daftar.html">Beli e-Meterai</a>
<button class="icon-btn menu-btn" type="button" aria-expanded="false" aria-controls="mobile-panel" aria-label="Buka menu">{ic("menu")}</button>
</div></div></header>
<div class="mobile-panel" id="mobile-panel"><nav aria-label="Navigasi seluler"><a href="{rel}index.html"{" aria-current=\"page\"" if active=="home" else ""}>Beranda{ic("arrow-right")}</a>{mlinks}</nav>
<div class="btns"><a class="btn btn-primary btn-lg" href="{rel}daftar.html">Beli e-Meterai</a><a class="btn btn-quiet btn-lg" href="{rel}masuk.html">Masuk</a></div></div>'''

def footer(rel):
    soc = ''.join(f'<a href="{u}" target="_blank" rel="noopener noreferrer" aria-label="{n}">{ic(k)}</a>' for k, n, u in SOCIAL)
    return f'''<footer class="site-footer"><div class="wrap">
<div class="foot-grid">
<div class="foot-about">{brand(rel)}<p>Beli, bubuhkan ke PDF, dan unduh dokumen bermeterai tanpa antre di kantor pos.</p>
<ul class="foot-contact"><li>{ic("mail")}<a href="mailto:{EMAIL}">{EMAIL}</a></li><li>{ic("pin")}<span>{ADDRESS}</span></li></ul>
<div class="socials">{soc}</div></div>
<div><h2>Produk</h2><ul><li><a href="{rel}daftar.html">Beli e-Meterai</a></li><li><a href="{rel}index.html#cek">Cek dokumen</a></li><li><a href="{rel}index.html#cara">Cara pakai</a></li><li><a href="{rel}kontak.html?topik=penawaran">Untuk perusahaan</a></li></ul></div>
<div><h2>Bantuan</h2><ul><li><a href="{rel}index.html#faq">Pertanyaan umum</a></li><li><a href="{rel}tentang.html">Tentang kami</a></li><li><a href="{rel}blog.html">Blog &amp; panduan</a></li><li><a href="{rel}kontak.html">Kontak</a></li></ul></div>
</div>
<div class="foot-bottom"><span>© <span data-year>2026</span> {LEGAL}. Hak cipta dilindungi.</span>
<nav aria-label="Legal"><a href="{rel}kebijakan-privasi.html">Kebijakan Privasi</a><a href="{rel}syarat-ketentuan.html">Syarat &amp; Ketentuan</a></nav></div>
</div></footer>'''

def head(title, desc, path, rel='', og='assets/img/og.png', ld=None, noindex=False, typ='website'):
    url = f'{BASE}/{path}' if path else BASE + '/'
    ldt = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False, separators=(",", ":"))}</script>\n' for x in (ld or []))
    robots = '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    return f'''<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<link rel="canonical" href="{url}">
<meta name="color-scheme" content="light only">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="{typ}"><meta property="og:site_name" content="{BRAND}"><meta property="og:locale" content="id_ID">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/{og}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{BASE}/{og}">
<link rel="icon" href="{rel}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="{rel}assets/css/styles.css">
{ldt}</head>'''

PAGES = {}  # dipakai standalone.py untuk merakit versi satu file

LOADER = '<div class="loader" aria-hidden="true"><div class="ld"><svg class="ld-ring" viewBox="0 0 60 60"><circle cx="30" cy="30" r="26"/></svg><svg class="ld-mark" viewBox="0 0 40 40"><use href="#logo-mark"/></svg></div><span class="ld-txt"><b>E-</b>Materai</span></div>'

def page(title, desc, path, active, body, rel='', ld=None, noindex=False, typ='website', og='assets/img/og.png', chrome=True, foot=True):
    PAGES[path] = dict(title=title, desc=desc, active=active, body=body, rel=rel, foot=foot)
    h = head(title, desc, path, rel, og, ld, noindex, typ)
    top = header(rel, active) if chrome else ''
    bot = footer(rel) if (chrome and foot) else ''
    return f'''{h}
<body>
{SPRITE}
{LOADER}
{top}
<main id="main">
{body}
</main>
{bot}
<script src="{rel}assets/js/app.js" defer></script>
</body>
</html>
'''

def write(path, content):
    p = os.path.join(OUT, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f: f.write(content)

ORG = {"@context": "https://schema.org", "@type": "Organization", "name": BRAND, "legalName": LEGAL, "url": BASE + "/",
       "logo": f"{BASE}/assets/img/logo-512.png",
       "address": {"@type": "PostalAddress", "streetAddress": "Jl. Transyogie, Cibubur", "addressLocality": "Kota Bekasi", "postalCode": "14123", "addressCountry": "ID"},
       "contactPoint": {"@type": "ContactPoint", "telephone": PHONE_RAW, "email": EMAIL, "contactType": "customer support", "availableLanguage": "id"},
       "sameAs": [u for _, _, u in SOCIAL]}
WEBSITE = {"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": BASE + "/", "inLanguage": "id-ID"}

def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": f"{BASE}/{p}"} for i, (n, p) in enumerate(items)]}

def faq_html():
    out = []
    for q, a in FAQ:
        out.append(f'<details><summary>{esc(q)}{ic("chevron")}</summary><div class="ans"><p>{esc(a)}</p></div></details>')
    return '\n'.join(out)

def post_card(a, rel='', feature=False):
    link = f'{rel}blog/{a["slug"]}.html'
    txt = (a['title'] + ' ' + a['excerpt'] + ' ' + a['cat']).lower()
    return f'''<a class="post reveal" href="{link}" data-cat="{a['cat'].lower().replace(' ','-')}" data-text="{esc(txt)}">
<div class="post-img"><img src="{rel}assets/img/{a['img']}" alt="{esc(a['alt'])}" width="699" height="389" loading="lazy" decoding="async"></div>
<div class="post-body"><div class="post-meta"><span class="tag">{a['cat']}</span><span>{a['read']} menit baca</span></div>
<h3>{esc(a['title'])}</h3><p>{esc(a['excerpt'])}</p><span class="link-arrow">Baca artikel {ic("arrow-right")}</span></div></a>'''

# ======================================================================
# BERANDA
# ======================================================================
def stamp(cls=''):
    return f'''<div class="emet {cls}" aria-hidden="true"><div class="perf"><div class="emet-in"><small>METERAI<br>ELEKTRONIK</small><i class="qr"></i><b>SAH<span>DOKUMEN ELEKTRONIK</span></b></div></div></div>'''

def home():
    title = 'Beli e-Meterai Resmi, Langsung Tempel ke PDF | E-Materai'
    desc = 'Beli e-Meterai resmi dari Peruri dan bubuhkan langsung ke PDF dalam hitungan menit, tanpa cetak dan tanpa antre. Sah menurut UU Bea Meterai. Untuk CPNS, kontrak, dan bisnis.'
    latest = ''.join(post_card(a) for a in [ARTICLES[3], ARTICLES[4], ARTICLES[7]])
    I = lambda n, s=18: ic(n, 'icon', f'style="width:{s}px;height:{s}px"')

    def stamp(cls=''):
        return f'''<div class="emet {cls}" aria-hidden="true"><div class="perf"><div class="emet-in"><small>METERAI<br>ELEKTRONIK</small><i class="qr"></i><b>SAH<span>DOKUMEN ELEKTRONIK</span></b></div></div></div>'''

    sig = '<svg viewBox="0 0 120 46" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 32c8-14 14-24 18-22s-6 26-2 26 10-22 16-22-2 20 3 20 8-14 12-14 0 12 4 12 10-10 16-14 4 8 10 6 12-6 18-8"/></svg>'

    uc = [
        ('cpns', 'cap', 'Lamaran CPNS &amp; kerja', 'blog-beli-emeterai-cpns.webp', 'Peserta seleksi CPNS duduk berbaris di ruang ujian',
         'Berkas lamaran bermeterai, siap diunggah ke portal seleksi',
         'Surat lamaran dan surat pernyataan untuk CPNS, PPPK, BUMN, maupun perusahaan swasta sering wajib bermeterai. Bubuhkan e-Meterai langsung ke PDF, lalu unggah. Tidak perlu printer atau scanner.',
         ['Surat lamaran', 'Surat pernyataan', 'Surat keterangan'],
         'Bubuhkan meterai beberapa hari sebelum batas akhir. Menjelang penutupan, portal seleksi dan pembelian meterai biasanya ramai.',
         ('daftar.html?tipe=personal', 'Beli untuk lamaran'), ('blog/cara-beli-emeterai-untuk-cpns-dan-pppk.html', 'Panduan e-Meterai untuk CPNS')),
        ('kontrak', 'file', 'Kontrak &amp; perjanjian', 'blog-letak-emeterai.webp', 'Contoh dokumen dengan e-Meterai di samping tanda tangan',
         'Kontrak ditandatangani hari ini, meterainya juga hari ini',
         'Perjanjian sewa, kerja sama, jual beli, atau perjanjian kerja bisa dimeteraikan tanpa harus bertemu. PDF bermeterai tinggal dikirim lewat email atau chat.',
         ['Perjanjian sewa', 'Perjanjian kerja', 'Surat kerja sama', 'Surat kuasa'],
         'Letakkan e-Meterai di dekat tanda tangan supaya jelas bagian mana yang dilunasi Bea Meterainya.',
         ('daftar.html?tipe=personal', 'Beli e-Meterai'), ('blog/letak-emeterai-jauh-dari-tanda-tangan-apakah-valid.html', 'Aturan letak e-Meterai')),
        ('umkm', 'store', 'UMKM &amp; freelancer', 'blog-e-meterai-solusi-praktis.webp', 'Mengurus dokumen lewat ponsel di depan laptop',
         'Kuitansi bernilai besar tetap rapi, tanpa stok meterai di laci',
         'Kuitansi dan tanda terima bernilai besar wajib bermeterai. Beli saat dibutuhkan saja, tidak perlu menyimpan meterai tempel yang bisa terlipat, sobek, atau hilang.',
         ['Kuitansi bernilai besar', 'Tanda terima pembayaran', 'Perjanjian kerja sama'],
         'Tidak semua kuitansi wajib bermeterai. Pakai fitur Cek dokumen di bawah untuk memastikan.',
         ('daftar.html?tipe=personal', 'Beli e-Meterai'), ('blog/dokumen-bebas-bea-meterai.html', 'Dokumen yang bebas Bea Meterai')),
        ('perusahaan', 'building', 'Perusahaan', 'blog-ingkari-perjanjian.webp', 'Lembaran meterai dalam jumlah banyak di atas meja',
         'Puluhan sampai ratusan dokumen, satu dasbor untuk semuanya',
         'Untuk tim HR, legal, dan keuangan yang rutin memeterai kontrak karyawan, perjanjian vendor, atau dokumen transaksi. Pemakaian dan riwayat pembubuhan terlihat dari satu akun perusahaan.',
         ['Kontrak karyawan', 'Perjanjian vendor', 'Dokumen transaksi'],
         '',
         ('kontak.html?topik=penawaran', 'Minta penawaran'), ('daftar.html?tipe=enterprise', 'Daftar akun perusahaan')),
    ]
    tabs = ''.join(f'<button class="uc-tab" role="tab" type="button" id="uct-{k}" aria-controls="ucp-{k}" aria-selected="{"true" if i==0 else "false"}" tabindex="{0 if i==0 else -1}">{I(icn)}{lbl}</button>' for i, (k, icn, lbl, *_r) in enumerate(uc))
    panels = ''
    for i, (k, icn, lbl, img, alt, h, p, docs, tip, a1, a2) in enumerate(uc):
        dl = ''.join(f'<li>{I("check",16)}{d}</li>' for d in docs)
        tp = f'<p class="uc-tip">{I("info")}<span>{tip}</span></p>' if tip else ''
        btn = 'btn-primary' if i < 3 else 'btn-primary'
        panels += f'''<div class="uc-panel" role="tabpanel" id="ucp-{k}" aria-labelledby="uct-{k}"{"" if i==0 else " hidden"}>
<div class="uc-img"><img src="assets/img/{img}" alt="{alt}" width="699" height="390" loading="lazy" decoding="async"></div>
<div class="uc-body"><h3>{h}</h3><p>{p}</p><ul class="uc-docs" aria-label="Contoh dokumen">{dl}</ul>{tp}
<div class="uc-actions"><a class="btn {btn}" href="{a1[0]}">{a1[1]} {ic("arrow-right","icon icon-go")}</a><a class="link-arrow" href="{a2[0]}">{a2[1]} {ic("arrow-right")}</a></div></div></div>'''

    body = f'''
<section class="hero" aria-labelledby="h1"><div class="wrap hero-grid">
<div class="hero-copy">
<span class="pill"><i>RESMI</i>Diterbitkan Peruri</span>
<h1 id="h1" class="h-display">Beli e-Meterai resmi, tempel ke PDF <span class="hl">dalam hitungan menit</span></h1>
<p class="lead">Tidak perlu mencari meterai tempel, mencetak, lalu memindai ulang. Unggah dokumen, geser meterai ke tempatnya, masukkan PIN, selesai. Bisa dari ponsel atau laptop.</p>
<div class="hero-cta"><a class="btn btn-primary btn-lg" href="daftar.html">Beli e-Meterai {ic("arrow-right","icon icon-go")}</a><a class="btn btn-quiet btn-lg" href="#cara">Coba simulasinya</a></div>
<ol class="mini-steps" aria-label="Tiga langkah"><li><span>1</span>Unggah PDF</li><li><span>2</span>Letakkan meterai</li><li><span>3</span>Masukkan PIN</li></ol>
<ul class="ticks"><li>{ic("check")}Sah menurut UU Bea Meterai</li><li>{ic("check")}Nomor seri unik</li><li>{ic("check")}Dibantu via WhatsApp</li></ul>
</div>
<div class="hero-visual" role="img" aria-label="Ilustrasi surat pernyataan dalam format PDF yang sudah dibubuhi e-Meterai di dekat tanda tangan">
<div class="sheet" aria-hidden="true">
<div class="sheet-head"><b>SURAT PERNYATAAN</b><span>PDF</span></div>
<div class="sheet-lines"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
<div class="sheet-lines" style="align-content:center"><i></i><i></i><i></i><i></i><i></i></div>
<div class="sheet-sign"><div class="who"><span class="d" style="border:0;padding:0;margin:0;font-weight:400;color:var(--tinta-3)">Bekasi, 2 Oktober 2026</span>{sig}<span>Rina Putri</span></div></div>
{stamp()}
</div>
<div class="float float-a" aria-hidden="true"><span class="ico">{ic("check")}</span><div><b>e-Meterai terbubuh</b><span>Surat-Pernyataan.pdf</span></div></div>
<div class="float float-b" aria-hidden="true"><span class="ico">{ic("qr")}</span><div><b>Nomor seri unik</b><span>Bisa dicek keasliannya</span></div></div>
<img class="hero-mascot" src="assets/img/mascot.png" alt="" width="397" height="1126">
</div>
</div></section>

<section class="legalbar" aria-label="Dasar hukum dan penerbit e-Meterai"><div class="wrap">
<p class="lb-t">Dasar hukum &amp; penerbit</p>
<div class="lb">{ic("stamp")}<div><b>Diterbitkan Peruri</b><span>Pencetak dan penerbit meterai resmi</span></div></div>
<div class="lb">{ic("gavel")}<div><b>UU No. 10 Tahun 2020</b><span>Tentang Bea Meterai</span></div></div>
<div class="lb">{ic("file")}<div><b>PP No. 86 Tahun 2021</b><span>Pengadaan dan penjualan meterai</span></div></div>
<div class="lb">{ic("shield")}<div><b>UU ITE Pasal 5</b><span>Dokumen elektronik sah sebagai bukti</span></div></div>
</div></section>

<section class="section" id="apa-itu" aria-labelledby="t-vs"><div class="wrap">
<div class="section-head"><span class="eyebrow">Apa itu e-Meterai</span><h2 id="t-vs" class="h-section">Satu meterai seharusnya tidak menghabiskan setengah hari</h2>
<p class="lead">e-Meterai adalah meterai dalam bentuk elektronik yang dibubuhkan langsung ke dokumen PDF. Fungsinya sama dengan meterai tempel, yaitu melunasi Bea Meterai. Bedanya ada di cara memakainya.</p></div>
<div class="versus">
<div class="vs-card vs-old reveal"><div class="vs-label"><b>Meterai tempel</b><span class="badge badge-grey">Cara lama</span></div>
<ol class="vs-list"><li>Cari meterai ke kantor pos atau toko terdekat</li><li>Cetak dokumen yang sudah jadi</li><li>Tempel meterai, lalu tanda tangan di atasnya</li><li>Pindai ulang, sering buram atau ukurannya terlalu besar</li><li>Kirim hasil pindaian ke penerima</li></ol>
<p class="vs-foot">{ic("clock")}Butuh keluar rumah, printer, dan scanner</p></div>
<div class="vs-card vs-new reveal" style="--i:1"><div class="vs-label"><b>Lewat {BRAND}</b><span class="badge badge-indigo">Cara baru</span></div>
<ol class="vs-list"><li><span><b>Unggah PDF</b> dari ponsel atau laptop</span></li><li><span><b>Geser meterai</b> ke dekat tanda tangan</span></li><li><span><b>Masukkan PIN</b>, lalu unduh dokumen bermeterai</span></li></ol>
<div class="vs-chips"><span>{I("x",14)}Tanpa printer</span><span>{I("x",14)}Tanpa scanner</span><span>{I("x",14)}Tanpa antre</span></div>
<p class="vs-foot">{ic("check")}Selesai dalam hitungan menit, dari mana saja</p>
<a class="link-arrow" href="#cara">Lihat simulasinya {ic("arrow-right")}</a></div>
</div></div></section>

<section class="section soft" id="kebutuhan" aria-labelledby="t-uc"><div class="wrap">
<div class="section-head"><span class="eyebrow">Untuk keperluan apa</span><h2 id="t-uc" class="h-section">Dipakai untuk dokumen yang paling sering butuh meterai</h2></div>
<div class="uc-tabs" role="tablist" aria-label="Pilih keperluan">{tabs}</div>
{panels}
<p class="note-line">Ragu dokumen Anda perlu meterai atau tidak? <a href="blog/kenali-emeterai-fungsi-dan-cara-mendapatkannya.html">Cek daftar dokumen yang dikenai Bea Meterai</a>.</p>
</div></section>

<section class="section" id="cara" aria-labelledby="t-cara"><div class="wrap how">
<div>
<div class="section-head" style="margin-bottom:28px"><span class="eyebrow">Cara pakai</span><h2 id="t-cara" class="h-section">Tiga langkah. Silakan coba simulasinya.</h2><p class="lead">Begini alurnya di akun {BRAND}. Klik tiap langkah, lalu coba geser meterainya di panel.</p></div>
<div class="step-list" role="tablist" aria-label="Langkah membubuhkan e-Meterai" aria-orientation="vertical">
<button class="step-tab" role="tab" id="tab-1" aria-controls="panel-1" aria-selected="true" type="button"><span class="step-n">1</span><span class="step-body"><h3>Unggah dokumen PDF</h3><span class="more">Masuk ke akun, buka menu Upload, isi detail dokumen, lalu pilih berkas PDF Anda.</span></span><span class="bar" aria-hidden="true"><i></i></span></button>
<button class="step-tab" role="tab" id="tab-2" aria-controls="panel-2" aria-selected="false" type="button"><span class="step-n">2</span><span class="step-body"><h3>Letakkan e-Meterai</h3><span class="more">Geser meterai ke posisi yang Anda mau, biasanya di dekat tanda tangan.</span></span><span class="bar" aria-hidden="true"><i></i></span></button>
<button class="step-tab" role="tab" id="tab-3" aria-controls="panel-3" aria-selected="false" type="button"><span class="step-n">3</span><span class="step-body"><h3>Masukkan PIN, lalu unduh</h3><span class="more">PIN mengonfirmasi pembubuhan. Dokumen bermeterai langsung bisa diunduh dan dikirim.</span></span><span class="bar" aria-hidden="true"><i></i></span></button>
</div>
<div class="how-cta"><a class="btn btn-primary btn-lg" href="daftar.html">Beli e-Meterai {ic("arrow-right","icon icon-go")}</a><span class="muted" style="font-size:.9375rem">Sudah punya akun? <a href="masuk.html">Masuk</a></span></div>
</div>
<div class="step-stage" aria-live="polite">
<div class="stage-panel" role="tabpanel" id="panel-1" aria-labelledby="tab-1"><div class="mock" role="img" aria-label="Contoh tampilan unggah dokumen PDF"><h4>Upload dokumen <small>Langkah 1 dari 3</small></h4>
<div class="drop">{ic("upload")}<b>Tarik PDF ke sini</b><span style="font-size:.8125rem">atau pilih berkas dari perangkat</span></div>
<div class="filerow"><span class="f">PDF</span><div><b>Surat-Pernyataan.pdf</b><span>248 KB · terunggah</span></div><span class="ok">{ic("check")}</span></div>
<div class="prog"><i></i></div><div class="mbtn">Lanjut atur posisi</div></div></div>
<div class="stage-panel" role="tabpanel" id="panel-2" aria-labelledby="tab-2"><div class="mock"><h4>Atur posisi e-Meterai <small>Langkah 2 dari 3</small></h4><div class="docpage" aria-label="Halaman dokumen contoh"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><div class="sign">Rina Putri</div><div class="drag-stamp" tabindex="0" role="button" aria-label="Contoh e-Meterai. Geser dengan mouse, jari, atau tombol panah"><div class="perf"><span>e-MET<br>SAH</span></div></div></div><p class="drag-hint">{ic("info")}Coba geser meterainya ke dekat tanda tangan.</p></div></div>
<div class="stage-panel" role="tabpanel" id="panel-3" aria-labelledby="tab-3"><div class="mock"><h4>Masukkan PIN <small>Langkah 3 dari 3</small></h4><div class="pin" aria-hidden="true"><i class="f">•</i><i class="f">•</i><i class="f">•</i><i class="f">•</i><i class="f">•</i><i class="f">•</i></div><div class="done-note">{ic("check")}e-Meterai berhasil dibubuhkan</div><div class="mbtn">Unduh dokumen</div></div></div>
</div>
</div></section>

<section class="section soft" id="cek" aria-labelledby="t-cek"><div class="wrap checker">
<div class="prose-block">
<span class="eyebrow">Cek dokumen</span><h2 id="t-cek" class="h-section">Dokumen Anda perlu e-Meterai atau tidak?</h2>
<p class="lead">Pilih jenis dokumennya, jawabannya langsung muncul. Tidak perlu menebak, tidak perlu membeli yang tidak dibutuhkan.</p>
<ul class="pc-list"><li>{ic("check")}Berdasarkan UU No. 10 Tahun 2020 tentang Bea Meterai</li><li>{ic("check")}Satu e-Meterai untuk satu dokumen</li><li>{ic("check")}Ragu? Tanyakan ke tim kami lewat WhatsApp</li></ul>
</div>
<div class="ck-card reveal" id="checker">
<p class="ck-q" id="ck-q1">Dokumen apa yang mau Anda meteraikan?</p>
<div class="ck-opts" role="group" aria-labelledby="ck-q1">
<button type="button" class="ck-opt" data-doc="pernyataan">{I("file")}Surat pernyataan</button>
<button type="button" class="ck-opt" data-doc="lamaran">{I("cap")}Lamaran CPNS / kerja</button>
<button type="button" class="ck-opt" data-doc="perjanjian">{I("briefcase")}Perjanjian / kontrak</button>
<button type="button" class="ck-opt" data-doc="kuasa">{I("user")}Surat kuasa</button>
<button type="button" class="ck-opt" data-doc="kuitansi">{I("wallet")}Kuitansi / tanda terima</button>
<button type="button" class="ck-opt" data-doc="akta">{I("gavel")}Akta notaris / PPAT</button>
<button type="button" class="ck-opt" data-doc="ijazah">{I("cap")}Ijazah</button>
<button type="button" class="ck-opt" data-doc="gaji">{I("chart")}Slip / tanda terima gaji</button>
</div>
<div class="ck-result" aria-live="polite" hidden><span class="badge"></span><b></b><p></p><div class="ck-acts"></div></div>
<p class="ck-empty">{I("info")}Pilih salah satu untuk melihat hasilnya.</p>
<div class="ck-links" hidden><a class="btn btn-primary" data-k="beli" href="daftar.html?tipe=personal">Beli e-Meterai {ic("arrow-right","icon icon-go")}</a><a class="link-arrow" data-k="cpns" href="blog/cara-beli-emeterai-untuk-cpns-dan-pppk.html">Panduan untuk CPNS {ic("arrow-right")}</a><a class="link-arrow" data-k="letak" href="blog/letak-emeterai-jauh-dari-tanda-tangan-apakah-valid.html">Aturan letak e-Meterai {ic("arrow-right")}</a><a class="link-arrow" data-k="bebas" href="blog/dokumen-bebas-bea-meterai.html">Dokumen yang bebas Bea Meterai {ic("arrow-right")}</a><a class="btn btn-quiet" data-k="tanya" href="kontak.html">Tanya tim kami {ic("arrow-right","icon icon-go")}</a></div>
<p class="fine">Ringkasan umum, bukan nasihat hukum atau pajak. Untuk kasus khusus, cek aturan terbaru.</p>
</div>
</div></section>

<section class="section" id="cara-beli" aria-labelledby="t-beli"><div class="wrap">
<div class="section-head center"><span class="eyebrow">Cara beli</span><h2 id="t-beli" class="h-section">Pilih sesuai kebutuhan Anda</h2><p class="lead">Untuk satu dokumen penting hari ini, atau ratusan kontrak tiap bulan.</p></div>
<div class="pricing">
<div class="price-card pc-main reveal">
<div class="pc-top"><span class="pc-ico pc-ico-b">{ic("user")}</span><span class="badge badge-ok">Paling praktis</span></div>
<div><h3 class="h-card" style="font-size:1.5rem">Perorangan</h3><p class="muted" style="margin-top:6px">Untuk lamaran kerja, kontrak sewa, surat pernyataan, dan dokumen pribadi.</p></div>
<ul class="pc-list"><li>{ic("check")}Beli satuan, sesuai jumlah dokumen</li><li>{ic("check")}Tidak ada paket yang wajib dibeli</li><li>{ic("check")}Langsung dibubuhkan ke PDF dari ponsel atau laptop</li><li>{ic("check")}Rincian pembayaran terlihat sebelum Anda membayar</li></ul>
<a class="btn btn-primary btn-lg btn-block" href="daftar.html?tipe=personal">Beli e-Meterai {ic("arrow-right","icon icon-go")}</a>
</div>
<div class="price-card pc-ent reveal" style="--i:1">
<div class="pc-top"><span class="pc-ico">{ic("building")}</span><span class="badge badge-indigo">Volume besar</span></div>
<div><h3 class="h-card" style="font-size:1.5rem">Perusahaan</h3><p class="muted" style="margin-top:6px">Untuk tim HR, legal, dan keuangan yang rutin memeterai dokumen.</p></div>
<ul class="pc-list"><li>{ic("check")}Penawaran disesuaikan dengan kebutuhan</li><li>{ic("check")}Pemakaian dan riwayat terpantau dari dasbor</li><li>{ic("check")}Satu akun untuk kontrak, perjanjian kerja, dan dokumen transaksi</li><li>{ic("check")}Tim kami bantu menghitung kebutuhan Anda</li></ul>
<a class="btn btn-quiet btn-lg btn-block" href="kontak.html?topik=penawaran">Minta penawaran {ic("arrow-right","icon icon-go")}</a>
</div>
</div></div></section>

<section class="section" id="kenapa" aria-labelledby="t-why"><div class="wrap why">
<div class="why-visual reveal" aria-hidden="true">
{stamp()}
<div class="check-card"><b>Cek keaslian</b><code>Nomor seri: 0A7F 9C2E 51BD 7730</code><span class="badge badge-ok">{I("check",14)}Terverifikasi</span><span class="muted" style="font-size:.6875rem">Contoh tampilan</span></div>
<img src="assets/img/mascot.png" alt="" width="397" height="1126" loading="lazy">
</div>
<div>
<div class="section-head" style="margin-bottom:8px"><span class="eyebrow">Kenapa {BRAND}</span><h2 id="t-why" class="h-section">Dokumen penting tidak boleh gagal hanya karena meterainya</h2></div>
<ul class="why-list">
<li class="reveal"><span class="why-ico">{ic("shield")}</span><div><h3>Resmi dari Peruri, bukan dari sumber tak jelas</h3><p>e-Meterai yang kami jual diterbitkan Peruri dan disalurkan lewat jalur resmi. Meterai dari penjual tidak resmi berisiko palsu, dan dokumen bisa ditolak saat diperiksa.</p></div></li>
<li class="reveal" style="--i:1"><span class="why-ico">{ic("qr")}</span><div><h3>Setiap meterai punya nomor seri unik</h3><p>Nomor seri inilah yang membuat e-Meterai bisa dicek keasliannya, termasuk oleh pihak yang menerima dokumen Anda.</p></div></li>
<li class="reveal" style="--i:2"><span class="why-ico">{ic("chat")}</span><div><h3>Ada orang yang bisa ditanya</h3><p>Gagal bubuh, salah posisi, atau bingung soal kuota? Hubungi kami lewat WhatsApp atau formulir. Kami membalas pada jam layanan, Senin sampai Sabtu.</p></div></li>
<li class="reveal" style="--i:3"><span class="why-ico">{ic("chart")}</span><div><h3>Riwayat tersimpan rapi</h3><p>Setiap pembubuhan tercatat di dasbor, jadi Anda tahu dokumen mana yang sudah bermeterai dan berapa sisa kuotanya.</p></div></li>
</ul></div>
</div></section>

<section class="section soft" id="faq" aria-labelledby="t-faq"><div class="wrap faq-wrap">
<div class="faq-side"><div class="section-head"><span class="eyebrow">FAQ</span><h2 id="t-faq" class="h-section">Yang paling sering ditanyakan</h2><p class="lead">Jawaban singkat sebelum Anda membeli.</p></div>
<div class="help-card"><img src="assets/img/mascot.png" alt="" width="64" height="64" loading="lazy"><div><b>Masih ada yang mengganjal?</b><span>Tanya langsung, kami balas pada jam layanan.</span></div>
<div class="acts"><a class="btn btn-wa btn-sm" data-wa="Halo E-Materai, saya mau tanya soal e-Meterai." href="https://wa.me/{PHONE_RAW.lstrip('+')}">{ic("chat")}WhatsApp</a><a class="btn btn-quiet btn-sm" href="kontak.html">Formulir kontak</a></div></div>
</div>
<div class="faq">{faq_html()}</div></div></section>

<section class="section" id="blog-terbaru" aria-labelledby="t-blog"><div class="wrap">
<div class="head-row"><div class="section-head"><span class="eyebrow">Blog</span><h2 id="t-blog" class="h-section">Baca dulu supaya tidak salah meterai</h2></div><a class="btn btn-quiet" href="blog.html">Semua artikel {ic("arrow-right","icon icon-go")}</a></div>
<div class="cards">{latest}</div>
</div></section>

<section class="section" style="padding-top:0" aria-labelledby="t-final"><div class="wrap"><div class="final reveal">
<div><h2 id="t-final">Dokumen Anda tinggal satu langkah lagi</h2><p>Buat akun, beli e-Meterai sesuai kebutuhan, dan bubuhkan ke PDF hari ini juga.</p>
<div class="acts"><a class="btn btn-primary btn-lg" href="daftar.html">Beli e-Meterai {ic("arrow-right","icon icon-go")}</a><a class="btn btn-wa btn-lg" data-wa="Halo E-Materai, saya mau tanya soal e-Meterai." href="https://wa.me/{PHONE_RAW.lstrip('+')}">{ic("chat")}Tanya via WhatsApp</a></div></div>
<div class="final-art" aria-hidden="true">{stamp()}{stamp("e2")}</div>
</div></div></section>

<div class="sticky-cta" aria-hidden="true"><div><small>e-Meterai resmi Peruri</small><b>Siap dalam hitungan menit</b></div><a class="btn btn-primary" href="daftar.html" tabindex="-1">Beli sekarang</a></div>
'''
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    svc = {"@context": "https://schema.org", "@type": "Service", "name": "Penjualan dan pembubuhan e-Meterai", "serviceType": "Meterai elektronik",
           "provider": {"@type": "Organization", "name": BRAND}, "areaServed": "ID", "audience": {"@type": "Audience", "audienceType": "Perorangan dan perusahaan"}}
    write('index.html', page(title, desc, '', 'home', body, ld=[ORG, WEBSITE, svc, faq_ld]))

# ======================================================================
# TENTANG
# ======================================================================
def about():
    title = 'Tentang E-Materai, Reseller e-Meterai Resmi'
    desc = f'Kenali E-Materai, reseller e-Meterai resmi yang dikelola {LEGAL}. Cara kami bekerja, prinsip layanan, dan cara menghubungi tim kami.'
    body = f'''
<section class="page-head"><div class="wrap"><div class="section-head"><span class="eyebrow">Tentang kami</span><h1 class="h-display" style="font-size:clamp(2.25rem,5vw,3.5rem)">Kami mengurus meterainya, Anda fokus ke dokumennya</h1>
<p class="lead">{BRAND} adalah reseller e-Meterai resmi yang dikelola {LEGAL}. Kami membantu perorangan dan perusahaan membubuhkan e-Meterai ke PDF dengan proses yang jelas dan langkah yang pendek.</p></div></div></section>
<section class="section" style="padding-top:clamp(24px,4vw,48px)"><div class="wrap split">
<div class="prose-block reveal"><h2 class="h-section">Kenapa {BRAND} ada</h2>
<p>Dokumen sekarang lahir dalam bentuk PDF. Anehnya, banyak orang masih mencetaknya hanya untuk menempel satu meterai, lalu memindainya lagi. Hasilnya sering buram, ukurannya kebesaran, dan waktunya habis di jalan.</p>
<p>e-Meterai menyelesaikan masalah itu. Yang masih kurang adalah tempat membeli yang jelas: prosesnya transparan, caranya gampang dipahami, dan ada orang yang bisa ditanya saat ada kendala. Itulah yang kami kerjakan.</p>
<div class="stats"><div class="stat"><b>Resmi</b><small>Diterbitkan Peruri</small></div><div class="stat"><b>3 langkah</b><small>Unggah, letakkan, PIN</small></div><div class="stat"><b>Senin–Sabtu</b><small>Jam layanan tim kami</small></div></div></div>
<figure class="figure-stamp perf-wrap reveal" style="--i:2"><div class="perf"><img src="assets/img/blog-aturan-bea-meterai.webp" alt="Meterai tempel dengan lambang Garuda Pancasila" width="699" height="389" loading="lazy"><figcaption><span class="seri">Resmi</span><span class="seri">Bea Meterai</span></figcaption></div></figure></div></section>
<section class="section soft"><div class="wrap"><div class="section-head"><span class="eyebrow">Yang kami pegang</span><h2 class="h-section">Tiga janji layanan</h2></div>
<div class="values">
<div class="value reveal"><span class="seri">01</span><h3 class="h-card">Transparan</h3><p>Rincian pembayaran selalu terlihat sebelum Anda membayar. Tidak ada paket yang wajib dibeli.</p></div>
<div class="value reveal" style="--i:1"><span class="seri">02</span><h3 class="h-card">Jalur resmi</h3><p>e-Meterai yang kami jual diterbitkan Peruri. Kami mengikuti aturan Bea Meterai yang berlaku dan memberi tahu bila ada perubahan.</p></div>
<div class="value reveal" style="--i:2"><span class="seri">03</span><h3 class="h-card">Bantuan yang nyata</h3><p>WhatsApp, telepon, email, dan formulir kontak. Tim kami membalas pada jam layanan.</p></div>
</div></div></section>
<section class="section"><div class="wrap split rev">
<ol class="timeline reveal"><li><div><b>Buat akun</b><span>Perorangan atau perusahaan. Cukup email dan nomor ponsel aktif.</span></div></li><li><div><b>Beli e-Meterai</b><span>Sesuai jumlah dokumen yang perlu dimeteraikan.</span></div></li><li><div><b>Bubuhkan ke PDF</b><span>Unggah, atur posisi, masukkan PIN, lalu unduh hasilnya.</span></div></li></ol>
<div class="prose-block reveal" style="--i:2"><span class="eyebrow">Cara kerja</span><h2 class="h-section">Dari akun sampai dokumen bermeterai</h2><p>Prosesnya dibuat sependek mungkin. Di beranda ada simulasi tiap langkah, termasuk menggeser posisi meterai di dokumen.</p><div style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-primary" href="index.html#cara">Lihat simulasinya</a><a class="btn btn-quiet" href="kontak.html">Hubungi kami</a></div></div></div></section>
'''
    ld = [ORG, crumbs_ld([('Beranda', 'index.html'), ('Tentang', 'tentang.html')]), {"@context": "https://schema.org", "@type": "AboutPage", "name": title, "url": f"{BASE}/tentang.html"}]
    write('tentang.html', page(title, desc, 'tentang.html', 'about', body, ld=ld))

# ======================================================================
# BLOG
# ======================================================================
def blog_index():
    title = 'Blog e-Meterai: Aturan, Panduan, dan Tips | E-Materai'
    desc = 'Artikel seputar e-Meterai dan Bea Meterai: perubahan aturan, panduan memakai materai elektronik, dokumen yang bebas bea, dan tips untuk pelamar CPNS.'
    cats = []
    for a in ARTICLES:
        if a['cat'] not in cats: cats.append(a['cat'])
    chips = '<button class="filter" type="button" data-f="semua" aria-pressed="true">Semua</button>' + ''.join(
        f'<button class="filter" type="button" data-f="{c.lower().replace(" ","-")}" aria-pressed="false">{c}</button>' for c in cats)
    cards = ''.join(post_card(a) for a in ARTICLES)
    body = f'''
<section class="page-head"><div class="wrap"><div class="section-head"><span class="eyebrow">Blog</span><h1 class="h-display" style="font-size:clamp(2.25rem,5vw,3.5rem)">Informasi pilihan seputar e-Meterai</h1><p class="lead">Aturan terbaru, panduan langkah demi langkah, dan jawaban untuk pertanyaan yang sering muncul.</p></div></div></section>
<section class="section" style="padding-top:clamp(16px,3vw,32px)"><div class="wrap">
<div class="toolbar"><div class="filters" role="group" aria-label="Filter kategori">{chips}</div>
<div class="search">{ic("search")}<label class="sr" for="blog-search">Cari artikel</label><input id="blog-search" class="input" type="search" placeholder="Cari artikel" autocomplete="off" style="min-height:46px;padding-left:42px"></div></div>
<p class="muted" id="blog-count" aria-live="polite" style="margin:-12px 0 20px;font-size:.9375rem">{len(ARTICLES)} artikel</p>
<div class="cards blog-grid">{cards}</div>
<div class="empty"><p><b>Tidak ada artikel yang cocok.</b></p><p>Coba kata kunci lain, atau pilih kategori Semua.</p></div>
</div></section>
'''
    items = [{"@type": "ListItem", "position": i + 1, "url": f"{BASE}/blog/{a['slug']}.html", "name": a['title']} for i, a in enumerate(ARTICLES)]
    ld = [ORG, crumbs_ld([('Beranda', 'index.html'), ('Blog', 'blog.html')]), {"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "url": f"{BASE}/blog.html", "mainEntity": {"@type": "ItemList", "itemListElement": items}}]
    write('blog.html', page(title, desc, 'blog.html', 'blog', body, ld=ld))

def article_page(a):
    rel = '../'
    heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', a['body'])
    toc = ''
    if len(heads) >= 3:
        toc = '<aside class="toc" aria-label="Daftar isi"><h2>Di artikel ini</h2><ol>' + ''.join(f'<li><a href="#{i}">{re.sub("<.*?>","",t)}</a></li>' for i, t in heads) + '</ol></aside>'
    others = [x for x in ARTICLES if x['slug'] != a['slug']]
    others.sort(key=lambda x: (x['cat'] != a['cat']))
    rel_cards = ''.join(post_card(x, rel) for x in others[:3])
    title = f"{a['title']} | {BRAND}"
    if len(title) > 62: title = a['title']
    meta = f'<span class="tag">{a["cat"]}</span>' + (f'<time datetime="{a["date"]}">{a["date_id"]}</time>' if a['date'] else '') + f'<span>{a["read"]} menit baca</span>'
    body = f'''
<div class="wrap"><ol class="crumbs" aria-label="Jejak halaman"><li><a href="../index.html">Beranda</a></li><li><a href="../blog.html">Blog</a></li><li aria-current="page">{esc(a['title'])}</li></ol></div>
<article class="wrap" style="padding-bottom:clamp(48px,7vw,96px)">
<header class="article-head"><div class="article-meta">{meta}</div><h1>{esc(a['title'])}</h1></header>
<figure class="article-hero" style="margin-inline:auto"><img src="../assets/img/{a['hero']}" alt="{esc(a['alt'])}" width="1400" height="454" fetchpriority="high"></figure>
<div class="article-grid{'' if toc else ' no-toc'}"><div class="prose">
{a['body']}
<section class="cta-card" aria-labelledby="cta-t"><h2 id="cta-t">Dokumen Anda siap dimeteraikan?</h2><p>Beli e-Meterai resmi, lalu bubuhkan langsung ke PDF dari ponsel atau laptop.</p><a class="btn btn-primary btn-lg" href="../daftar.html">Beli e-Meterai {ic("arrow-right","icon icon-go")}</a></section>
<div class="share"><b>Bagikan:</b><button class="btn btn-quiet" type="button" data-copy>{ic("link")}Salin tautan</button><a class="btn btn-quiet" data-share="wa" target="_blank" rel="noopener" href="#">{ic("chat")}WhatsApp</a><a class="btn btn-quiet" data-share="li" target="_blank" rel="noopener" href="#">{ic("linkedin")}LinkedIn</a><a class="btn btn-quiet" data-share="x" target="_blank" rel="noopener" href="#">{ic("x-social")}X</a></div>
</div>{toc}</div>
<section class="related" aria-labelledby="rel-t"><h2 id="rel-t" class="h-section" style="font-size:1.75rem;margin-bottom:28px">Artikel lainnya</h2><div class="cards">{rel_cards}</div></section>
</article>
'''
    ld = [ORG, crumbs_ld([('Beranda', 'index.html'), ('Blog', 'blog.html'), (a['title'], f"blog/{a['slug']}.html")])]
    art = {"@context": "https://schema.org", "@type": "Article", "headline": a['title'], "description": a['desc'], "inLanguage": "id-ID",
           "image": f"{BASE}/assets/img/{a['hero']}", "mainEntityOfPage": f"{BASE}/blog/{a['slug']}.html",
           "author": {"@type": "Organization", "name": BRAND}, "publisher": {"@type": "Organization", "name": LEGAL, "logo": {"@type": "ImageObject", "url": f"{BASE}/assets/img/logo-512.png"}}}
    if a['date']: art['datePublished'] = a['date']; art['dateModified'] = a['date']
    ld.append(art)
    write(f"blog/{a['slug']}.html", page(title, a['desc'], f"blog/{a['slug']}.html", 'blog', body, rel=rel, ld=ld, typ='article', og=f"assets/img/{a['hero']}"))

# ======================================================================
# KONTAK
# ======================================================================
def contact():
    title = 'Hubungi Kami | Kontak E-Materai'
    desc = f'Ada pertanyaan soal e-Meterai atau kendala transaksi? Kirim pesan, telepon, atau chat WhatsApp. Kantor di Cibubur, Kota Bekasi. Layanan Senin–Sabtu.'
    hours = ''.join(f'<span style="display:flex;justify-content:space-between;gap:16px;max-width:260px"><span>{d}</span><span class="num">{t}</span></span>' for d, t in HOURS)
    body = f'''
<section class="page-head"><div class="wrap"><div class="section-head"><span class="eyebrow">Kontak</span><h1 class="h-display" style="font-size:clamp(2.25rem,5vw,3.5rem)">Ada yang bisa kami bantu?</h1><p class="lead">Pertanyaan soal e-Meterai, kendala transaksi, atau penawaran untuk perusahaan. Tulis saja, tim kami yang membalas.</p></div></div></section>
<section class="section" style="padding-top:clamp(16px,3vw,32px)"><div class="wrap contact">
<aside class="contact-info" aria-label="Informasi kontak"><div><h2>Butuh jawaban cepat?</h2><p class="muted" style="margin-top:6px">Untuk pertanyaan singkat, WhatsApp paling praktis. Sertakan nomor transaksi bila terkait pembelian.</p></div>
<img src="assets/img/contact-illustration.png" alt="Ilustrasi koper, ponsel, telepon, dan jam" width="826" height="276" loading="lazy">
<ul class="cinfo">
<li><span class="ci">{ic("chat")}</span><div><b>WhatsApp</b><a data-wa="Halo E-Materai, saya ingin bertanya soal e-Meterai." href="https://wa.me/{PHONE_RAW.lstrip('+')}">{PHONE}</a></div></li>
<li><span class="ci">{ic("phone")}</span><div><b>Telepon</b><a href="tel:{PHONE_RAW}">{PHONE}</a></div></li>
<li><span class="ci">{ic("mail")}</span><div><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
<li><span class="ci">{ic("pin")}</span><div><b>Alamat</b>{ADDRESS}</div></li>
<li><span class="ci">{ic("clock")}</span><div><b>Jam layanan</b>{hours}</div></li>
</ul></aside>
<div class="contact-form"><h2 class="h-card" style="font-size:1.5rem">Lengkapi data Anda</h2><p class="muted" style="margin:6px 0 24px">Kami membalas pada jam layanan. Kolom bertanda * wajib diisi.</p>
<form id="form-contact" class="form" novalidate>
<div class="row2">
<div class="field"><label for="c-nama">Nama lengkap *</label><input class="input" id="c-nama" name="nama" autocomplete="name" data-v="required" aria-describedby="c-nama-e"><div class="err" id="c-nama-e" role="alert">{ic("alert","icon",'style="width:16px;height:16px"')}<span></span></div></div>
<div class="field"><label for="c-email">Email *</label><input class="input" id="c-email" name="email" type="email" inputmode="email" autocomplete="email" placeholder="nama@email.com" data-v="required email" aria-describedby="c-email-e"><div class="err" id="c-email-e" role="alert">{ic("alert","icon",'style="width:16px;height:16px"')}<span></span></div></div></div>
<div class="row2">
<div class="field"><label for="c-topik">Topik *</label><select class="input" id="c-topik" name="topik" data-v="required"><option value="">Pilih topik</option><option value="umum">Pertanyaan umum</option><option value="transaksi">Kendala transaksi</option><option value="penawaran">Penawaran untuk perusahaan</option><option value="lainnya">Lainnya</option></select><div class="err" role="alert">{ic("alert","icon",'style="width:16px;height:16px"')}<span></span></div></div>
<div class="field"><label for="c-trx">Nomor transaksi <span class="opt">(opsional)</span></label><input class="input" id="c-trx" name="transaksi" placeholder="Jika terkait transaksi"></div></div>
<div class="field"><label for="c-pesan">Pesan *</label><textarea class="input" id="c-pesan" name="pesan" maxlength="1000" placeholder="Tulis kebutuhan atau kendala Anda sejelas mungkin" data-v="min10" aria-describedby="c-pesan-e"></textarea><div class="row-between"><div class="err" id="c-pesan-e" role="alert">{ic("alert","icon",'style="width:16px;height:16px"')}<span></span></div><span class="counter num" id="msg-count">0/1000</span></div></div>
<div class="alert" role="status">{ic("info")}<span></span></div>
<div style="display:flex;gap:12px;flex-wrap:wrap"><button class="btn btn-primary btn-lg" type="submit"><span class="spin"></span><span>Kirim pesan</span></button></div>
</form></div>
</div></section>
'''
    ld = [ORG, crumbs_ld([('Beranda', 'index.html'), ('Kontak', 'kontak.html')]), {"@context": "https://schema.org", "@type": "ContactPage", "name": title, "url": f"{BASE}/kontak.html"}]
    write('kontak.html', page(title, desc, 'kontak.html', 'contact', body, ld=ld))

# ======================================================================
# MASUK
# ======================================================================
def login():
    title = 'Masuk ke Akun | E-Materai'
    desc = 'Masuk ke akun E-Materai untuk membeli dan membubuhkan e-Meterai pada dokumen Anda.'
    errI = lambda i='': f'<div class="err" role="alert">{ic("alert","icon",chr(115)+"tyle=\"width:16px;height:16px\"")}<span></span></div>'
    body = f'''
<section class="auth">
<aside class="auth-art">{stamp()}<h2>Lanjutkan memeterai dokumen Anda</h2><ul><li>{ic("check")}Riwayat pembubuhan tersimpan di dasbor</li><li>{ic("check")}Sisa kuota terlihat sebelum membeli lagi</li><li>{ic("check")}Bantuan via WhatsApp pada jam layanan</li></ul></aside>
<div class="auth-main"><div class="auth-card">
{brand('')}
<div id="view-login" class="view">
<div><h1>Selamat datang kembali</h1><p class="sub">Masuk untuk melanjutkan ke akun Anda.</p></div>
<form id="form-login" class="form" novalidate>
<div class="field"><label for="l-id">Email atau nomor ponsel</label><input class="input" id="l-id" name="id" autocomplete="username" inputmode="email" placeholder="nama@email.com" data-v="required emailOrPhone">{errI()}</div>
<div class="field"><label for="l-pw">Kata sandi</label><div class="input-wrap"><input class="input has-btn" id="l-pw" name="password" type="password" autocomplete="current-password" data-v="required"><button class="toggle" type="button" aria-label="Tampilkan kata sandi" aria-pressed="false">{ic("eye","icon i-on")}{ic("eye-off","icon i-off")}</button></div>{errI()}</div>
<div class="row-between"><label class="check"><input type="checkbox" name="ingat" checked><span>Ingat saya</span></label><a href="#" data-view="reset" style="font-weight:600;min-height:44px;display:inline-flex;align-items:center">Lupa kata sandi?</a></div>
<div class="alert" role="status">{ic("info")}<span></span></div>
<button class="btn btn-primary btn-lg btn-block" type="submit"><span class="spin"></span><span>Masuk</span></button>
</form></div>
<div id="view-reset" class="view" hidden>
<div><h2 style="font-size:1.625rem;letter-spacing:-.025em">Atur ulang kata sandi</h2><p class="sub">Masukkan email akun Anda. Kami kirim tautan untuk membuat kata sandi baru.</p></div>
<form id="form-reset" class="form" novalidate>
<div class="field"><label for="r-email">Email</label><input class="input" id="r-email" name="email" type="email" autocomplete="email" placeholder="nama@email.com" data-v="required email">{errI()}</div>
<div class="alert" role="status">{ic("info")}<span></span></div>
<button class="btn btn-primary btn-lg btn-block" type="submit"><span class="spin"></span><span>Kirim tautan</span></button>
<button class="btn btn-ghost btn-block" type="button" data-view="login">{ic("arrow-left")}Kembali ke halaman masuk</button>
</form></div>
<p class="auth-foot">Belum punya akun? <a href="daftar.html">Daftar sekarang</a></p>
</div></div></section>
'''
    write('masuk.html', page(title, desc, 'masuk.html', None, body, noindex=True, foot=False))

# ======================================================================
# DAFTAR
# ======================================================================
def register():
    title = 'Daftar Akun e-Meterai | E-Materai'
    desc = 'Buat akun E-Materai sebagai perorangan atau perusahaan untuk membeli dan membubuhkan e-Meterai.'
    I = lambda: f'<div class="err" role="alert">{ic("alert","icon","style=\"width:16px;height:16px\"")}<span></span></div>'
    body = f'''
<div class="reg">
<aside class="reg-side"><div><h2>Satu akun untuk semua dokumen bermeterai</h2><ul><li>{ic("check")}Beli e-Meterai sesuai jumlah dokumen</li><li>{ic("check")}Bubuhkan ke PDF dari ponsel atau laptop</li><li>{ic("check")}Riwayat dan sisa kuota tercatat rapi</li></ul></div><img src="assets/img/mascot.png" alt="" width="397" height="1126"></aside>
<div class="reg-main">
<ol class="stepper" aria-label="Langkah pendaftaran" style="list-style:none;padding:0;margin:0">
<li class="s on"><span class="dot" aria-hidden="true">1</span><span><b>Jenis akun</b><small>Pilih tipe pengguna</small></span></li>
<li class="line" aria-hidden="true" style="--p:0"></li>
<li class="s"><span class="dot" aria-hidden="true">2</span><span><b>Data akun</b><small>Lengkapi detail</small></span></li></ol>
<form id="form-register" class="form" novalidate>
<div id="step-1" class="view">
<div><h1 style="font-size:1.875rem;letter-spacing:-.03em">Pilih jenis akun</h1><p class="sub muted" style="margin-top:6px">Pilih yang paling sesuai dengan kebutuhan Anda. Bisa diubah kapan saja sebelum mendaftar.</p></div>
<fieldset style="border:0;padding:0;margin:0" class="types"><legend class="sr">Jenis akun</legend>
<label class="type"><input type="radio" name="tipe" value="personal" checked><span class="radio"></span><span class="t-ico">{ic("user")}</span><b>Perorangan</b><span>Memeterai surat pernyataan, perjanjian, atau dokumen pribadi tanpa ke kantor pos.</span></label>
<label class="type"><input type="radio" name="tipe" value="enterprise"><span class="radio"></span><span class="t-ico">{ic("building")}</span><b>Perusahaan</b><span>Memeterai kontrak dan dokumen bisnis, dengan pemakaian yang bisa dipantau.</span></label></fieldset>
<div class="wiz-nav"><a class="btn btn-ghost" href="masuk.html">Sudah punya akun</a><button class="btn btn-primary btn-lg" type="button" id="to-2">Lanjut {ic("arrow-right")}</button></div>
</div>
<div id="step-2" class="view" hidden>
<div><h2 style="font-size:1.875rem;letter-spacing:-.03em">Lengkapi data akun</h2><p class="sub muted" style="margin-top:6px">Gunakan email dan nomor ponsel yang aktif. Kami mengirim notifikasi transaksi ke sana.</p></div>
<div class="row2"><div class="field"><label for="g-first">Nama depan *</label><input class="input" id="g-first" name="nama_depan" autocomplete="given-name" data-v="required">{I()}</div>
<div class="field"><label for="g-last">Nama belakang</label><input class="input" id="g-last" name="nama_belakang" autocomplete="family-name"></div></div>
<div class="field"><label for="g-email">Email *</label><input class="input" id="g-email" name="email" type="email" inputmode="email" autocomplete="email" placeholder="nama@email.com" data-v="required email">{I()}</div>
<div class="field"><label for="g-hp">Nomor ponsel *</label><div class="input-wrap"><span class="prefix">+62</span><input class="input has-prefix" id="g-hp" name="hp" type="tel" inputmode="tel" autocomplete="tel-national" placeholder="812 3456 7890" data-v="required phone"></div><div class="hint">Tanpa angka 0 di depan.</div>{I()}</div>
<div class="field ent-only" hidden><label for="g-pt">Nama perusahaan *</label><input class="input" id="g-pt" name="perusahaan" autocomplete="organization" data-ent-required data-v="">{I()}</div>
<div class="row2"><div class="field"><label for="reg-pw">Kata sandi *</label><div class="input-wrap"><input class="input has-btn" id="reg-pw" name="password" type="password" autocomplete="new-password" data-v="required min8"><button class="toggle" type="button" aria-label="Tampilkan kata sandi" aria-pressed="false">{ic("eye","icon i-on")}{ic("eye-off","icon i-off")}</button></div><div class="strength" data-s="0" aria-hidden="true"><i></i><i></i><i></i><i></i></div><div class="hint">Minimal 8 karakter. <span id="pw-label" style="font-weight:600"></span></div>{I()}</div>
<div class="field"><label for="reg-pw2">Ulangi kata sandi *</label><div class="input-wrap"><input class="input has-btn" id="reg-pw2" name="password2" type="password" autocomplete="new-password" data-match="#reg-pw" data-v="required match"><button class="toggle" type="button" aria-label="Tampilkan kata sandi" aria-pressed="false">{ic("eye","icon i-on")}{ic("eye-off","icon i-off")}</button></div>{I()}</div></div>
<div class="field ent-only" hidden><label for="g-alamat">Alamat perusahaan <span class="opt">(opsional)</span></label><textarea class="input" id="g-alamat" name="alamat" style="min-height:92px" placeholder="Jl. Contoh No. 1, Kota"></textarea></div>
<div class="field check-field"><label class="check"><input type="checkbox" name="setuju" data-v="consent"><span>Saya menyetujui <a href="syarat-ketentuan.html" target="_blank">Syarat &amp; Ketentuan</a> dan <a href="kebijakan-privasi.html" target="_blank">Kebijakan Privasi</a>.</span></label>{I()}</div>
<div class="alert" role="status">{ic("info")}<span></span></div>
<div class="wiz-nav"><button class="btn btn-quiet btn-lg" type="button" id="to-1">{ic("arrow-left")}Kembali</button><button class="btn btn-primary btn-lg" type="submit"><span class="spin"></span><span>Buat akun</span></button></div>
</div>
</form></div></div>
'''
    write('daftar.html', page(title, desc, 'daftar.html', None, body, noindex=True, foot=False))

# ======================================================================
# 404 & LEGAL
# ======================================================================
def notfound():
    title = 'Halaman Tidak Ditemukan | E-Materai'
    body = f'''
<section class="nf"><div>
<img src="assets/img/404.png" alt="Ilustrasi tiga dimensi angka 404 dengan kursor dan tanda silang" width="900" height="778">
<h1 class="h-section">Halaman ini tidak ditemukan</h1>
<p class="lead" style="margin-top:10px">Alamatnya mungkin salah ketik, atau halamannya sudah dipindahkan.</p>
<div class="nf-links"><a class="btn btn-primary btn-lg" href="index.html">Kembali ke beranda</a><a class="btn btn-quiet btn-lg" href="blog.html">Baca blog</a><a class="btn btn-quiet btn-lg" href="kontak.html">Hubungi kami</a></div>
<p class="nf-sugg"><span class="muted">Mungkin yang Anda cari:</span><a href="index.html#cek">Cek dokumen</a><a href="index.html#cara">Cara pakai</a><a href="blog/cara-beli-emeterai-untuk-cpns-dan-pppk.html">Panduan CPNS</a></p>
</div></section>
'''
    write('404.html', page(title, 'Halaman yang Anda cari tidak ditemukan. Kembali ke beranda E-Materai, baca blog e-Meterai, atau hubungi tim kami.', '404.html', None, body, noindex=True))

def legal(slug, title, intro, sections):
    secs = ''.join(f'<h2 id="s{i}">{t}</h2>{p}' for i, (t, p) in enumerate(sections))
    body = f'''
<section class="page-head"><div class="wrap legal"><div class="section-head"><span class="eyebrow">Legal</span><h1 class="h-display" style="font-size:clamp(2rem,4.5vw,3rem)">{title}</h1></div></div></section>
<section class="section" style="padding-top:16px"><div class="wrap legal"><div class="draft">{ic("alert")}<span><b>Draf kerangka.</b> Teks ini adalah kerangka awal dan harus ditinjau serta disesuaikan oleh tim legal {LEGAL} sebelum situs diterbitkan.</span></div>
<div class="prose"><p class="lead-in">{intro}</p>{secs}</div></div></section>'''
    ld = [crumbs_ld([('Beranda', 'index.html'), (title, f'{slug}.html')])]
    write(f'{slug}.html', page(f'{title.replace("&amp;","&")} | {BRAND}', intro + ' Halaman ini masih berupa draf kerangka.', f'{slug}.html', None, body, ld=ld))

def legals():
    legal('kebijakan-privasi', 'Kebijakan Privasi', f'Kebijakan ini menjelaskan data apa yang dikumpulkan {BRAND} dan bagaimana data itu digunakan.', [
        ('Data yang kami kumpulkan', '<p>Nama, email, nomor ponsel, dan data perusahaan (untuk akun perusahaan) saat Anda mendaftar, serta dokumen PDF yang Anda unggah untuk dimeteraikan.</p>'),
        ('Tujuan penggunaan', '<p>Data digunakan untuk membuat akun, memproses pembelian dan pembubuhan e-Meterai, mengirim notifikasi transaksi, dan memberikan bantuan.</p>'),
        ('Hak Anda', '<p>Anda dapat meminta akses, perbaikan, atau penghapusan data pribadi sesuai ketentuan perundang-undangan perlindungan data pribadi yang berlaku. Hubungi kami melalui halaman kontak.</p>'),
        ('Kontak', f'<p>Pertanyaan soal privasi dapat dikirim ke <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>')])
    legal('syarat-ketentuan', 'Syarat &amp; Ketentuan', f'Dengan memakai layanan {BRAND}, Anda menyetujui ketentuan berikut.', [
        ('Layanan', f'<p>{BRAND} adalah channel penjualan e-Meterai yang dikelola {LEGAL}. e-Meterai dibubuhkan pada dokumen berformat PDF.</p>'),
        ('Tanggung jawab pengguna', '<p>Pengguna bertanggung jawab atas kebenaran dan kewajiban memeterai dokumennya, serta atas kerahasiaan kata sandi dan PIN.</p>'),
        ('Pembayaran dan pengembalian dana', '<p>Ketentuan pembayaran dan pengembalian dana mengikuti kebijakan yang akan dicantumkan di sini oleh tim legal.</p>'),
        ('Perubahan ketentuan', '<p>Ketentuan dapat diperbarui sewaktu-waktu. Versi terbaru selalu tersedia di halaman ini.</p>')])

# ======================================================================
def seo_files():
    urls = ['', 'tentang.html', 'blog.html', 'kontak.html'] + [f"blog/{a['slug']}.html" for a in ARTICLES] + ['kebijakan-privasi.html', 'syarat-ketentuan.html']
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{BASE}/{u}</loc></url>\n' for u in urls) + '</urlset>\n'
    write('sitemap.xml', xml)
    write('robots.txt', f'User-agent: *\nAllow: /\nDisallow: /masuk.html\nDisallow: /daftar.html\n\nSitemap: {BASE}/sitemap.xml\n')

if __name__ == '__main__':
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(SRC, 'assets'), os.path.join(OUT, 'assets'))
    home(); about(); blog_index(); [article_page(a) for a in ARTICLES]; contact(); login(); register(); notfound(); legals(); seo_files()
    print('built ->', OUT)
