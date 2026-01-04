from models import db
from datetime import datetime

class Transaksi(db.Model):
    __tablename__ = 'transaksi'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    customer_id = db.Column(db.String(100), nullable=False)
    product = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False, default=0.0)
    total = db.Column(db.Float, nullable=False, default=0.0)
    
    def __repr__(self):
        return f'<Transaksi {self.transaction_id} - {self.product}>'

class AturanAsosiasi(db.Model):
    __tablename__ = 'aturan_asosiasi'
    
    id = db.Column(db.Integer, primary_key=True)
    antecedents = db.Column(db.String(500), nullable=False)
    consequents = db.Column(db.String(500), nullable=False)
    support = db.Column(db.Float, nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    lift = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Rule {self.antecedents} => {self.consequents}>'

class SegmentasiPelanggan(db.Model):
    __tablename__ = 'segmentasi_pelanggan'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(100), nullable=False)
    recency = db.Column(db.Integer, nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    monetary = db.Column(db.Float, nullable=False)
    cluster = db.Column(db.Integer, nullable=False)
    cluster_label = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Segmentasi {self.customer_id} - {self.cluster_label}>'
