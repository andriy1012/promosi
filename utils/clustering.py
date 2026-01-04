"""
Implementasi sederhana RFM dan K-Means Clustering
"""
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
from datetime import datetime

def calculate_rfm(transactions_df, current_date=None):
    """
    Menghitung nilai RFM untuk setiap pelanggan
    
    Args:
        transactions_df: DataFrame dengan kolom ['customer_id', 'date', 'total']
        current_date: Tanggal referensi untuk hitung recency (default: today)
    
    Returns:
        DataFrame dengan kolom ['customer_id', 'Recency', 'Frequency', 'Monetary']
    """
    if current_date is None:
        current_date = datetime.now()
    
    # Convert date column to datetime jika belum
    transactions_df['date'] = pd.to_datetime(transactions_df['date'])
    
    # Hitung RFM
    rfm = transactions_df.groupby('customer_id').agg({
        'date': lambda x: (current_date - x.max()).days,  # Recency: hari sejak transaksi terakhir
        'transaction_id': 'nunique',                       # Frequency: jumlah transaksi unik
        'total': 'sum'                                     # Monetary: total pembelian
    })
    
    # Rename columns
    rfm.columns = ['Recency', 'Frequency', 'Monetary']
    
    # Reset index untuk customer_id jadi kolom
    rfm = rfm.reset_index()
    
    return rfm

def kmeans_clustering(rfm_df, n_clusters=3):
    """
    Melakukan K-Means clustering pada data RFM
    
    Args:
        rfm_df: DataFrame dengan kolom ['customer_id', 'Recency', 'Frequency', 'Monetary']
        n_clusters: Jumlah cluster (default 3)
    
    Returns:
        Tuple (rfm_clustered_df, kmeans_model)
        - rfm_clustered_df: DataFrame dengan tambahan kolom 'Cluster' dan 'Cluster_Label'
        - kmeans_model: Model K-Means yang sudah difit
    """
    # Copy dataframe
    rfm_result = rfm_df.copy()
    
    # Ambil hanya kolom RFM untuk clustering
    rfm_values = rfm_df[['Recency', 'Frequency', 'Monetary']].values
    
    # Step 1: Normalisasi data menggunakan StandardScaler
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm_values)
    
    # Step 2: K-Means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(rfm_scaled)
    
    # Step 3: Tambahkan cluster ke dataframe
    rfm_result['Cluster'] = clusters
    
    # Step 4: Label cluster berdasarkan karakteristik RFM
    cluster_labels = assign_cluster_labels(rfm_result, n_clusters)
    rfm_result['Cluster_Label'] = rfm_result['Cluster'].map(cluster_labels)
    
    return rfm_result, kmeans

def assign_cluster_labels(rfm_df, n_clusters):
    """
    Assign label untuk setiap cluster berdasarkan karakteristik RFM
    
    Logic:
    - Recency rendah (baru beli) = bagus
    - Frequency tinggi (sering beli) = bagus
    - Monetary tinggi (banyak belanja) = bagus
    
    Args:
        rfm_df: DataFrame with Cluster column
        n_clusters: Number of clusters
    
    Returns:
        Dictionary mapping cluster number to label
    """
    # Hitung rata-rata RFM per cluster
    cluster_means = rfm_df.groupby('Cluster')[['Recency', 'Frequency', 'Monetary']].mean()
    
    # Hitung score untuk setiap cluster
    # Score tinggi = pelanggan bagus
    # Recency: lower is better, jadi dikali -1
    # Frequency: higher is better
    # Monetary: higher is better
    cluster_means['Score'] = (
        -cluster_means['Recency'] * 0.3 +  # Weight 30%
        cluster_means['Frequency'] * 0.3 + # Weight 30%
        cluster_means['Monetary'] * 0.4    # Weight 40%
    )
    
    # Sort by score descending
    cluster_means = cluster_means.sort_values('Score', ascending=False)
    
    # Assign labels
    labels = {}
    cluster_order = cluster_means.index.tolist()
    
    if n_clusters == 3:
        labels[cluster_order[0]] = 'Best Customers'
        labels[cluster_order[1]] = 'Potential Customers'
        labels[cluster_order[2]] = 'Lost Customers'
    elif n_clusters == 2:
        labels[cluster_order[0]] = 'Best Customers'
        labels[cluster_order[1]] = 'Potential Customers'
    else:
        # Untuk n_clusters lainnya, distribusikan label
        for i, cluster in enumerate(cluster_order):
            if i < n_clusters // 3:
                labels[cluster] = 'Best Customers'
            elif i < 2 * n_clusters // 3:
                labels[cluster] = 'Potential Customers'
            else:
                labels[cluster] = 'Lost Customers'
    
    return labels
