import socket
import json
import hashlib
import sqlite3
import threading
from uuid import uuid4

class Server:
    def __init__(self, listen_from, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', port))
        self.sock.listen()
        self.clients = []


class DB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def auth_client(self, user_id, user_pass_hash):
        data = self.cursor.execute("SELECT * FROM `users` WHERE `id` = 1 AND `password` = :pass_hash", {"pass_hash": user_pass_hash}).fetchall()
        return data

class User:
    def __init__(self, conn, user_id=None, sended_hash=None, nick=None, token=None, authed=False):
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
                        self.user_id = data["user_id"]
                        self.sended_hash = data["user_pass"]
                        if db.auth_client(self.user_id, self.sended_hash):
                            self.token = str(uuid4())
                            self.conn.send(json.dumps({"auth": True, "token": self.token}).encode("utf-8"))
                        else:
                            self.conn.send(json.dumps({"auth": False}).encode("utf-8"))
                    else:
                        self.conn.close()
                        self.__del__()
            except json.decoder.JSONDecodeError:
                pass

            
    def __del__(self):
        pass

if __name__ == "__main__":
    try:
        server = Server("", 5001)
        db = DB("data/database")
        while True:
            conn, addr = server.sock.accept()
            server.clients.append(User(conn))
            threading.Thread(target=server.clients[-1].listen_thread).start()
            print(addr)
            print("[LOG] New client")
    except KeyboardInterrupt:
        server.sock.close()

