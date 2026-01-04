# Panduan Deployment ke Vercel

## Persiapan

Sebelum melakukan deployment ke Vercel, pastikan Anda telah menyiapkan file-file berikut:

1. `app.py` - File utama aplikasi Flask Anda
2. `requirements.txt` - Daftar dependensi Python
3. `vercel.json` - File konfigurasi untuk Vercel (sudah disediakan)

## Langkah-langkah Deployment

### 1. Instalasi Vercel CLI (opsional)
Jika Anda ingin melakukan deployment dari command line:
```bash
npm install -g vercel
```

### 2. Inisialisasi Proyek di Vercel
- Buat akun di [vercel.com](https://vercel.com)
- Import repository GitHub Anda ke Vercel
- Atau gunakan Vercel CLI:
```bash
vercel
```

### 3. Konfigurasi Deployment
- Pastikan framework yang dipilih adalah "Other Framework" atau biarkan Vercel mendeteksi secara otomatis
- Pastikan build command adalah `pip install -r requirements.txt`
- Pastikan root directory adalah folder yang berisi `app.py`

### 4. Environment Variables (jika diperlukan)
Jika Anda ingin menggunakan database produksi atau konfigurasi lainnya, Anda bisa menambahkan environment variables di pengaturan proyek Vercel.

## Catatan Penting

1. **Database SQLite**: Aplikasi ini menggunakan SQLite yang disimpan dalam file lokal. Di lingkungan serverless seperti Vercel, file ini tidak akan persisten. Untuk produksi, pertimbangkan untuk menggunakan database eksternal seperti PostgreSQL atau MySQL.

2. **Upload Folder**: Folder upload juga tidak akan persisten di Vercel. Untuk produksi, pertimbangkan untuk menggunakan layanan penyimpanan eksternal seperti AWS S3.

3. **Static Files**: Pastikan file CSS, JS, dan gambar diakses dengan benar melalui Flask's `url_for()` function.

## Struktur File yang Dibutuhkan

Pastikan struktur file Anda mencakup:
```
├── app.py (entry point untuk aplikasi Flask)
├── requirements.txt (daftar dependensi)
├── vercel.json (konfigurasi Vercel)
├── config.py (konfigurasi aplikasi)
├── controllers/ (logika kontroler)
├── models/ (model database)
├── templates/ (file HTML template)
├── static/ (file CSS, JS, dan gambar)
└── utils/ (fungsi-fungsi utilitas)
```

## Troubleshooting

Jika mengalami masalah saat deployment:
1. Pastikan semua dependensi terdaftar di `requirements.txt`
2. Pastikan tidak ada path absolut yang digunakan
3. Pastikan aplikasi bisa berjalan lokal sebelum di-deploy
4. Periksa log deployment di dashboard Vercel untuk informasi error