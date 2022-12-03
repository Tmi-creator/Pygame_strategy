import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
while True:
    try:
        sock.connect(('45.80.45.18', 9999))
    except:
        print(11111111)

sock.connect(('45.80.45.18', 9999))
while True:
    sock.send('hmmm'.encode())
    data = sock.recv(2**20)
    data = data.decode()
    print(data)