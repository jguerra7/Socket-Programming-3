import socket

# TCP    127.0.0.1:51125        127.0.0.1:65432        TIME_WAIT

HOST = '127.0.0.1'
PORT = 65432

print(f"Using Host:{HOST} at Port:{PORT}\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # send() -> needs to be called as many times data need to be sent, so use sendall()
    s.sendall(b'Hello World')   # seding byte-like object and not string
    data = s.recv(1024)     # read server reply and print

print('Data received: ', repr(data))