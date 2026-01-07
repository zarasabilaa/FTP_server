import os
from pyftpdlib.authorizers import DummyAuthorizer # type: ignore
from pyftpdlib.handlers import FTPHandler # type: ignore
from pyftpdlib.servers import FTPServer # type: ignore


def start_ftp():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FTP_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", "ftp_data"))

    print("FTP ROOT:", FTP_ROOT)

    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "12345", FTP_ROOT, perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer(("127.0.0.1", 2122), handler)
    server.serve_forever()


if __name__ == "__main__":
    start_ftp()
