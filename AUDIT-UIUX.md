# Audit UI/UX dan keputusan perbaikan

Audit ini dibuat dari 8 layar yang dikirim: beranda, blog, artikel, kontak, masuk, daftar (2 langkah), dan 404. Tidak ada akses ke situs live, jadi semua penilaian berasal dari tampilan layar, bukan dari kode atau data analitik.

## Yang sudah baik (dipertahankan)
- Palet satu aksen indigo, tipografi Inter, dan kartu putih di atas latar abu muda terasa bersih dan konsisten di semua halaman.
- Alur daftar dua langkah dengan stepper jelas, dan ada tombol mode gelap.
- Beranda punya struktur lengkap: hero, penjelasan produk, layanan, cara pakai, blog, FAQ, ajakan bertindak.
- Halaman 404 ramah dan punya tombol keluar.

## Temuan dan perbaikan

| # | Temuan | Dampak | Perbaikan di versi baru |
|---|--------|--------|-------------------------|
| 1 | Header dua lapis (logo lalu menu) memakai ±180px tinggi layar sebelum konten. | Konten utama turun ke bawah, terutama di laptop kecil dan ponsel. | Satu baris header 68px, menempel di atas (sticky), menu jadi panel di ponsel. |
| 2 | Tombol "Login / Register" digabung jadi satu. | Pengguna lama dan baru diarahkan ke tempat yang sama, bingung memilih. | Dipisah: "Masuk" (sekunder) dan "Daftar" (utama). |
| 3 | Teks halaman daftar langkah 1 berisi copy template properti ("List your property as an individual to lease, rent, or sell…"). | Merusak kepercayaan, jelas salah konteks. | Ditulis ulang sesuai produk: Perorangan dan Perusahaan. |
| 4 | Halaman masuk dan daftar berbahasa Inggris, sementara beranda, blog, dan kontak berbahasa Indonesia. Kolom login bernama "Full name". | Pengalaman terasa tidak utuh; login dengan nama lengkap tidak lazim. | Seluruh teks Indonesia; login memakai email atau nomor ponsel. |
| 5 | Dua kolom bernama sama "Password" tanpa pembeda; tidak ada indikator kekuatan atau syarat sandi. | Salah ketik tidak terdeteksi. | "Kata sandi" dan "Ulangi kata sandi", meteran kekuatan, validasi saat berpindah kolom. |
| 6 | Semua kolom di form daftar berwarna biru aktif. Tidak bisa dibedakan mana yang sedang diisi, sudah terisi, atau salah. | Status form tidak terbaca. | Tiga status jelas: normal, fokus (cincin), salah (merah + pesan di bawah kolom). |
| 7 | Tombol Submit berwarna cyan, beda dengan warna tombol utama di seluruh situs. | Aksi utama terlihat tidak konsisten. | Semua tombol utama memakai satu warna. |
| 8 | Tidak ada persetujuan syarat dan privasi saat mendaftar. | Risiko kepatuhan (data pribadi) dan kepercayaan. | Kotak persetujuan wajib + halaman Kebijakan Privasi dan Syarat (draf kerangka, perlu ditinjau tim legal). |
| 9 | Kolom "Company Name" muncul untuk semua pengguna, termasuk perorangan. | Kolom tidak relevan memperlambat pengisian. | Hanya muncul jika memilih Perusahaan. |
| 10 | Nomor hotline di halaman kontak berkode negara +84 (Vietnam), sedangkan nomor lain +62. | Kesalahan data. | Semua memakai +62 (nomor contoh, ganti dengan nomor asli). |
| 11 | Klaim "Customer Support 24/7" bertabrakan dengan jam kerja Senin–Jumat 09.00–18.00. | Ekspektasi pengguna tidak sesuai kenyataan. | Dituliskan jujur: pusat bantuan 24 jam, tim membalas pada jam layanan. |
| 12 | Tidak ada harga di mana pun, padahal tombol "Beli Sekarang" ada di beranda. | Calon pembeli harus daftar dulu untuk tahu biaya. | Bagian harga + kalkulator (tarif Rp10.000 per e-Meterai). |
| 13 | Paragraf "Apa sih eMaterai itu?" rata kanan-kiri dengan huruf kecil. | Sulit dibaca, jarak antarkata tidak rata. | Rata kiri, 17px, lebar baris ±60 karakter. |
| 14 | Kata "Evisiensi" (salah ketik), "Materai" dan "Meterai" tercampur, "Kontak" di footer vs "Contact" di menu. | Tampak kurang rapi; ejaan tidak seragam untuk SEO. | Ejaan baku "meterai" dipakai di judul, kata "materai" tetap muncul di isi supaya cocok dengan pencarian. Menu seragam Indonesia. |
| 15 | Judul artikel dipotong di tengah kata ("…Materai Elektronik di..."). | Judul tidak bisa dibaca utuh. | Judul tampil penuh; hanya ringkasan yang dipotong di akhir kalimat. |
| 16 | Kartu blog tidak punya kategori, waktu baca, atau pencarian. Paginasi 1–10 padahal artikel hanya sembilan. | Sulit menemukan artikel; paginasi palsu menyesatkan. | Filter kategori, kolom cari, waktu baca. Paginasi dihapus. |
| 17 | Halaman artikel: teks ±13px, subjudul berupa teks tebal biasa, ada paragraf penutup yang sama persis dengan paragraf ketiga, tidak ada daftar isi, artikel terkait, atau ajakan di akhir. Ikon bagikan tanpa label. | Sulit dibaca dan tidak mengarahkan pembaca ke langkah berikut. | Teks 18px/1.75, subjudul h2/h3 asli, daftar isi yang ikut bergulir, artikel terkait, kartu ajakan, tombol bagikan berlabel. |
| 18 | Halaman kontak: placeholder sebagai label, tidak ada pilihan topik, tulisan di kartu ungu berukuran 10px dengan kontras rendah. | Form sulit dipakai, teks susah dibaca. | Label tetap di atas kolom, pilihan topik, WhatsApp, tulisan 16px dengan kontras terukur. |
| 19 | 404: hanya satu tombol, bahasa Inggris, ikon peringatan berlebih. | Pengunjung buntu. | Tiga jalan keluar (beranda, blog, kontak), bahasa Indonesia. |
| 20 | Footer tanpa tautan legal, alamat, atau kontak; judul "Get more information" berbahasa Inggris. | Kurang kepercayaan. | Footer empat kolom: menu, layanan, kontak, legal. |

## Hal tambahan untuk SEO
- Satu H1 per halaman, judul dan deskripsi unik, canonical, Open Graph, Twitter card.
- Data terstruktur: Organization, WebSite, Service, FAQPage, BreadcrumbList, Article, CollectionPage, ContactPage.
- sitemap.xml dan robots.txt; halaman masuk, daftar, dan 404 diberi noindex.
- Konten yang semula sangat ringkas diperluas: penjelasan e-Meterai, dokumen yang dikenai bea, harga, FAQ delapan pertanyaan, dan sembilan artikel.
- Gambar punya teks alternatif, dimensi, dan lazy loading; tema gelap, fokus keyboard, dan `prefers-reduced-motion` didukung.

## Yang perlu diverifikasi sebelum tayang
1. Semua isi hukum dan pajak (UU 10/2020, ambang Rp5.000.000, contoh dokumen bebas bea, ketentuan pengembalian dana) ditulis dari pengetahuan umum dan isi gambar. Pencarian web tidak tersedia saat membuat ini, jadi belum dicek ke sumber resmi. Mohon ditinjau tim legal atau pajak.
2. Nomor telepon, email, tautan media sosial, dan domain (`https://logoipsum.com`) masih berupa contoh.
3. Formulir masih mode demo: validasi jalan, tetapi belum terkirim ke server.
