import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.connect(('localhost', 5000))
sock.send(bytes('Hello, world', encoding='UTF-8')) 
while True:
    data = sock.recv(1024) 
    print(data)

    
sock.close()
