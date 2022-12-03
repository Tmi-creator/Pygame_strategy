import socket
import time

# cmd = "Gen_Ya.1.cpp"
# subprocess.call(["g++", cmd])
# subprocess.call("./a.out")

# cmd1 = "smooth2.cpp"
# subprocess.call(["g++", cmd1])
# subprocess.call("./a.out")

f = open('input.txt', 'r+')
main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind(('localhost', 9999))
main_socket.setblocking(False)
main_socket.listen(10)
print('socket works')
players_sockets = []
players_addr = []
running = True

mapa = []
for i in range(40):
    a = str(f.readline())  # короче это карта с местностью и зданием
    b = []
    for k in range(40):
        b.append(a[k])
    mapa.append(b)

map_ = []
for i in range(40):  # а вот это фигня с границами
    a = [0] * 40
    map_.append(a)

s = ''
for i in range(40):
    for j in range(40):
        s += mapa[i][j]
    s += '\n'
turn = 0
f.close()
cities1 = []
cities2 = []

while running:
    try:
        new_socket, addr = main_socket.accept()
        print('add', addr)
        new_socket.setblocking(False)
        players_sockets.append(new_socket)
        players_addr.append(addr)
        new_socket.send(s.encode())
    except:
        pass

    data = 0
    try:
        data = players_sockets[turn % 2].recv(2 ** 20)
        data = data.decode()
        print(data)
        if data == 'give map':
            for y, x in cities1:
                for i in range(5):
                    for j in range(5):
                        try:
                            if map_[x - 2 + i][y - 2 + j] == '0':
                                map_[x - 2 + i][y - 2 + j] = 2
                        except:
                            pass
            for y, x in cities2:
                for i in range(5):
                    for j in range(5):
                        try:
                            if map_[x - 2 + i][y - 2 + j] == '0':
                                map_[x - 2 + i][y - 2 + j] = 1
                        except:
                            pass

            s = ''
            for i in range(40):
                for j in range(40):
                    s += mapa[i][j]
                s += '\n'
            for i in range(40):
                for j in range(40):
                    s += str(map_[i][j])
                s += '\n'

            players_sockets[turn % 2].send(s.encode())
            continue
        print(players_sockets[turn % 2])
        command = data.split()
        if command[0] == 'place':
            turn += 1
            command[1], command[2] = int(command[2]), int(command[1])
            if command[3] == 'capital' and turn < 3 and mapa[command[1]][command[2]] != '0':
                mapa[command[1]][command[2]] = 'd'

                if turn % 2 == 0:
                    cities1.append([command[1], command[2]])
                else:
                    cities2.append([command[1], command[2]])
            elif command[3] == 'city':
                if map_[command[1]][command[2]] == str(turn % 2 + 1):
                    mapa[command[1]][command[2]] = ';'
                    if turn % 2 == 0:
                        cities1.append([command[1], command[2]])
                    else:
                        cities2.append([command[1], command[2]])
            elif command[3] == 'wall':
                if map_[command[1]][command[2]] == str(turn % 2 + 1):
                    mapa[command[1]][command[2]] = '<'
            elif command[3] == 'tower':
                abc = mapa[command[1]][command[2] + 1] == '<' + mapa[command[1] - 1][command[2]] == '<' + \
                      mapa[command[1] + 1][command[2]] == '<' + mapa[command[1]][command[2] - 1] == '<'
                if abc > 1:
                    if map_[command[1]][command[2]] == str(turn % 2 + 1):
                        mapa[command[1]][command[2]] = 'B'
            # players_sockets[turn % 2].send(command[3] + 'completed'.encode())

        print(turn, players_addr[(turn - 1) % 2])
    except:
        time.sleep(0.1)
        continue

    # for sock in players_sockets:
    #     try:
    #         data = sock.recv(2**20)
    #         data = data.decode()
    #         print('get', data)
    #     except:
    #         pass
    for y, x in cities1:
        for i in range(5):
            for j in range(5):
                try:
                    if map_[x - 2 + i][y - 2 + j] == '0':
                        map_[x - 2 + i][y - 2 + j] = 2
                except:
                    pass
    for y, x in cities2:
        for i in range(5):
            for j in range(5):
                try:
                    if map_[x - 2 + i][y - 2 + j] == '0':
                        map_[x - 2 + i][y - 2 + j] = 1
                except:
                    pass

    s = ''
    for i in range(40):
        for j in range(40):
            s += mapa[i][j]
        s += '\n'
    for i in range(40):
        for j in range(40):
            s += str(map_[i][j])
        s += '\n'

    for sock in players_sockets:
        try:
            sock.send(s.encode())
        except:
            players_sockets.remove(sock)
            sock.close()
            print('disconnected', sock)
    time.sleep(0.1)

