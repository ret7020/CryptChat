import socket
import json
import hashlib
import sqlite3

class Server:
    def __init__(self, listen_from, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', port))
        self.sock.listen()
        self.clients = {}


class DB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.cursor = con.cursor()

    def auth_client(self, user_id, user_pass_hash):
        data = self.cursor.execute("SELECT * FROM `users` WHERE `id` = 1 AND `password` = :pass_hash", {"pass_hash": user_pass_hash}) # 1160130875fda0812c99c5e3f1a03516471a6370c4f97129b221938eb4763e63
        print(data)

class User:
    def __init__(self, conn, user_id, sended_hash, nick=None, token=None, authed=False):
        self.conn = conn
        self.user_id = user_id
        self.sended_hash = sended_hash
        self.nick = nick
        self.token = token
        self.authed = authed
    
    def listen_thread(self):
        while True:
            data = self.conn.recv(2048)
            data = data.decode("utf-8")
            try:
                data = json.loads(data)
                if not self.authed:
                    if data["cmd"] == 0:
                        pass
                    else:
                        self.conn.close()
                        self.__del__()

            except:
                pass
    def __del__(self):
        pass

if __name__ == "__main__":
    server = Server("", 5000)
    while True:
        conn, addr = server.accept()
        print(addr)
        print("[LOG] New client")
    
