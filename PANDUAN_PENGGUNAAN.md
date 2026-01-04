# 📘 PANDUAN PENGGUNAAN SISTEM REKOMENDASI PROMOSI

## PT. NATURA BOGA

---

## 🚀 CARA MENJALANKAN APLIKASI

### **Metode 1: Menggunakan Script (RECOMMENDED)**

```bash
cd /home/bearman10/Downloads/revisi/sistem_rekomendasi
./run.sh
```

### **Metode 2: Manual**

```bash
cd /home/bearman10/Downloads/revisi/sistem_rekomendasi
source venv/bin/activate
python app.py
```

Setelah aplikasi berjalan, buka browser dan akses:
**http://localhost:5000**

---

## 📋 LANGKAH-LANGKAH PENGGUNAAN

### **STEP 1: Upload Data Transaksi**

1. Klik menu **"Data Transaksi"** di navigation bar
2. Klik tombol **"Pilih File"**
3. Pilih file CSV atau Excel dari komputer Anda
   - File contoh: `sample_data.csv` sudah tersedia di folder proyek
4. Klik **"Upload"**
5. Tunggu hingga muncul pesan sukses
6. Data akan otomatis ditampilkan dalam tabel

**Format File yang Dibutuhkan:**
```csv
transaction_id,date,customer_id,product,quantity,price,total
TRX001,2025-01-15 10:30:00,CUST001,Aqua 600ml,5,3000,15000
TRX001,2025-01-15 10:30:00,CUST001,Teh Botol Sosro,3,4000,12000
```

**Kolom Wajib:**
- `transaction_id` → ID transaksi
- `date` → Tanggal (format: YYYY-MM-DD HH:MM:SS)
- `customer_id` → ID pelanggan
- `product` → Nama produk

**Kolom Opsional:**
- `quantity` → Jumlah (default: 1)
- `price` → Harga (default: 0)
- `total` → Total (default: quantity × price)

---

### **STEP 2: Analisis Market Basket Analysis**

1. Klik menu **"Analisis MBA"**
2. Atur parameter:

**Minimum Support:**
- Nilai: 0.001 - 1
- Default: 0.01 (1%)
- **Penjelasan:** Persentase transaksi yang harus mengandung itemset
- **Contoh:** 0.01 = produk muncul minimal di 1% dari total transaksi
- **Tips:** Gunakan nilai rendah (0.005 - 0.01) untuk dataset kecil

**Minimum Confidence:**
- Nilai: 0.01 - 1
- Default: 0.3 (30%)
- **Penjelasan:** Persentase kemungkinan produk B dibeli jika produk A dibeli
- **Contoh:** 0.3 = 30% pelanggan yang beli produk A juga beli produk B
- **Tips:** Nilai 0.3 - 0.5 sudah cukup bagus untuk rekomendasi

3. Klik **"Jalankan Analisis"**
4. Sistem akan menampilkan:
   - Tabel association rules (antecedent → consequent)
   - Bar chart top 15 rules
   - Heatmap asosiasi produk (interaktif)

**Interpretasi Hasil:**

| Metric | Formula | Interpretasi |
|--------|---------|--------------|
| **Support** | Jumlah transaksi mengandung itemset / Total transaksi | Seberapa sering itemset muncul |
| **Confidence** | Support(A ∪ B) / Support(A) | Kemungkinan B dibeli jika A dibeli |
| **Lift** | Support(A ∪ B) / (Support(A) × Support(B)) | Kekuatan asosiasi |

**Lift Values:**
- **Lift > 1.5** → Asosiasi SANGAT KUAT ✅ (Prioritas Tinggi)
- **Lift 1.0 - 1.5** → Asosiasi LEMAH ⚠️
- **Lift < 1.0** → TIDAK ADA asosiasi ❌

---

### **STEP 3: Analisis Segmentasi Pelanggan**

1. Klik menu **"Segmentasi"**
2. Atur parameter:

**Jumlah Cluster (K):**
- Nilai: 2 - 10
- Default: 3
- **Rekomendasi:**
  - K=2: Best vs Others
  - K=3: Best vs Potential vs Lost (RECOMMENDED)
  - K=4-5: Segmentasi lebih detail
  - K>5: Hanya jika punya banyak pelanggan (>100)

3. Klik **"Jalankan Clustering"**
4. Sistem akan menampilkan:
   - Statistik per cluster
   - Pie chart distribusi segmen
   - **Grafik 3D interaktif** (bisa dirotate, zoom, hover)
   - Tabel hasil segmentasi

**Model RFM:**

| Variabel | Penjelasan | Nilai Bagus |
|----------|------------|-------------|
| **Recency** | Hari sejak transaksi terakhir | < 30 hari |
| **Frequency** | Jumlah transaksi | > 5 kali |
| **Monetary** | Total pembelian (Rp) | > Rp 1 juta |

**Label Cluster:**

🟢 **Best Customers:**
- Recency RENDAH (baru beli)
- Frequency TINGGI (sering beli)
- Monetary TINGGI (banyak belanja)
- **Strategi:** Loyalty program, VIP treatment, early access

🟡 **Potential Customers:**
- Recency SEDANG
- Frequency SEDANG
- Monetary SEDANG
- **Strategi:** Push notification, cross-selling, diskon

🔴 **Lost Customers:**
- Recency TINGGI (lama tidak beli)
- Frequency RENDAH
- Monetary RENDAH
- **Strategi:** Re-engagement campaign, comeback discount

---

### **STEP 4: Lihat Rekomendasi Promosi**

1. Klik menu **"Rekomendasi"**
2. Sistem akan menampilkan:

**A. Rekomendasi Bundling Produk**
- Top 10 pasangan produk dengan lift tertinggi
- Confidence (persentase keberhasilan)
- **Contoh Implementasi:**
  - Jika rule: "Aqua → Teh Botol" (Lift 2.5, Confidence 75%)
  - Buat promo: "Beli Aqua + Teh Botol diskon 10%"

**B. Rekomendasi Target Pelanggan**
- Daftar customer ID per segmen
- Strategi promosi untuk setiap segmen
- **Best Customers:** Reward loyalty
- **Potential Customers:** Diskon untuk upgrade
- **Lost Customers:** Comeback special

**C. Action Plan**
- Timeline implementasi promosi (6 minggu)
- Langkah-langkah eksekusi
- KPI dan metrik evaluasi

---

## 🎯 CONTOH KASUS PENGGUNAAN

### **Kasus 1: Menemukan Produk Bundling**

**Situasi:** Ingin buat paket promo produk

**Langkah:**
1. Upload data transaksi 1 bulan terakhir
2. Jalankan MBA dengan parameter:
   - Min Support: 0.01
   - Min Confidence: 0.3
3. Lihat hasil:
   - Rule: "Aqua 600ml → Teh Botol Sosro"
   - Lift: 2.3
   - Confidence: 65%
4. **Action:**
   - Buat paket "Aqua + Teh Botol" dengan diskon 10%
   - Expected: 65% pelanggan yang beli Aqua akan tertarik

---

### **Kasus 2: Menarget Pelanggan yang Tepat**

**Situasi:** Budget promosi terbatas, ingin target pelanggan efektif

**Langkah:**
1. Upload data transaksi 3-6 bulan
2. Jalankan Segmentasi dengan K=3
3. Lihat hasil:
   - Best Customers: 50 orang
   - Potential: 120 orang
   - Lost: 80 orang
4. **Action:**
   - **Best (50):** Kirim voucher eksklusif Rp 50rb (budget: Rp 2.5jt)
   - **Potential (120):** Diskon 15% next purchase (budget minimal)
   - **Lost (80):** Email re-engagement (gratis)

**ROI:** Budget efisien, fokus pada pelanggan yang paling berharga

---

### **Kasus 3: Kombinasi MBA + Segmentasi**

**Situasi:** Strategi promosi komprehensif

**Langkah:**
1. Jalankan MBA → dapat rekomendasi bundling
2. Jalankan Segmentasi → dapat target customer
3. **Kombinasi:**
   - Kirim promo bundling "Aqua + Teh Botol" HANYA ke **Best Customers**
   - Hasil: Conversion rate lebih tinggi karena targetted

---

## ⚠️ TROUBLESHOOTING

### **Problem 1: "Tidak ada aturan asosiasi yang ditemukan"**
**Solusi:**
- Kurangi nilai min_support (coba 0.005 atau 0.001)
- Kurangi nilai min_confidence (coba 0.2 atau 0.1)
- Pastikan data transaksi cukup banyak (minimal 20-30 transaksi)

### **Problem 2: "Jumlah cluster tidak boleh melebihi jumlah data"**
**Solusi:**
- Kurangi nilai K
- Upload data transaksi lebih banyak untuk dapat lebih banyak unique customer

### **Problem 3: "Data transaksi kosong"**
**Solusi:**
- Pastikan file CSV/Excel sudah diupload dengan benar
- Cek format kolom sesuai dengan requirements
- Lihat pesan error untuk detail masalah

### **Problem 4: Visualisasi tidak muncul**
**Solusi:**
- Refresh halaman browser
- Pastikan JavaScript enabled di browser
- Cek koneksi internet (Plotly memerlukan CDN)

### **Problem 5: Upload file gagal**
**Solusi:**
- Cek format file (harus CSV atau XLSX)
- Cek nama kolom (case-sensitive)
- Cek format tanggal (YYYY-MM-DD HH:MM:SS)
- Maksimal ukuran file: 16MB

---

## 📊 TIPS & BEST PRACTICES

### **1. Data Quality**
✅ **DO:**
- Upload data minimal 1 bulan (20-50 transaksi)
- Pastikan data bersih (no missing values)
- Update data secara berkala (weekly/monthly)

❌ **DON'T:**
- Upload data terlalu sedikit (<10 transaksi)
- Upload data dengan banyak error/duplikat

### **2. Parameter Tuning**
✅ **DO:**
- Mulai dengan parameter default
- Adjust bertahap berdasarkan hasil
- Dokumentasikan parameter yang berhasil

❌ **DON'T:**
- Gunakan nilai ekstrim (0.001 atau 0.999)
- Sering ganti-ganti parameter tanpa alasan

### **3. Interpretasi Hasil**
✅ **DO:**
- Focus pada rules dengan lift > 1.5
- Prioritas segmen Best Customers
- Kombinasikan insight MBA + Segmentasi

❌ **DON'T:**
- Implementasi semua rules tanpa prioritas
- Ignore segmen Lost Customers (bisa di-reactivate)

---

## 📞 SUPPORT

Untuk bantuan lebih lanjut:
- **Email:** ppic@naturaboga.com
- **Telp:** (021) 1234-5678
- **Dokumentasi:** README.md

---

**© 2025 PT. Natura Boga. All Rights Reserved.**
