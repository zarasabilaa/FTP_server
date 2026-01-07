import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FTP_HOST = "127.0.0.1"
FTP_PORT = 2122

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
