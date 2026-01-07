from ftplib import FTP
from app.config import FTP_HOST, FTP_PORT


class FTPController:
    def __init__(self):
        self.ftp = FTP()

    def login(self, user, password):
        self.ftp.connect(FTP_HOST, FTP_PORT, timeout=5)
        self.ftp.login(user, password)

    def pwd(self):
        return self.ftp.pwd()

    def list_items(self):
        items = []
        names = self.ftp.nlst()

        for name in names:
            try:
                self.ftp.cwd(name)
                self.ftp.cwd("..")
                items.append({"name": name, "type": "dir"})
            except:
                items.append({"name": name, "type": "file"})
        return items

    def cwd(self, folder):
        self.ftp.cwd(folder)

    def home(self, home_dir):
        self.ftp.cwd(home_dir)

    def upload(self, local_path, filename):
        with open(local_path, "rb") as f:
            self.ftp.storbinary(f"STOR {filename}", f)

    def download(self, filename, local_path):
        with open(local_path, "wb") as f:
            self.ftp.retrbinary(f"RETR {filename}", f.write)

    def delete(self, filename):
        self.ftp.delete(filename)

    def close(self):
        self.ftp.quit()
