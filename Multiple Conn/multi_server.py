import selectors, socket
import types

sel = selectors.DefaultSelector()

host = '127.0.0.1'
port = 65432

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))

lsock.listen()
print("Listening on",(host, port))     # configure socket in non-blocking mode for multiple conns
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)    # register socket to be monitored with select()


def accept_wrapper(sock):
    conn, addr = sock.accept()
    print('Connected using', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print("Closing connection to: ", data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print("Sending ", repr(data.outb), " to ", data.addr, " using ", data.inb)
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

while True:
    events = sel.select(timeout=None)   # blocking until sockets are ready
    for key, mask in events:
        if key.data is None:    # if True -> from listening socket and accept() connection
            accept_wrapper(key.fileobj)
        else:                   # client socket already accepted
            service_connection(key, mask)


