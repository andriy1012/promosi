# Sistem Rekomendasi Promosi PT. Natura Boga

Sistem berbasis web untuk analisis pola pembelian produk minuman dan segmentasi pelanggan menggunakan **Market Basket Analysis (Algoritma Apriori)** dan **K-Means Clustering dengan model RFM**.

## 📋 Fitur Utama

1. **Manajemen Data Transaksi**
   - Upload data transaksi dalam format CSV/Excel
   - Tampilkan dan kelola data transaksi
   - Hapus data transaksi

2. **Market Basket Analysis (MBA)**
   - Analisis pola asosiasi produk menggunakan algoritma Apriori
   - Parameter: minimum support dan minimum confidence
   - Visualisasi: Heatmap dan Bar Chart association rules
   - Output: Aturan asosiasi (antecedent → consequent) dengan nilai support, confidence, dan lift

3. **Segmentasi Pelanggan**
   - Model RFM (Recency, Frequency, Monetary)
   - K-Means Clustering untuk mengelompokkan pelanggan
   - Parameter: jumlah cluster (K)
   - Visualisasi: Grafik 3D cluster dan Pie Chart distribusi
   - Label cluster: Best Customers, Potential Customers, Lost Customers

4. **Rekomendasi Promosi**
   - Rekomendasi bundling produk berdasarkan MBA
   - Rekomendasi target pelanggan berdasarkan segmentasi
   - Strategi promosi per segmen pelanggan

## 🛠️ Teknologi yang Digunakan

### Backend
- **Python 3.10+**
- **Flask 2.3.3** - Web framework
- **SQLAlchemy** - ORM untuk database
- **SQLite** - Database

### Library Data Science
- **Pandas** - Manipulasi data
- **NumPy** - Komputasi numerik
- **MLxtend** - Algoritma Apriori
- **Scikit-learn** - K-Means Clustering
- **Plotly** - Visualisasi interaktif

### Frontend
- **HTML5, CSS3, JavaScript**
- **Bootstrap 5** - UI Framework
- **Bootstrap Icons** - Icon library

## 📦 Instalasi

### 1. Clone atau Download Repository
```bash
cd /home/bearman10/Downloads/revisi/sistem_rekomendasi
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

Atau install manual:
```bash
pip install Flask==2.3.3 Flask-SQLAlchemy==3.0.5 pandas==2.0.3 numpy==1.24.3 mlxtend==0.22.0 scikit-learn==1.3.0 plotly==5.16.1 Werkzeug==2.3.7 openpyxl==3.1.2
```

### 3. Jalankan Aplikasi
```bash
python app.py
```

Aplikasi akan berjalan di: **http://localhost:5000**

## 📊 Format Data Transaksi

File CSV/Excel harus memiliki kolom berikut:

### Kolom Wajib:
- `transaction_id` - ID transaksi unik
- `date` - Tanggal transaksi (format: YYYY-MM-DD HH:MM:SS)
- `customer_id` - ID pelanggan
- `product` - Nama produk

### Kolom Opsional:
- `quantity` - Jumlah produk (default: 1)
- `price` - Harga satuan (default: 0)
- `total` - Total harga (default: quantity × price)

### Contoh Data:
```csv
transaction_id,date,customer_id,product,quantity,price,total
TRX001,2025-01-15 10:30:00,CUST001,Aqua 600ml,5,3000,15000
TRX001,2025-01-15 10:30:00,CUST001,Teh Botol Sosro,3,4000,12000
TRX002,2025-01-15 14:20:00,CUST002,Aqua 600ml,2,3000,6000
```

File contoh tersedia di: `sample_data.csv`

## 🎯 Cara Penggunaan

### 1. Upload Data Transaksi
1. Buka menu **Data Transaksi**
2. Klik tombol **Pilih File** dan pilih file CSV/Excel
3. Klik **Upload**
4. Data akan otomatis disimpan ke database

### 2. Analisis Market Basket Analysis
1. Buka menu **Analisis MBA**
2. Atur parameter:
   - **Minimum Support**: 0.001 - 1 (default: 0.01)
     - Nilai kecil = menemukan pola yang jarang
     - Nilai besar = hanya pola yang sangat sering
   - **Minimum Confidence**: 0.01 - 1 (default: 0.3)
     - Persentase kemungkinan produk B dibeli jika produk A dibeli
3. Klik **Jalankan Analisis**
4. Sistem akan menampilkan:
   - Tabel association rules
   - Bar chart top 15 rules
   - Heatmap asosiasi produk

### 3. Analisis Segmentasi Pelanggan
1. Buka menu **Segmentasi**
2. Atur parameter:
   - **Jumlah Cluster (K)**: 2-10 (default: 3)
     - K=3: Best, Potential, Lost Customers
3. Klik **Jalankan Clustering**
4. Sistem akan menampilkan:
   - Statistik per cluster
   - Pie chart distribusi segmen
   - Grafik 3D interaktif (Recency, Frequency, Monetary)
   - Tabel hasil segmentasi

### 4. Lihat Rekomendasi Promosi
1. Buka menu **Rekomendasi**
2. Sistem akan menampilkan:
   - **Rekomendasi Bundling Produk**: Paket produk yang sering dibeli bersamaan
   - **Rekomendasi Target Pelanggan**: Strategi promosi per segmen
   - **Action Plan**: Langkah implementasi promosi

## 📐 Penjelasan Algoritma

### 1. Algoritma Apriori (Market Basket Analysis)

**Rumus Support:**
```
Support(A) = Jumlah transaksi yang mengandung A / Total transaksi
```

**Rumus Confidence:**
```
Confidence(A → B) = Support(A ∪ B) / Support(A)
```

**Rumus Lift:**
```
Lift(A → B) = Support(A ∪ B) / (Support(A) × Support(B))
```

**Interpretasi Lift:**
- Lift > 1: Asosiasi positif (produk cenderung dibeli bersamaan)
- Lift = 1: Tidak ada asosiasi
- Lift < 1: Asosiasi negatif

### 2. Model RFM

**Recency (R):**
```
Recency = Tanggal sekarang - Tanggal transaksi terakhir pelanggan (dalam hari)
```

**Frequency (F):**
```
Frequency = Jumlah transaksi unik pelanggan
```

**Monetary (M):**
```
Monetary = Total pembelian pelanggan (Rp)
```

### 3. K-Means Clustering

**Langkah-langkah:**
1. Normalisasi data RFM menggunakan StandardScaler
2. Inisialisasi K centroid secara random
3. Assign setiap pelanggan ke centroid terdekat
4. Update centroid berdasarkan rata-rata cluster
5. Ulangi langkah 3-4 hingga konvergen

**Formula Jarak Euclidean:**
```
Distance = √[(R₁-R₂)² + (F₁-F₂)² + (M₁-M₂)²]
```

**Labeling Cluster:**
- Score = -Recency × 0.3 + Frequency × 0.3 + Monetary × 0.4
- Cluster dengan score tertinggi = Best Customers
- Cluster dengan score terendah = Lost Customers

## 📁 Struktur Proyek

```
sistem_rekomendasi/
│
├── app.py                      # File utama Flask
├── config.py                   # Konfigurasi aplikasi
├── requirements.txt            # Dependencies
├── sample_data.csv             # Contoh data transaksi
├── README.md                   # Dokumentasi
│
├── models/                     # Model database
│   ├── __init__.py
│   └── transaksi.py            # Model Transaksi, AturanAsosiasi, SegmentasiPelanggan
│
├── controllers/                # Logic bisnis
│   ├── __init__.py
│   └── data_controller.py      # Controller untuk manajemen data
│
├── utils/                      # Fungsi pembantu
│   ├── __init__.py
│   ├── apriori.py              # Implementasi algoritma Apriori
│   ├── clustering.py           # Implementasi RFM dan K-Means
│   └── visualization.py        # Fungsi visualisasi Plotly
│
├── templates/                  # Template HTML
│   ├── base.html
│   ├── dashboard.html
│   ├── data_transaksi.html
│   ├── analisis_mba.html
│   ├── segmentasi.html
│   └── rekomendasi.html
│
└── static/                     # File statis
    ├── css/
    ├── js/
    └── uploads/                # Folder upload file
```

## 🔍 Troubleshooting

### Error: "No module named 'mlxtend'"
```bash
pip install mlxtend
```

### Error: "Tidak ada aturan yang ditemukan"
- Gunakan nilai `min_support` dan `min_confidence` yang lebih rendah
- Pastikan data transaksi cukup banyak (minimal 20-30 transaksi)

### Error: "Jumlah cluster tidak boleh melebihi jumlah data"
- Kurangi nilai K
- Pastikan data pelanggan cukup banyak

### Database Error
Hapus file `natura_boga.db` dan restart aplikasi untuk membuat database baru.

## 📝 Catatan

1. **Tidak ada fitur login** - Sistem langsung bisa diakses tanpa autentikasi
2. **Database SQLite** - Cocok untuk skala kecil-menengah (< 100,000 transaksi)
3. **Visualisasi Interaktif** - Grafik Plotly mendukung zoom, rotate, dan hover
4. **Algoritma Sederhana** - Implementasi straightforward untuk pembelajaran dan produksi

## 📧 Support

Untuk pertanyaan atau bantuan, hubungi tim PPIC PT. Natura Boga.

## 📄 License

© 2025 PT. Natura Boga. All rights reserved.
