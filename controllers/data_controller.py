"""
Controller untuk manajemen data transaksi
"""
import pandas as pd
from werkzeug.utils import secure_filename
from models import db
from models.transaksi import Transaksi
import os

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def upload_data(file, upload_folder, allowed_extensions):
    """
    Upload dan simpan data transaksi dari file CSV/Excel
    
    Args:
        file: File object dari request.files
        upload_folder: Path folder untuk upload
        allowed_extensions: Set of allowed extensions
    
    Returns:
        Dictionary dengan key 'success' atau 'error'
    """
    if not file:
        return {"error": "Tidak ada file yang dipilih"}
    
    if file.filename == '':
        return {"error": "Nama file kosong"}
    
    if not allowed_file(file.filename, allowed_extensions):
        return {"error": "Format file tidak didukung. Gunakan CSV atau Excel (.xlsx)"}
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    
    try:
        file.save(filepath)
        
        # Baca file
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(filepath)
        else:
            return {"error": "Format file tidak didukung"}
        
        # Validasi kolom yang diperlukan
        required_columns = ['transaction_id', 'date', 'customer_id', 'product']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return {"error": f"Kolom tidak lengkap. Kolom yang hilang: {', '.join(missing_columns)}"}
        
        # Tambahkan kolom default jika tidak ada
        if 'quantity' not in df.columns:
            df['quantity'] = 1
        
        if 'price' not in df.columns:
            df['price'] = 0.0
        
        if 'total' not in df.columns:
            df['total'] = df['quantity'] * df['price']
        
        # Simpan ke database
        count = 0
        for _, row in df.iterrows():
            transaksi = Transaksi(
                transaction_id=str(row['transaction_id']),
                date=pd.to_datetime(row['date']),
                customer_id=str(row['customer_id']),
                product=str(row['product']),
                quantity=int(row['quantity']),
                price=float(row['price']) if 'price' in row else 0.0,
                total=float(row['total']) if 'total' in row else 0.0
            )
            db.session.add(transaksi)
            count += 1
        
        db.session.commit()
        
        # Hapus file setelah diimport
        os.remove(filepath)
        
        return {"success": f"Berhasil mengupload {count} data transaksi"}
        
    except Exception as e:
        db.session.rollback()
        return {"error": f"Error saat mengupload file: {str(e)}"}

def get_all_transactions():
    """
    Ambil semua data transaksi dari database
    
    Returns:
        List of Transaksi objects
    """
    return Transaksi.query.all()

def get_transactions_dataframe():
    """
    Ambil data transaksi dalam format DataFrame
    
    Returns:
        pandas DataFrame
    """
    transactions = Transaksi.query.all()
    
    if not transactions:
        return pd.DataFrame()
    
    data = [{
        'id': t.id,
        'transaction_id': t.transaction_id,
        'date': t.date,
        'customer_id': t.customer_id,
        'product': t.product,
        'quantity': t.quantity,
        'price': t.price,
        'total': t.total
    } for t in transactions]
    
    return pd.DataFrame(data)

def delete_transaction(transaction_id):
    """
    Hapus transaksi berdasarkan ID
    
    Args:
        transaction_id: ID transaksi
    
    Returns:
        Dictionary dengan key 'success' atau 'error'
    """
    try:
        transaksi = Transaksi.query.get(transaction_id)
        if not transaksi:
            return {"error": "Transaksi tidak ditemukan"}
        
        db.session.delete(transaksi)
        db.session.commit()
        return {"success": "Transaksi berhasil dihapus"}
    except Exception as e:
        db.session.rollback()
        return {"error": f"Error: {str(e)}"}

def delete_all_transactions():
    """
    Hapus semua data transaksi
    
    Returns:
        Dictionary dengan key 'success' atau 'error'
    """
    try:
        count = Transaksi.query.delete()
        db.session.commit()
        return {"success": f"Berhasil menghapus {count} data transaksi"}
    except Exception as e:
        db.session.rollback()
        return {"error": f"Error: {str(e)}"}

def get_statistics():
    """
    Dapatkan statistik dasar dari data transaksi
    
    Returns:
        Dictionary dengan statistik
    """
    df = get_transactions_dataframe()
    
    if df.empty:
        return {
            'total_transactions': 0,
            'total_customers': 0,
            'total_products': 0,
            'total_revenue': 0
        }
    
    return {
        'total_transactions': df['transaction_id'].nunique(),
        'total_customers': df['customer_id'].nunique(),
        'total_products': df['product'].nunique(),
        'total_revenue': df['total'].sum()
    }
