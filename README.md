# E-Materai: website statis

Situs statis multi-halaman (HTML, CSS, JS murni, tanpa framework). Buka `index.html` di browser, atau unggah seluruh folder ke hosting apa pun.

## Isi
- `index.html` Beranda · `tentang.html` · `blog.html` + 9 artikel di `blog/` · `kontak.html`
- `masuk.html` · `daftar.html` (2 langkah) · `404.html` · `kebijakan-privasi.html` · `syarat-ketentuan.html`
- `sitemap.xml`, `robots.txt`, `assets/` (css, js, gambar)
- `_source/` skrip pembuat halaman (`build.py`), isi artikel dan FAQ (`content.py`), dan pembuat versi satu file (`standalone.py`)

## Yang perlu Anda ganti
Semua ada di bagian atas `_source/build.py`:
- `BASE` domain final (dipakai canonical, sitemap, Open Graph)
- `PHONE`, `EMAIL`, `ADDRESS`, `HOURS`, `SOCIAL` (semua masih contoh)
- Nama merek `E-Materai` (`BRAND`) dan logo: simbol `logo-mark` di `SPRITE`, `assets/img/favicon.svg`, `logo-512.png`, `og.png`

Setelah mengubah, jalankan `python3 _source/build.py`. Hasilnya ditulis ke folder baru `_build/`; salin isinya menggantikan file di folder utama (folder `assets/` tetap sumber gambar dan CSS/JS).

## Menghubungkan formulir
Formulir masih mode demo. Isi alamat API di `assets/js/app.js`, objek `CONFIG.endpoints` (`login`, `register`, `reset`, `contact`). Data dikirim sebagai JSON lewat POST.
Nomor WhatsApp: `CONFIG.whatsapp`.

## Catatan hosting
Tautan memakai ekstensi `.html` supaya bisa dibuka langsung dari folder. Jika hosting Anda mendukung URL bersih (misalnya `/tentang`), aktifkan lalu sesuaikan `BASE` dan tautan di `build.py`.
Font Plus Jakarta Sans dimuat dari Google Fonts; tanpa internet, situs memakai font sistem.

## Versi satu file
Jalankan `python3 _source/standalone.py` untuk membuat `_build/emeterai-standalone.html`: semua halaman, CSS, JS, dan gambar dalam satu file untuk pratinjau. Untuk tayang dan SEO, pakai versi multi-file.

## Sebelum tayang
Baca bagian "Yang perlu diverifikasi" di `AUDIT-UIUX.md`. Isi hukum dan pajak perlu ditinjau tim legal, dan dua halaman legal masih draf kerangka.
