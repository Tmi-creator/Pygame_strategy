import socket
import time

from oop import *

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
a = ['0'] * 40
map_ = [a] * 40
mapa = []
for i in range(40):
    a = str(f.readline())  # короче это карта с местностью и зданием
    b = []
    for k in range(40):
        b.append(a[k])
    mapa.append(b)

s = ''
for i in range(40):
    for j in range(40):
        s += mapa[i][j]
    s += '\n'
turn = 0
turn1 = 0
f.close()
# ниже куча списков и словарей для хранения всякой штуки
capital1 = []  # A
capital2 = []
cities1 = []  # B
cities2 = []
explorers1 = []  # C
explorers2 = []
artilleries1 = []  # D
artilleries2 = []
cruisers1 = []  # E
cruisers2 = []
sawmills1 = []  # F
sawmills2 = []
farms1 = []  # G
farms2 = []
fish_farms1 = []  # H
fish_farms2 = []
stone_mines1 = []  # I
stone_mines2 = []
metal_mines1 = []  # J
metal_mines2 = []
plat_mines1 = []  # K
plat_mines2 = []
super_mines1 = []  # L
super_mines2 = []
shipyards1 = []  # M
shipyards2 = []
towers1 = []  # N
towers2 = []
superlist1 = [capital1, cities1, explorers1, artilleries1, cruisers1, sawmills1, farms1, fish_farms1,
              stone_mines1, metal_mines1, plat_mines1, super_mines1, shipyards1, towers1]
superlist2 = [capital2, cities2, explorers2, artilleries2, cruisers2, sawmills2, farms2, fish_farms2,
              stone_mines2, metal_mines2, plat_mines2, super_mines2, shipyards2, towers2]

ultralist = [superlist1, superlist2]

superdict = {  # for i in range(len(superdict[command[3]].cost)):
    'city': [100, 100],  # superdict[command[3]].cost[i] <= resources2[command[3]].cost[i]
    'sawmill': [50, 75],  # superdict2[command[3]].append(superdict4[command[3]](command[1], command[2]))
    'farm': [150, 50],
    "fish_farm": [50, 75],
    "stone_mine": [125, 75],
    "metal_mine": [200, 200],
    "plat_mine": [200, 300],
    "super_mine": [200, 250],
    "shipyard": [150, 350],
    "tower": [150, 150],
    'explorer': [200, 250, 0],
    'artillery': [0, 350, 200],
    'cruiser': [0, 150, 100]
}

superdict1 = {
    'city': cities1,
    'sawmill': sawmills1,
    'farm': farms1,
    "fish_farm": fish_farms1,
    "stone_mine": stone_mines1,
    "metal_mine": metal_mines1,
    "plat_mine": plat_mines1,
    "super_mine": super_mines1,
    "shipyard": shipyards1,
    "tower": towers1
}

superdict2 = {
    'city': cities2,
    'sawmill': sawmills2,
    'farm': farms2,
    "fish_farm": fish_farms2,
    "stone_mine": stone_mines2,
    "metal_mine": metal_mines2,
    "plat_mine": plat_mines2,
    "super_mine": super_mines2,
    "shipyard": shipyards2,
    "tower": towers2
}

superdict11 = {
    'artillery': artilleries1,
    'cruiser': cruisers1,
    'explorer': explorers1
}

superdict111 = {
    'city': cities1,
    'sawmill': sawmills1,
    'farm': farms1,
    "fish_farm": fish_farms1,
    "stone_mine": stone_mines1,
    "metal_mine": metal_mines1,
    "plat_mine": plat_mines1,
    "super_mine": super_mines1,
    "shipyard": shipyards1,
    "tower": towers1,
    'artillery': artilleries1,
    'cruiser': cruisers1,
    'explorer': explorers1

}

superdict22 = {
    'artillery': artilleries2,
    'cruiser': cruisers2,
    'explorer': explorers2
}

superdict222 = {
    'city': cities2,
    'sawmill': sawmills2,
    'farm': farms2,
    "fish_farm": fish_farms2,
    "stone_mine": stone_mines2,
    "metal_mine": metal_mines2,
    "plat_mine": plat_mines2,
    "super_mine": super_mines2,
    "shipyard": shipyards2,
    "tower": towers2,
    'artillery': artilleries2,
    'cruiser': cruisers2,
    'explorer': explorers2
}

superdict4 = {
    'city': City,
    'explorer': Explorer,
    'artillery': Artillery,
    'cruiser': Cruiser,
    'sawmill': Sawmill,
    'farm': Farm,
    "fish_farm": FishFarm,
    "stone_mine": StoneMine,
    "metal_mine": MetalMine,
    "plat_mine": PlatinumMine,
    "super_mine": SuperMine,
    "shipyard": Shipyard,
    "tower": Tower
}

superdict5 = {
    'capital': 'A',
    'city': 'B',
    'explorer': 'C',
    'artillery': 'D',
    'cruiser': 'E',
    'sawmill': 'F',
    'farm': 'G',
    "fish_farm": 'H',
    "stone_mine": 'I',
    "metal_mine": 'J',
    "plat_mine": 'K',
    "super_mine": 'L',
    "shipyard": 'M',
    "tower": 'N'
}

resources1 = {
    'wood': 75,
    'stone': 0,
    'gold': 50,
    'platinum': 0,
    'metal': 0,
    'food': 100
}

resources2 = {
    'wood': 75,
    'stone': 0,
    'gold': 100,
    'platinum': 0,
    'metal': 0,
    'food': 100
}

ultradict = {
    '1': superdict111,
    '2': superdict222
}

imginfo = {
    '0': 'water',
    '1': 'earth',
    '2': 'forest',
    '3': 'hill',
    '4': 'black earth',
    '5': 'mountain',
    '6': 'cave',
    '7': 'ruins',
    '8': 'platinum',
    '9': 'all',
    'A': 'capital',
    'B': 'city',
    'C': 'explorer',
    'D': 'artillery',
    'E': 'cruisers',
    'F': 'sawmill',
    'G': 'farm',
    'H': 'fish_farm',
    'I': 'stone_mine',
    'J': 'metal_mine',
    'K': 'platinum_mine',
    'L': "super_mines",
    'M': "shipyard",
    'N': 'tower'
}


# 55555555555
# 54444444445
# 54333333345
# 54322222345
# 54321112345
# 54321012345
# 54321112345
# 54322222345
# 54333333345
# 54444444445
# 55555555555
# 232, 248, 345, 412, 415

def attack_check(player):  # автоматическая атака башен ближайшего противника
    for i in range(len(ultradict[player]['tower'])):

        # for j in range(5):
        #     for k in range(j + 1):
        #         for l in range(k * 2):
        #             for p in range(4):
        #                 if ultradict[player]['tower'][i].x + k
        targets = []
        distance = []
        temp = 0
        for j in range(-5, 5):
            for l in range(-5, 5):
                if str(mapa[j][l]) != any in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and map_[j][
                    l] == 3 - player:
                    targets.append((j, l))
        for j in range(len(targets)):
            distance[j] = int((targets[j][0] ** 2 + targets[j][1] ** 2) ** 0.5)

        for j in range(len(distance)):
            if distance[j] <= distance[temp]:
                temp = j
        for j in range(len(ultradict[3 - player][imginfo[mapa[targets[temp][0]][targets[temp][0]]]])):
            if ultradict[player]['tower'][i].x == \
                    ultradict[3 - player][imginfo[mapa[targets[temp][0]][targets[temp][0]]]][j] and \
                    ultradict[player]['tower'][i].y == \
                    ultradict[3 - player][imginfo[mapa[targets[temp][0]][targets[temp][0]]]][j]:
                ultradict[player]['tower'][i].target = \
                    ultradict[3 - player][imginfo[mapa[targets[temp][0]][targets[temp][0]]]][j]
        try:
            ultradict[player]['tower'][i].attack()
        except:
            pass


def queue(attack_queue, move_queue, build_queue):  # тут вроде и так понятно
    pass


def income_func(player):  # прибавка ресурсов
    if player == 1:
        for i in range(len(superlist1)):
            for j in range(len(superlist1[i])):
                for k in range(len(superlist1[i][j].income)):
                    resources1[superlist1[i][j].resource[k]] += superlist1[i][j].income[k]
    else:
        for i in range(len(superlist2)):
            for j in range(len(superlist2[i])):
                for k in range(len(superlist2[i][j].income)):
                    resources2[superlist2[i][j].resource[k]] += superlist2[i][j].income[k]


need_to_sent = 0
print(capital1, capital2)
while running:  # основной цикл сервера
    need_to_sent += 1
    map_ = []
    for i in range(40):  # а вот это фигня с границами
        a = [0] * 40
        map_.append(a)
    try:
        new_socket, addr = main_socket.accept()
        print('add', addr)
        new_socket.setblocking(False)
        players_sockets.append(new_socket)
        players_addr.append(addr)
        new_socket.send(s.encode())
    except:
        pass

    # for i in range(2):  # проверка на уничтожение зданий и юнитов
    #     for j in ultralist[i]:
    #         for k in j:
    #             try:
    #                 mapa[k.x][k.y] = k.destroy()
    #                 j.remove(k)
    #             except:
    #                 pass

    data = 0
    for i in players_sockets:  # че то отправляем
        try:
            data = i.recv(2 ** 20).decode()
            if data == 'give map':
                print('map sent')
                for a in cities1:  # рисуем границы государств
                    for i in range(5):
                        for j in range(5):
                            try:
                                if str(map_[a.x - 2 + i][a.y - 2 + j]) == '0':
                                    map_[a.x - 2 + i][a.y - 2 + j] = '2'
                            except:
                                pass
                for city in cities2:
                    for i in range(5):
                        for j in range(5):
                            try:
                                if str(map_[city.x - 2 + i][city.y - 2 + j]) == '0':
                                    map_[city.x - 2 + i][city.y - 2 + j] = '1'
                            except:
                                pass

                # лениво рисуем границы государств*/
                try:
                    print(capital1[0], capital2[0])
                except:
                    print(capital1, capital2)
                for i in range(5):
                    for j in range(5):
                        try:
                            if str(map_[capital1[0].x - 2 + i][capital1[0].y - 2 + j]) == '0':
                                map_[capital1[0].x - 2 + i][capital1[0].y - 2 + j] = '2'
                        except:
                            print('ono slomalos111')
                        try:
                            if str(map_[capital2[0].x - 2 + i][capital2[0].y - 2 + j]) == '0':
                                map_[capital2[0].x - 2 + i][capital2[0].y - 2 + j] = '1'
                        except:
                            print('ono slomalos222')

                for explorer in explorers1:  # рисуем границы государств
                    for i in range(3):
                        for j in range(3):
                            try:
                                if str(map_[explorer.x - 1 + i][explorer.y - 1 + j]) == '0':
                                    map_[explorer.x - 1 + i][explorer.y - 1 + j] = '2'
                            except:
                                pass

                for a in explorers2:  # код ленивого балбеса
                    for i in range(3):
                        for j in range(3):
                            try:
                                if str(map_[a.x - 1 + i][a.y - 1 + j]) == '0':
                                    map_[a.x - 1 + i][a.y - 1 + j] = '1'
                            except:
                                pass

                s = ''
                for k in range(40):
                    for j in range(40):
                        s += mapa[k][j]
                    s += '\n'
                for k in range(40):
                    for j in range(40):
                        s += str(map_[k][j])
                    s += '\n'
                i.send(s.encode())

            elif data[:10] == 'give stats':  # give stats farm 2 5 1

                data = data[10:].split()
                if data[-1] == '1':
                    for j in superdict111[data[0]]:
                        if j.y == data[1] and j.x == data[2]:
                            atk = 0
                            try:
                                atk = j.atk
                            except:
                                pass
                            i.send(('hp = ' + str(j.hp) + ' atk = ' + str(atk) + ' level = ' + str(j.level)).encode())

                elif data[-1] == '2':
                    for j in superdict222[data[0]]:
                        if j.y == data[1] and j.x == data[2]:
                            atk = 0
                            try:
                                atk = j.atk
                            except:
                                pass
                            i.send(('hp = ' + str(j.hp) + ' atk = ' + str(atk) + ' level = ' + str(j.level)).encode())

                else:
                    i.send((' ').encode())
                    print('balbesina pustuyu stroke otpravlyaet')
                print('stats sent')

            elif data[:9] == 'give turn':  # give turn x y
                print('turn sent')
                data = data[9:].split()
                if capital1[0].y == int(data[0]) and capital1[0].x == int(data[1]):
                    i.send((str(turn) + " " + str(resources1['wood']) + "\n" + str(resources1['stone']) + " " + str(
                        resources1['gold']) + "\n" + str(resources1['platinum']) + " " + str(
                        resources1['metal']) + "\n" + str(
                        resources1['food'])).encode())
                elif capital2[0].y == int(data[0]) and capital2[0].x == int(data[1]):
                    i.send((str(turn) + " " + str(resources2['wood']) + "\n" + str(resources2['stone']) + " " + str(
                        resources2['gold']) + "\n" + str(resources2['platinum']) + "\n" + str(
                        resources2['metal']) + "\n" + str(
                        resources2['food'])).encode())
                else:
                    print('balbesina777')
        except:
            pass
    if turn1 != turn:  # заработок ресурсов в ход
        turn1 = turn
        income_func(turn % 2 + 1)  # перенести отсюда в место, где прибавляется ход

    data = 0
    try:  # принимаем команды
        data = 0
        try:
            data = players_sockets[turn % 2].recv(2 ** 20).decode()
            data = data.split()
        except:
            pass
        time.sleep(0.005)
        data1 = 0
        try:
            data1 = players_sockets[turn % 2].recv(2 ** 20).decode()
            data1 = data1.split()
        except:
            pass
        time.sleep(0.005)
        data2 = 0
        try:
            data2 = players_sockets[turn % 2].recv(2 ** 20).decode()
            data2 = data2.split()
        except:
            pass
        print(data, data1, data2, end='\n')
        command = 0
        try:
            if data and (data[0] == 'place' or data[0] == 'destroy' or data[0] == 'unit' or data[0] == 'attack' or data[
                0] == 'move' or data[0] == 'skip'):
                command = data
        except:
            pass
        try:
            if data1 and (
                    data1[0] == 'place' or data1[0] == 'destroy' or data1[0] == 'unit' or data1[0] == 'attack' or data1[
                0] == 'move' or data[0] == 'skip'):
                command = data1
        except:
            pass
        try:
            if data2[0] == 'place' or data2[0] == 'destroy' or data2[0] == 'unit' or data2[0] == 'attack' or data2[
                0] == 'move' or data[0] == 'skip':
                command = data2
        except:
            pass
        print('\n\n\n\n', command, command[0], '\n\n\n\n\n')

        if command[0] == 'place':  # place 2 5 capital
            turn += 1
            command[1], command[2] = int(command[2]), int(command[1])

            print(111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111)
            print(command[3] == 'capital' and (len(capital1) == 0 or len(capital2) == 0) and str(
                mapa[command[1]][command[2]]) != '0' and str(
                map_[command[1]][command[2]]) == '0')
            if command[3] == 'capital':
                if (len(capital1) == 0 or len(capital2) == 0) and str(mapa[command[1]][command[2]]) != '0' and str(
                        map_[command[1]][command[2]]) == '0':
                    mapa[command[1]][command[2]] = 'A'

                    if turn % 2 == 0:
                        zzz = Capital(command[1], command[2], mapa[command[1]][command[2]])
                        capital2.append(zzz)
                    else:
                        fff = Capital(command[1], command[2], mapa[command[1]][command[2]])
                        capital1.append(fff)

            else:
                if turn % 2 == 0:
                    true = True
                    true *= (superdict[command[3]][0] <= resources2['wood'])
                    true *= (superdict[command[3]][1] <= resources2['gold'])
                    if true:
                        superdict2[command[3]].append(
                            superdict4[command[3]](command[1], command[2], mapa[command[1]][command[2]]))
                        mapa[command[1]][command[2]] = superdict5[command[3]]
                        resources2['wood'] -= superdict[command[3]][0]
                        resources2['gold'] -= superdict[command[3]][1]
                else:
                    true = True
                    true *= (superdict[command[3]][0] <= resources1['wood'])
                    true *= (superdict[command[3]][1] <= resources1['gold'])
                    if true:
                        superdict1[command[3]].append(
                            superdict4[command[3]](command[1], command[2], mapa[command[1]][command[2]]))
                        mapa[command[1]][command[2]] = superdict5[command[3]]
                        resources1['wood'] -= superdict[command[3]][0]
                        resources1['gold'] -= superdict[command[3]][1]
            # players_sockets[turn % 2].send(command[3] + 'completed'.encode())
        elif command[0] == 'destroy':  # destroy farm 2 5
            # if mapa[]
            turn += 1
            if turn % 2 + 1 == 1:
                for i in superdict1[command[1]]:
                    if superdict1[command[1]][i].x == command[2] and superdict1[command[1]][i].y == command[3]:
                        mapa[command[2]][command[3]] = superdict1[command[1]][i].landscape_before
                        resources1['wood'] += int(superdict1[command[1]].cost[0]) * 0.3
                        resources1['gold'] += int(superdict1[command[1]].cost[1]) * 0.3
            else:
                for i in superdict2[command[1]]:
                    if superdict2[command[1]][i].x == command[2] and superdict2[command[1]][i].y == command[3]:
                        mapa[command[2]][command[3]] = superdict2[command[1]][i].landscape_before
                        resources2['wood'] += int(superdict2[command[1]].cost[0]) * 0.3
                        resources2['gold'] += int(superdict2[command[1]].cost[1]) * 0.3

        elif command[0] == 'unit':  # где прибавка хода?
            if turn % 2 == 0:
                true = True
                true *= (superdict[command[3]][0] <= resources2['wood'])
                true *= (superdict[command[3]][1] <= resources2['gold'])
                true *= (superdict[command[3]][2] <= resources2['metal'])
                if true and (
                        mapa[command[1] - 1][command[2]] == 'M' or mapa[command[1] + 1][command[2]] == 'M' or
                        mapa[command[1]][
                            command[2] - 1] == 'M' or mapa[command[1]][command[2] + 1] == 'M'):
                    superdict2[command[3]].append(
                        superdict4[command[3]](command[1], command[2], mapa[command[1]][command[2]]))
                    mapa[command[1]][command[2]] = superdict5[command[3]]
                    resources2['wood'] -= superdict[command[3]][0]
                    resources2['gold'] -= superdict[command[3]][1]
                    resources2['metal'] -= superdict[command[3]][2]
            else:
                true = True
                true *= (superdict[command[3]][0] <= resources1['wood'])
                true *= (superdict[command[3]][1] <= resources1['gold'])
                true *= (superdict[command[3]][2] <= resources1['metal'])
                if true and (
                        mapa[command[1] - 1][command[2]] == 'M' or mapa[command[1] + 1][command[2]] == 'M' or
                        mapa[command[1]][
                            command[2] - 1] == 'M' or mapa[command[1]][command[2] + 1] == 'M'):
                    superdict1[command[3]].append(
                        superdict4[command[3]](command[1], command[2], mapa[command[1]][command[2]]))
                    mapa[command[1]][command[2]] = superdict5[command[3]]
                    resources1['wood'] -= superdict[command[3]][0]
                    resources1['gold'] -= superdict[command[3]][1]
                    resources1['metal'] -= superdict[command[3]][2]
            turn += 1
        elif command[0] == 'move':  # move cruiser 2 5 4 5
            pass

        elif command[0] == 'attack':  # attack cruiser 2 5 farm 4 5
            turn += 1
            if turn % 2 + 1 == 1:
                for i in superdict11[command[1]]:
                    if superdict11[command[1]][i].x == command[2] and superdict11[command[1]][i].y == command[2]:
                        pass  # ждем синхронизации супердиктов 1, 11 и 111

        elif command[0] == 'skip':
            turn += 1

        # print(turn, players_addr[(turn - 1) % 2])
    except:
        pass

    # for sock in players_sockets:
    #     try:
    #         data = sock.recv(2**20)
    #         data = data.decode()
    #         print('get', data)
    #     except:
    #         pass
    for a in cities1:  # рисуем границы государств
        for i in range(5):
            for j in range(5):
                try:
                    if str(map_[a.x - 2 + i][a.y - 2 + j]) == '0':
                        map_[a.x - 2 + i][a.y - 2 + j] = '2'
                except:
                    pass
    for city in cities2:
        for i in range(5):
            for j in range(5):
                try:
                    if str(map_[city.x - 2 + i][city.y - 2 + j]) == '0':
                        map_[city.x - 2 + i][city.y - 2 + j] = '1'
                except:
                    pass

    for a in capital1:  # лениво рисуем границы государств
        for i in range(5):
            for j in range(5):
                try:
                    if str(map_[a.x - 2 + i][a.y - 2 + j]) == '0':
                        map_[a.x - 2 + i][a.y - 2 + j] = '2'
                except:
                    print('ono slomalos')

    for capital in capital2:
        for i in range(5):
            for j in range(5):
                try:
                    if str(map_[capital.x - 2 + i][capital.y - 2 + j]) == '0':
                        map_[capital.x - 2 + i][capital.y - 2 + j] = '1'
                except:
                    print('ono slomalos')

    for explorer in explorers1:  # рисуем границы государств
        for i in range(3):
            for j in range(3):
                try:
                    if str(map_[explorer.x - 1 + i][explorer.y - 1 + j]) == '0':
                        map_[explorer.x - 1 + i][explorer.y - 1 + j] = '2'
                except:
                    pass

    for a in explorers2:  # код ленивого балбеса
        for i in range(3):
            for j in range(3):
                try:
                    if str(map_[a.x - 1 + i][a.y - 1 + j]) == '0':
                        map_[a.x - 1 + i][a.y - 1 + j] = '1'
                except:
                    pass

    s = ''
    for i in range(40):
        for j in range(40):
            try:
                s += mapa[i][j]
            except:
                s += 'A'
        s += '\n'
    for i in range(40):
        for j in range(40):
            s += str(map_[i][j])
        s += '\n'

    # for sock in players_sockets:
    #     try:
    #         sock.send(s.encode())
    #     except:
    #         players_sockets.remove(sock)
    #         sock.close()
    #         print('disconnected', sock)
    if need_to_sent == 20:
        need_to_sent = 0
        for sock in players_sockets:
            try:
                sock.send(s.encode())
            except:
                pass
    time.sleep(0.01)

# elif command[3] == 'city': #superdict[command[3]].cost[i] <= resources2[]
#                 if str(map_[command[1]][command[2]]) == str(turn % 2 + 1):
#                     mapa[command[1]][command[2]] = ';'
#                     if turn % 2 == 0:
#                         if recources2[City.recource[0]] >= City.cost[0] and recources2[City.recource[1]] >= City.cost[1]:
#                             cities2.append(City(command[1], command[2]))

#                     else:
#                         cities1.append(City(command[1], command[2]))
#             elif command[3] == 'tower':
#                 if str(map_[command[1]][command[2]]) == str(turn % 2 + 1):
#                     if map_[command[1]][command[2]] == str(turn % 2 + 1):
#                         mapa[command[1]][command[2]] = '>'
#             elif command[3] == 'sawmill':
#                 mapa[command[1]][command[2]] = 'F'
#                 if turn % 2 == 0:
#                     sawmills2.append([command[1], command[2]])
#                 else:
#                     sawmills1.append([command[1], command[2]])
#             elif command[3] == 'farm':
#                 mapa[command[1]][command[2]] = 'G'
#                 if turn % 2 == 0:
#                     farms2.append([command[1], command[2]])
#                 else:
#                     farms1.append([command[1], command[2]])
#             elif command[3] == 'fish_farm':
#                 mapa[command[1]][command[2]] = 'H'
#                 if turn % 2 == 0:
#                     fish_farms2.append([command[1], command[2]])
#                 else:
#                     fish_farms1.append([command[1], command[2]])
