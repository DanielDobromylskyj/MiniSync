import socket
import rsa
import hashlib

class App:
    def __init__(self, password, host, port=5234):
        self.serverPublicKey = None
        self.privkey = None
        self.pubkey = None

        # I understand that sha256 is not very good for password security, the server ues bcrypt.
        self.passwordHash = hashlib.sha256(password.encode(), usedforsecurity=True).digest()
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def rsaExchange(self):
        self.pubkey, self.privkey = rsa.newkeys(1024)

        self.sock.send(b"Ready")
        self.sock.recv(1024)

        self.serverPublicKey = rsa.PublicKey.load_pkcs1(self.sock.recv(2048), "PEM")
        self.sock.send(self.pubkey.save_pkcs1("PEM"))
        self.sock.recv(1024)

    def run(self):
        self.sock.connect((self.host, self.port))
        self.rsaExchange()

        self.sock.send(self.passwordHash)
        self.sock.recv(1024)


if __name__ == "__main__":
    app = App(password="myPassword", host="localhost")
    app.run()
