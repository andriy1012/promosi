"""
Modul visualisasi menggunakan Plotly
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.apriori import format_itemset

def create_association_heatmap(rules_df):
    """
    Membuat heatmap untuk visualisasi association rules
    
    Args:
        rules_df: DataFrame hasil dari run_apriori
    
    Returns:
        HTML string dari Plotly heatmap
    """
    if rules_df.empty:
        return "<p>Tidak ada data untuk divisualisasikan</p>"
    
    # Convert frozenset to string
    rules_df = rules_df.copy()
    rules_df['antecedents_str'] = rules_df['antecedents'].apply(format_itemset)
    rules_df['consequents_str'] = rules_df['consequents'].apply(format_itemset)
    
    # Ambil top 20 rules untuk visualisasi
    rules_top = rules_df.head(20)
    
    # Create pivot table for heatmap
    try:
        pivot = rules_top.pivot_table(
            values='lift', 
            index='antecedents_str', 
            columns='consequents_str', 
            aggfunc='mean',
            fill_value=0
        )
    except:
        # Jika pivot gagal, buat heatmap sederhana
        pivot = pd.DataFrame({
            'lift': rules_top['lift'].values,
            'antecedents': rules_top['antecedents_str'].values,
            'consequents': rules_top['consequents_str'].values
        })
        return create_simple_bar_chart(rules_top)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale='RdYlGn',
        text=pivot.values,
        texttemplate='%{text:.2f}',
        textfont={"size": 10},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='Heatmap Asosiasi Produk (Nilai Lift)',
        xaxis_title='Consequent (Produk yang Direkomendasikan)',
        yaxis_title='Antecedent (Produk Awal)',
        height=600,
        font=dict(size=11)
    )
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def create_simple_bar_chart(rules_df):
    """
    Membuat bar chart sederhana untuk association rules
    
    Args:
        rules_df: DataFrame hasil dari run_apriori
    
    Returns:
        HTML string dari Plotly bar chart
    """
    if rules_df.empty:
        return "<p>Tidak ada data untuk divisualisasikan</p>"
    
    # Ambil top 15 rules
    rules_top = rules_df.head(15).copy()
    rules_top['rule'] = rules_top['antecedents'].apply(format_itemset) + ' → ' + rules_top['consequents'].apply(format_itemset)
    
    # Create bar chart untuk lift
    fig = go.Figure(data=[
        go.Bar(
            x=rules_top['lift'],
            y=rules_top['rule'],
            orientation='h',
            marker=dict(
                color=rules_top['lift'],
                colorscale='RdYlGn',
                showscale=True
            ),
            text=rules_top['lift'].round(2),
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title='Top 15 Association Rules (berdasarkan Lift)',
        xaxis_title='Lift',
        yaxis_title='Aturan Asosiasi',
        height=600,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def create_3d_cluster_plot(rfm_df):
    """
    Membuat grafik 3D untuk visualisasi cluster pelanggan
    
    Args:
        rfm_df: DataFrame dengan kolom ['customer_id', 'Recency', 'Frequency', 'Monetary', 'Cluster', 'Cluster_Label']
    
    Returns:
        HTML string dari Plotly 3D scatter plot
    """
    if rfm_df.empty:
        return "<p>Tidak ada data untuk divisualisasikan</p>"
    
    fig = px.scatter_3d(
        rfm_df, 
        x='Recency', 
        y='Frequency', 
        z='Monetary',
        color='Cluster_Label',
        hover_data=['customer_id'],
        title='Visualisasi 3D Segmentasi Pelanggan (RFM + K-Means)',
        labels={
            'Recency': 'Recency (hari)',
            'Frequency': 'Frequency (transaksi)',
            'Monetary': 'Monetary (Rp)',
            'Cluster_Label': 'Segmen'
        },
        color_discrete_map={
            'Best Customers': '#00CC96',
            'Potential Customers': '#FFA15A',
            'Lost Customers': '#EF553B'
        }
    )
    
    fig.update_traces(marker=dict(size=6))
    
    fig.update_layout(
        scene=dict(
            xaxis_title='Recency (hari sejak transaksi terakhir)',
            yaxis_title='Frequency (jumlah transaksi)',
            zaxis_title='Monetary (total pembelian Rp)'
        ),
        height=700
    )
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def create_cluster_summary_chart(rfm_df):
    """
    Membuat pie chart untuk distribusi cluster
    
    Args:
        rfm_df: DataFrame dengan kolom Cluster_Label
    
    Returns:
        HTML string dari Plotly pie chart
    """
    if rfm_df.empty:
        return "<p>Tidak ada data untuk divisualisasikan</p>"
    
    cluster_counts = rfm_df['Cluster_Label'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=cluster_counts.index,
        values=cluster_counts.values,
        marker=dict(
            colors=['#00CC96', '#FFA15A', '#EF553B']
        ),
        textinfo='label+percent',
        textfont_size=14
    )])
    
    fig.update_layout(
        title='Distribusi Segmen Pelanggan',
        height=400
    )
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn')
