import socket
import json
import hashlib
import os
import rsa


class Connection:
    def __init__(self, user_id, user_pass_hash, server_ip="localhost", server_port=5002, local_storage="./LocalStorage"):
        self.user_id = user_id
        self.user_pass_hash = user_pass_hash
        self.token = None
        self.authed = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.sock.connect((server_ip, server_port))
        self.local_storage = local_storage
        self.public_key_file_name = "PUB"
        self.private_key_file_name = "PRIV"
        self.pub = None
        self.priv = None


    def check_crypto_keys(self):
        path_to_keys = os.path.join(self.local_storage, "Keys")
        files_list = os.listdir(path_to_keys)
        if self.public_key_file_name in files_list and self.private_key_file_name in files_list:
            print("[LOG] Keys exists")
            self.load_keys()
        else:
            print("[LOG] Generating new pair")
            self.generate_keys()

    def generate_keys(self):
        pub, priv = rsa.newkeys(512)
        print("[LOG] Pair generated")
        print(pub)
        print(priv)
        pubKeyPem = pub.save_pkcs1().decode('utf8') 
        privKeyPem = priv.save_pkcs1().decode('utf8') 
        with open(os.path.join(self.local_storage, "Keys", self.public_key_file_name), "w") as file:
            file.write(pubKeyPem)
        with open(os.path.join(self.local_storage, "Keys", self.private_key_file_name), "w") as file:
            file.write(privKeyPem)
        print("[LOG] Keys saved")
                

    def load_keys(self):
        with open(os.path.join(self.local_storage, "Keys", self.public_key_file_name)) as file:
            publicKeyPkcs1PEM = file.read()
        with open(os.path.join(self.local_storage, "Keys", self.private_key_file_name)) as file:
            privateKeyPkcs1PEM = file.read()
        self.pub = rsa.PublicKey.load_pkcs1(publicKeyPkcs1PEM.encode('utf8')) 
        self.priv = rsa.PrivateKey.load_pkcs1(privateKeyPkcs1PEM.encode('utf8')) 
        print(self.pub)
        print(self.priv)
        

    def auth(self):
        auth_dict = {"cmd": 0, "user_id": self.user_id, "user_pass": self.user_pass_hash}
        self.sock.send(json.dumps(auth_dict).encode("utf-8")) 
        data = json.loads(self.sock.recv(1024).decode("utf-8"))
        if not data["auth"]:
            self.sock.close()
            exit(1)

    def share_pub_key(self):
        self.sock.send(json.dumps({"cmd": 1, "key": self.pub.save_pkcs1().decode('utf8')}).encode("utf-8"))


user_id = int(input("User id:"))
user_pass = input("User pass:")
user_pass_hash = hashlib.sha256(user_pass.encode('utf-8')).hexdigest()
connection = Connection(user_id, user_pass_hash)
connection.check_crypto_keys()
connection.auth()
while True:
    data = connection.sock.recv(1024)
    try:
        data = json.loads(data)
        if data["cmd"] == 1:
            connection.share_pub_key()
    except json.decoder.JSONDecodeError:
        pass
    
connection.sock.close()
