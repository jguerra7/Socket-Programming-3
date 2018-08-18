import socket

# TCP    127.0.0.1:51125        127.0.0.1:65432        TIME_WAIT

HOST = "127.0.0.1"  # if empty, server accepts connections on all IPv4 interfaces
PORT = 65432        # PORT -> 1 - 65535

# TCP connection handle -> socket.SOCK_STREAM
# UDP connection handle -> socket.SOCK_DGRAM
# IPv4 address family -> AF_INET
# IPv6 address family -> AF_INET6

print("Waiting for Connection Request \n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # socket.socket -> using socket without socket close()
    s.bind((HOST, PORT))    # HOST -> Network interface, PORT -> PORT
    # IPv4 -> (host, port), IPv6 -> (host, port, flowinfo, scopeid)
    s.listen()  # default backlog value is used - number of connections to accept
    conn, addr = s.accept()
    # print(f'Connection established with: {conn}, {addr}')
    with conn:
        print('Connected using', addr)
        while True:
            data = conn.recv(1024)
            if not data:    # if conn.recv returns an empty bytes object -> b''
                break       # close socket
            conn.sendall(data)