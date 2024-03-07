import socket
import rsa
import bcrypt

# todo List todo - Make it check to see if a ip is spamming incorrect passwords,
#  if so, block it for [(attempts**2) * 60]s when attempts > 3


class App:
    def __init__(self, passwordFile, host, port=5234):
        self.clientPublicKey = None
        self.privkey = None
        self.pubkey = None

        self.passwordFile = passwordFile
        with open(self.passwordFile, "rb") as f:
            self.hashedPassword = f.read()


        self.addr = None
        self.conn = None

        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def rsaExchange(self):
        self.pubkey, self.privkey = rsa.newkeys(1024)

        self.conn.send(b"Ready")
        self.conn.recv(1024)

        self.conn.send(self.pubkey.save_pkcs1("PEM"))
        self.clientPublicKey = rsa.PublicKey.load_pkcs1(self.conn.recv(2048), "PEM")
        self.conn.send(b"Done")

    def run(self, setPassword=False):
        self.sock.bind((self.host, self.port))
        self.sock.listen()

        # create secure connection
        self.conn, self.addr = self.sock.accept()
        self.rsaExchange()

        # validate user with password
        pswrd = self.conn.recv(1024)

        if setPassword:
            self.hashedPassword = bcrypt.hashpw(pswrd, bcrypt.gensalt())
            with open(self.passwordFile, "wb") as f:
                f.write(self.hashedPassword)

        if not bcrypt.checkpw(pswrd, self.hashedPassword):
            raise Exception("Wrong password")

        self.conn.send(b"Password Excepted")

        while self.conn:
            command = self.conn.recv(1024)






if __name__ == "__main__":
    app = App("clientPassword.txt", "localhost")
    app.run()
