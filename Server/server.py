import socket
import json
import hashlib
import sqlite3
import threading
from uuid import uuid4
import os
from db import DB

class Server:
    def __init__(self, listen_from, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', port))
        self.sock.listen()
        self.clients = []



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
                            self.check_pub_key()
                        else:
                            self.conn.send(json.dumps({"auth": False}).encode("utf-8"))
                    elif data["cmd"] == 1:
                        key = data["key"]
                        with open(os.path.join("data/UserKeys", f"pub_key_u_{self.user_id}"), "w") as file:
                            file.write(key)
                    elif not self.authed:
                        self.conn.close()
                        self.__del__()
            except json.decoder.JSONDecodeError:
                pass

    def check_pub_key(self):
        if not(os.path.exists(os.path.join("data/UserKeys", f"pub_key_u_{self.user_id}"))):
            self.conn.send(json.dumps({"cmd": 1}).encode("utf-8")) # req to client

    def get_convs(self):
        pass

            
    def __del__(self):
        pass

if __name__ == "__main__":
    try:
        server = Server("", 5002)
        db = DB("data/database")
        while True:
            conn, addr = server.sock.accept()
            server.clients.append(User(conn))
            threading.Thread(target=server.clients[-1].listen_thread).start()
            print(addr)
            print("[LOG] New client")
    except KeyboardInterrupt:
        server.sock.close()

