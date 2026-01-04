import os

def get_db_path():
    """Mendapatkan path database berdasarkan lingkungan"""
    if os.environ.get('VERCEL'):
        # Di lingkungan Vercel, gunakan path sementara
        return '/tmp/natura_boga.db'
    else:
        # Di lingkungan lokal, gunakan path lokal
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'natura_boga.db')

def get_upload_folder():
    """Mendapatkan folder upload berdasarkan lingkungan"""
    base_dir = os.path.abspath(os.path.dirname(__file__))
    upload_base = '/tmp' if os.environ.get('VERCEL') else base_dir
    return os.path.join(upload_base, 'uploads')

class Config:
    SECRET_KEY = 'natura-boga-secret-key-2025'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + get_db_path()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = get_upload_folder()
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
