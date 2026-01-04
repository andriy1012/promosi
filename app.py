"""
Sistem Rekomendasi Promosi PT. Natura Boga
Market Basket Analysis + Segmentasi Pelanggan (RFM + K-Means)
"""
from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db
from models.transaksi import Transaksi, AturanAsosiasi, SegmentasiPelanggan
from controllers.data_controller import (
    upload_data, get_all_transactions, get_transactions_dataframe,
    delete_transaction, delete_all_transactions, get_statistics
)
from utils.apriori import run_apriori, format_itemset
from utils.clustering import calculate_rfm, kmeans_clustering
from utils.visualization import (
    create_association_heatmap, create_simple_bar_chart,
    create_3d_cluster_plot, create_cluster_summary_chart
)
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Create upload folder if not exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """Halaman dashboard"""
    stats = get_statistics()
    return render_template('dashboard.html', stats=stats)

@app.route('/data_transaksi')
def data_transaksi():
    """Halaman data transaksi"""
    transactions = get_all_transactions()
    stats = get_statistics()
    return render_template('data_transaksi.html', transactions=transactions, stats=stats)

@app.route('/upload', methods=['POST'])
def upload():
    """Upload file data transaksi"""
    if 'file' not in request.files:
        flash('Tidak ada file yang diupload', 'error')
        return redirect(url_for('data_transaksi'))
    
    file = request.files['file']
    result = upload_data(file, app.config['UPLOAD_FOLDER'], app.config['ALLOWED_EXTENSIONS'])
    
    if 'error' in result:
        flash(result['error'], 'error')
    else:
        flash(result['success'], 'success')
    
    return redirect(url_for('data_transaksi'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    """Hapus satu transaksi"""
    result = delete_transaction(id)
    
    if 'error' in result:
        flash(result['error'], 'error')
    else:
        flash(result['success'], 'success')
    
    return redirect(url_for('data_transaksi'))

@app.route('/delete_all', methods=['POST'])
def delete_all():
    """Hapus semua transaksi"""
    result = delete_all_transactions()
    
    # Hapus juga hasil analisis
    AturanAsosiasi.query.delete()
    SegmentasiPelanggan.query.delete()
    db.session.commit()
    
    if 'error' in result:
        flash(result['error'], 'error')
    else:
        flash(result['success'], 'success')
    
    return redirect(url_for('data_transaksi'))

@app.route('/analisis_mba', methods=['GET', 'POST'])
def analisis_mba():
    """Halaman analisis Market Basket Analysis"""
    if request.method == 'POST':
        try:
            min_support = float(request.form.get('min_support', 0.01))
            min_confidence = float(request.form.get('min_confidence', 0.3))
            
            # Ambil data transaksi
            df = get_transactions_dataframe()
            
            if df.empty:
                flash('Data transaksi kosong. Silakan upload data terlebih dahulu.', 'error')
                return redirect(url_for('data_transaksi'))
            
            # Group produk per transaksi
            transactions = df.groupby('transaction_id')['product'].apply(list).values.tolist()
            
            # Jalankan Apriori
            rules = run_apriori(transactions, min_support, min_confidence)
            
            if rules.empty:
                flash(f'Tidak ada aturan asosiasi yang ditemukan dengan parameter min_support={min_support} dan min_confidence={min_confidence}. Coba gunakan nilai yang lebih rendah.', 'warning')
                return render_template('analisis_mba.html', rules=None, heatmap=None, bar_chart=None)
            
            # Hapus rules lama
            AturanAsosiasi.query.delete()
            
            # Simpan rules ke database
            for _, row in rules.iterrows():
                rule = AturanAsosiasi(
                    antecedents=format_itemset(row['antecedents']),
                    consequents=format_itemset(row['consequents']),
                    support=float(row['support']),
                    confidence=float(row['confidence']),
                    lift=float(row['lift'])
                )
                db.session.add(rule)
            
            db.session.commit()
            
            # Buat visualisasi
            heatmap = create_association_heatmap(rules)
            bar_chart = create_simple_bar_chart(rules)
            
            # Format rules untuk tampilan
            rules_display = []
            for _, row in rules.head(20).iterrows():
                rules_display.append({
                    'antecedents': format_itemset(row['antecedents']),
                    'consequents': format_itemset(row['consequents']),
                    'support': round(row['support'], 4),
                    'confidence': round(row['confidence'], 4),
                    'lift': round(row['lift'], 4)
                })
            
            flash(f'Analisis berhasil! Ditemukan {len(rules)} aturan asosiasi.', 'success')
            
            return render_template('analisis_mba.html', 
                                 rules=rules_display, 
                                 heatmap=heatmap,
                                 bar_chart=bar_chart,
                                 total_rules=len(rules))
            
        except Exception as e:
            flash(f'Error saat analisis: {str(e)}', 'error')
            return render_template('analisis_mba.html', rules=None, heatmap=None, bar_chart=None)
    
    return render_template('analisis_mba.html', rules=None, heatmap=None, bar_chart=None)

@app.route('/segmentasi', methods=['GET', 'POST'])
def segmentasi():
    """Halaman analisis segmentasi pelanggan"""
    if request.method == 'POST':
        try:
            n_clusters = int(request.form.get('n_clusters', 3))
            
            # Validasi K
            if n_clusters < 2:
                flash('Jumlah cluster minimal adalah 2', 'error')
                return render_template('segmentasi.html', rfm_data=None, plot_3d=None, pie_chart=None)
            
            # Ambil data transaksi
            df = get_transactions_dataframe()
            
            if df.empty:
                flash('Data transaksi kosong. Silakan upload data terlebih dahulu.', 'error')
                return redirect(url_for('data_transaksi'))
            
            # Validasi jumlah customer
            n_customers = df['customer_id'].nunique()
            if n_clusters > n_customers:
                flash(f'Jumlah cluster ({n_clusters}) tidak boleh lebih dari jumlah pelanggan ({n_customers})', 'error')
                return render_template('segmentasi.html', rfm_data=None, plot_3d=None, pie_chart=None)
            
            # Hitung RFM
            rfm_df = calculate_rfm(df)
            
            # K-Means clustering
            rfm_clustered, kmeans_model = kmeans_clustering(rfm_df, n_clusters)
            
            # Hapus segmentasi lama
            SegmentasiPelanggan.query.delete()
            
            # Simpan hasil segmentasi ke database
            for _, row in rfm_clustered.iterrows():
                segmentasi = SegmentasiPelanggan(
                    customer_id=row['customer_id'],
                    recency=int(row['Recency']),
                    frequency=int(row['Frequency']),
                    monetary=float(row['Monetary']),
                    cluster=int(row['Cluster']),
                    cluster_label=row['Cluster_Label']
                )
                db.session.add(segmentasi)
            
            db.session.commit()
            
            # Buat visualisasi
            plot_3d = create_3d_cluster_plot(rfm_clustered)
            pie_chart = create_cluster_summary_chart(rfm_clustered)
            
            # Urutkan data berdasarkan label kategori pelanggan
            # Best Customers -> Potential Customers -> Lost Customers
            label_order = {'Best Customers': 0, 'Potential Customers': 1, 'Lost Customers': 2}
            rfm_clustered['label_sort'] = rfm_clustered['Cluster_Label'].map(label_order)
            rfm_clustered_sorted = rfm_clustered.sort_values(['label_sort', 'customer_id'])
            rfm_clustered_sorted = rfm_clustered_sorted.drop('label_sort', axis=1)

            # Format data untuk tampilan
            rfm_display = rfm_clustered_sorted.to_dict('records')
            
            # Statistik per cluster
            cluster_stats = rfm_clustered.groupby('Cluster_Label').agg({
                'Recency': 'mean',
                'Frequency': 'mean',
                'Monetary': 'mean',
                'customer_id': 'count'
            }).round(2).to_dict('index')
            
            flash(f'Analisis berhasil! Pelanggan dikelompokkan menjadi {n_clusters} cluster.', 'success')
            
            return render_template('segmentasi.html', 
                                 rfm_data=rfm_display,
                                 plot_3d=plot_3d,
                                 pie_chart=pie_chart,
                                 cluster_stats=cluster_stats,
                                 total_customers=len(rfm_clustered))
            
        except Exception as e:
            flash(f'Error saat analisis: {str(e)}', 'error')
            return render_template('segmentasi.html', rfm_data=None, plot_3d=None, pie_chart=None)
    
    return render_template('segmentasi.html', rfm_data=None, plot_3d=None, pie_chart=None)

@app.route('/rekomendasi')
def rekomendasi():
    """Halaman rekomendasi promosi"""
    # Ambil association rules
    rules = AturanAsosiasi.query.order_by(AturanAsosiasi.lift.desc()).limit(10).all()
    
    # Ambil segmentasi pelanggan
    segmentasi = SegmentasiPelanggan.query.all()
    
    # Generate rekomendasi bundling
    bundling_recommendations = []
    for rule in rules:
        bundling_recommendations.append({
            'produk_utama': rule.antecedents,
            'produk_bundling': rule.consequents,
            'lift': round(rule.lift, 2),
            'confidence': round(rule.confidence * 100, 1)
        })
    
    # Generate rekomendasi target pelanggan
    # Urutkan pelanggan berdasarkan ID dalam setiap kategori
    best_customers = sorted([s for s in segmentasi if s.cluster_label == 'Best Customers'], key=lambda x: x.customer_id)
    potential_customers = sorted([s for s in segmentasi if s.cluster_label == 'Potential Customers'], key=lambda x: x.customer_id)
    lost_customers = sorted([s for s in segmentasi if s.cluster_label == 'Lost Customers'], key=lambda x: x.customer_id)
    
    return render_template('rekomendasi.html',
                         bundling_recommendations=bundling_recommendations,
                         best_customers=best_customers[:10],
                         potential_customers=potential_customers[:10],
                         lost_customers=lost_customers[:10],
                         total_best=len(best_customers),
                         total_potential=len(potential_customers),
                         total_lost=len(lost_customers))

# Hanya dijalankan saat di lokal, tidak untuk production di Vercel
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5006)))
