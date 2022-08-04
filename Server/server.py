import socket


class Server:
    def __init__(self, listen_from, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', port))
        self.sock.listen()
        self.clients = {}


class DB:
    def __init__(self):
        pass

    def auth_client(self):
        pass

class Client:
    def __init__(self, conn):
        self.conn = conn

if __name__ == "__main__":
    '''server = Server("", 5000)
    while True:
        conn, addr = server.accept()
        print(addr)
        print("[LOG] New client")
    '''
