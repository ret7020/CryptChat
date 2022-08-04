import socket
import json
import hashlib

user_id = int(input("User id:"))
user_pass = input("User pass:")
user_pass_hash = hashlib.sha256(user_pass.encode('utf-8')).hexdigest()
print(user_pass_hash)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.connect(('localhost', 5000))


# Auth
auth_dict = {"cmd": 0, "user_id": 0, "user_pass": user_pass_hash}
sock.send(json.dums(auth_dict).encode("utf-8")) 
while True:
    data = sock.recv(1024)
    


sock.close()
