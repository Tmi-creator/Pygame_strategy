import socket
import time
import os
import subprocess

from oop import *

subprocess.run(["a.exe", "-config filename"])
subprocess.run(["smooth2.exe", "-config filename"])

# turn % 2 == 0 - 1player, turn%2 == 1  - 2 player
# cmd1 = "smooth2.cpp"
# subprocess.call(["g++", cmd1])
# subprocess.call("./a.out")

f = open('output.txt', 'r+')
main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind(('localhost', 9999))
main_socket.setblocking(False)
main_socket.listen(10)
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

ecolist1 = [capital1, cities1, explorers2, artilleries2, cruisers2, sawmills1, farms1, fish_farms1,
            stone_mines1, metal_mines1, plat_mines1, super_mines1, shipyards1, towers1]
ecolist2 = [capital2, cities2, explorers1, artilleries1, cruisers1, sawmills2, farms2, fish_farms2,
            stone_mines2, metal_mines2, plat_mines2, super_mines2, shipyards2, towers2]
superborders = [capital1, capital2, cities1, cities2, explorers1, explorers2]

ultralist = [superlist1, superlist2]
ultralist1 = [ecolist1, ecolist2]

upgrade_cost = [[50, 20], [50, 20]]  # stone gold
# upgrade cost * (1.1 ** upgrade_cnt)
upgrade_cnt1 = 0
upgrade_cnt2 = 0

levels1 = {
    'city': 1,
    'sawmill': 1,
    'farm': 1,
    "fish_farm": 1,
    "stone_mine": 1,
    "metal_mine": 1,
    "plat_mine": 1,
    "super_mine": 1,
    "shipyard": 1,
    "tower": 1
}

levels2 = {
    'city': 1,
    'sawmill': 1,
    'farm': 1,
    "fish_farm": 1,
    "stone_mine": 1,
    "metal_mine": 1,
    "plat_mine": 1,
    "super_mine": 1,
    "shipyard": 1,
    "tower": 1
}
# цены на все
superdict = {  # for i in range(len(superdict[command[3]].cost)):
    'city': City().cost,  # superdict[command[3]].cost[i] <= resources2[command[3]].cost[i]
    'sawmill': Sawmill().cost,  # superdict2[command[3]].append(superdict4[command[3]](command[1], command[2]))
    'farm': Farm().cost,
    "fish_farm": FishFarm().cost,
    "stone_mine": StoneMine().cost,
    "metal_mine": MetalMine().cost,
    "plat_mine": PlatinumMine().cost,
    "super_mine": SuperMine().cost,
    "shipyard": Shipyard().cost,
    "tower": Tower().cost,
    'explorer': Explorer().cost,
    'artillery': Artillery().cost,
    'cruiser': Cruiser().cost
}
# словарь со списками всех построек игрока 1
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
# то же самое но игрок 2
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
# словарь со списками всех юнитов игрока 1
superdict11 = {
    'artillery': artilleries1,
    'cruiser': cruisers1,
    'explorer': explorers1
}
# вообще все игрока 1
superdict111 = {
    'capital': capital1,
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
# словарь со списками всех юнитов игрока 2
superdict22 = {
    'artillery': artilleries2,
    'cruiser': cruisers2,
    'explorer': explorers2
}
# вообще все игрока 2
superdict222 = {
    'capital': capital2,
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
# обращение к классам
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
# обозначение на карте
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
superdict7 = {
    'city': City().landscape,
    'explorer': Explorer().landscape,
    'artillery': Artillery().landscape,
    'cruiser': Cruiser().landscape,
    'sawmill': Sawmill().landscape,
    'farm': Farm().landscape,
    "fish_farm": FishFarm().landscape,
    "stone_mine": StoneMine().landscape,
    "metal_mine": MetalMine().landscape,
    "plat_mine": PlatinumMine().landscape,
    "super_mine": SuperMine().landscape,
    "shipyard": Shipyard().landscape,
    "tower": Tower().landscape
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
# не влезай убьет
ultradict = {
    '1': superdict111,
    '2': superdict222
}

ultraresources = {
    '1': resources1,
    '2': resources2
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


def income_func():  # прибавка ресурсов НЕ ТРОГАТЬ
    for player in range(len(ultralist1)):
        for i in range(len(ultralist1[player])):
            for j in range(len(ultralist1[player][i])):
                for k in range(len(ultralist1[player][i][j].income)):
                    ultraresources[str(player + 1)][ultralist1[player][i][j].resource[k]] += \
                    ultralist1[player][i][j].income[k] * (1.1 ** (ultralist1[player][i][j].level - 1))
        print(ultraresources[str(player + 1)])


def make_move_great_again(player):  # опять можно двигать все что двигается
    if player == 1:
        for i in superdict11.keys():
            for j in superdict11[i]:
                j.can_move = True
    else:
        for i in superdict22.keys():
            for j in superdict22[i]:
                j.can_move = True


def make_attack_great_again(player):  # опять можно стрелять всем что стреляется
    if player == 1:
        for i in superdict11.keys():
            for j in superdict11[i]:
                j.can_attack = True
    else:
        for i in superdict22.keys():
            for j in superdict22[i]:
                j.can_attack = True


def risuemgranit():  # рисуем гранит
    for fignya in range(6):  # для фигни от 0 до 5
        for k in range(len(superborders[fignya])):
            for i in range(5 - fignya // 4 * 2):  # сам хз что это
                for j in range(5 - fignya // 4 * 2):
                    try:  # попытка не пытка
                        if str(map_[superborders[fignya][k].x - (2 - fignya // 4) + i][
                                   superborders[fignya][k].y - (2 - fignya // 4) + j]) == '0':
                            map_[superborders[fignya][k].x - (2 - fignya // 4) + i][
                                superborders[fignya][k].y - (2 - fignya // 4) + j] = str(fignya % 2 + 1)
                    except:
                        pass  # пропуск (билет типа)


news = ''

need_to_sent = 0
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
    risuemgranit()

    # for i in range(2):  # проверка на уничтожение зданий и юнитов
    #     for j in ultralist[i]:
    #         for k in j:
    #             try:
    #                 mapa[k.x][k.y] = k.destroy()
    #                 j.remove(k)
    #             except:
    #                 pass

    if turn1 != turn:  # заработок ресурсов в ход
        income_func()  # перенести отсюда в место, где прибавляется ход completed
        make_move_great_again(turn % 2 + 1)
        make_attack_great_again(turn % 2 + 1)
        turn1 = turn

    data = 0
    try:  # принимаем командs
        data = players_sockets[turn % 2].recv(2 ** 20).decode()
        data = data.split()
        command = data
        if command[0] == 'place':  # place 2 5 capital
            turn += 1
            command[1], command[2] = int(command[2]), int(command[1])

            # 100000
            # 000000
            # 000000
            # 000000
            # 000001
            if command[3] == 'capital':
                if (len(capital1) == 0 or len(capital2) == 0) and str(mapa[command[1]][command[2]]) != '0' and str(
                        map_[command[1]][command[2]]) == '0' and not (15 < int(command[1]) < 26 and 15 < int(
                    command[2]) < 26) and -1 < int(command[1]) < 41 and -1 < int(command[2]) < 41:
                    if capital2 and (abs(int(command[1]) - capital2[0].x) > 4 or abs(
                            int(command[2]) - capital2[0].y) > 4) or not capital2:

                        mapa[command[1]][command[2]] = 'A'

                        if turn % 2 == 0:
                            zzz = Capital(command[1], command[2], mapa[command[1]][command[2]])
                            capital2.append(zzz)
                            news += str(command[3]) + ' ' + str(zzz.x) + ' ' + str(zzz.y) + ' ' + str(
                                turn % 2 + 1) + ' ' + str(zzz.hp)
                        else:
                            fff = Capital(command[1], command[2], mapa[command[1]][command[2]])
                            capital1.append(fff)
                            news += str(command[3]) + ' ' + str(fff.x) + ' ' + str(fff.y) + ' ' + str(
                                turn % 2 + 1) + ' ' + str(fff.hp)

            else:
                if turn % 2 == 0:
                    true = (superdict[command[3]][0] <= resources2['wood'])
                    true *= (superdict[command[3]][1] <= resources2['gold'])
                    true *= (str(mapa[command[1]][command[2]]) in superdict7[command[3]])
                    true *= (int(map_[command[1]][command[2]]) == (2 - turn % 2))

                    if true:
                        ooo = superdict4[command[3]](command[1], command[2], mapa[command[1]][command[2]])
                        superdict2[command[3]].append(ooo)
                        mapa[command[1]][command[2]] = superdict5[command[3]]
                        resources2['wood'] -= superdict[command[3]][0]
                        resources2['gold'] -= superdict[command[3]][1]
                        news += str(command[3]) + ' ' + str(ooo.x) + ' ' + str(ooo.y) + ' ' + str(
                            turn % 2 + 1) + ' ' + str(ooo.hp)
                        if command[3] == 'tower':  # атаку добавить короче
                            news += " " + str(ooo.atk)

                else:
                    true = (superdict[command[3]][0] <= resources1['wood'])
                    true *= (superdict[command[3]][1] <= resources1['gold'])
                    true *= (str(mapa[command[1]][command[2]]) in superdict7[command[3]])
                    true *= (int(map_[command[1]][command[2]]) == (2 - turn % 2))

                    if true:
                        ooo = superdict4[command[3]](command[1], command[2], mapa[command[1]][command[2]])
                        superdict1[command[3]].append(ooo)
                        mapa[command[1]][command[2]] = superdict5[command[3]]
                        resources1['wood'] -= superdict[command[3]][0]
                        resources1['gold'] -= superdict[command[3]][1]
                        news += str(command[3]) + ' ' + str(ooo.x) + ' ' + str(ooo.y) + ' ' + str(
                            turn % 2 + 1) + ' ' + str(ooo.hp)
                        if command[3] == 'tower':  # атаку добавить короче
                            news += " " + str(ooo.atk)
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
                        news += 'update destroy ' + command[2] + ' ' + command[3]
            else:
                for i in superdict2[command[1]]:
                    if superdict2[command[1]][i].x == command[2] and superdict2[command[1]][i].y == command[3]:
                        mapa[command[2]][command[3]] = superdict2[command[1]][i].landscape_before
                        resources2['wood'] += int(superdict2[command[1]].cost[0]) * 0.3
                        resources2['gold'] += int(superdict2[command[1]].cost[1]) * 0.3
                        news += 'update destroy ' + command[2] + " " + command[3]

        elif command[0] == 'unit':  # где прибавка хода?
            turn += 1
            command[1], command[2] = int(command[2]), int(command[1])
            if turn % 2 == 1:
                true = True
                true *= (superdict[command[3]][0] <= resources2['wood'])
                true *= (superdict[command[3]][1] <= resources2['gold'])
                true *= (superdict[command[3]][2] <= resources2['metal'])
                true1 = False
                try:
                    true1 += (mapa[command[1] - 1][command[2]] == 'M')
                except:
                    pass
                try:
                    true1 += (mapa[command[1] + 1][command[2]] == 'M')
                except:
                    pass
                try:
                    true1 += (mapa[command[1]][command[2] - 1] == 'M')
                except:
                    pass
                try:
                    true1 += (mapa[command[1]][command[2] + 1] == 'M')
                except:
                    pass
                if true and true1:
                    ooo = superdict4[command[3]](command[1], command[2], mapa[command[1]][command[2]])
                    superdict22[command[3]].append(ooo)
                    mapa[command[1]][command[2]] = superdict5[command[3]]  # unit 1 2 cruiser
                    resources2['wood'] -= superdict[command[3]][0]
                    resources2['gold'] -= superdict[command[3]][1]
                    resources2['metal'] -= superdict[command[3]][2]
                    news += str(command[3]) + ' ' + str(ooo.x) + ' ' + str(ooo.y) + ' ' + str(turn % 2 + 1) + ' ' + str(
                        ooo.hp) + ' ' + str(ooo.atk)
            else:
                true = True
                true *= (superdict[command[3]][0] <= resources1['wood'])
                true *= (superdict[command[3]][1] <= resources1['gold'])
                true *= (superdict[command[3]][2] <= resources1['metal'])
                true1 = False
                try:
                    true1 += (mapa[command[1] - 1][command[2]] == 'M')
                except:
                    pass
                try:
                    true1 += (mapa[command[1] + 1][command[2]] == 'M')
                except:
                    pass
                try:
                    true1 += (mapa[command[1]][command[2] - 1] == 'M')
                except:
                    pass
                try:
                    true1 += (mapa[command[1]][command[2] + 1] == 'M')
                except:
                    pass
                if true and true1:
                    ooo = superdict4[command[3]](command[1], command[2], mapa[command[1]][command[2]])
                    superdict11[command[3]].append(ooo)
                    mapa[command[1]][command[2]] = superdict5[command[3]]
                    resources1['wood'] -= superdict[command[3]][0]
                    resources1['gold'] -= superdict[command[3]][1]
                    resources1['metal'] -= superdict[command[3]][2]
                    news += str(command[3]) + ' ' + str(ooo.x) + ' ' + str(ooo.y) + ' ' + str(turn % 2 + 1) + ' ' + str(
                        ooo.hp) + ' ' + str(ooo.atk)

        elif command[0] == 'move':  # move cruiser 2 5 4 5
            cur_plane = 0
            for i in range(2, 6):
                command[i] = int(command[i])
            if turn % 2 == 0:

                for i in superdict22[command[1]]:
                    if i.x == int(command[2]) and i.y == int(command[3]):
                        cur_plane = i
                if cur_plane and cur_plane.can_move and str(mapa[command[4]][command[5]]) in ['0', '1', '2', '3', '4',
                                                                                              '5', '6', '7', '8', '9']:
                    if abs(int(command[2]) - int(command[4])) <= cur_plane.speed and abs(
                            command[3] - command[5]) <= cur_plane.speed:
                        cur_plane.can_move = False
                        mapa[command[2]][command[3]] = cur_plane.landscape_before
                        map_[command[4]][command[5]] = '1'
                        mapa[command[4]][command[5]] = superdict5[command[1]]
                        cur_plane.x = command[4]
                        cur_plane.y = command[5]
                        for i in range(2, 6):
                            command[i] = str(command[i])
                        news += 'update move ' + command[2] + ' ' + command[3] + ' ' + command[4] + ' ' + command[5]
            else:
                for i in superdict11[command[1]]:
                    if i.x == int(command[2]) and i.y == int(command[3]):
                        cur_plane = i
                if cur_plane and cur_plane.can_move and str(mapa[command[4]][command[5]]) in ['0', '1', '2', '3', '4',
                                                                                              '5', '6', '7', '8', '9']:
                    if abs(int(command[2]) - int(command[4])) <= cur_plane.speed and abs(
                            command[3] - command[5]) <= cur_plane.speed:
                        cur_plane.can_move = False
                        mapa[command[2]][command[3]] = cur_plane.landscape_before
                        map_[command[4]][command[5]] = '2'
                        mapa[command[4]][command[5]] = superdict5[command[1]]
                        cur_plane.x = command[4]
                        cur_plane.y = command[5]
                        for i in range(2, 6):
                            command[i] = str(command[i])
                        news += 'update move ' + command[2] + ' ' + command[3] + ' ' + command[4] + ' ' + command[5]



        elif command[0] == 'attack':  # attack cruiser 2 3 farm 5 6
            print(command)
            if turn % 2 + 1 == 2:
                for i in superdict11[command[1]]:
                    if str(i.x) == command[2] and str(i.y) == command[3] and abs(
                            int(command[5]) - int(command[2])) <= i.range and abs(
                            int(command[6]) - int(command[3])) <= i.range:
                        for j in superdict222[command[4]]:
                            if str(j.x) == command[5] and str(j.y) == command[6] and i.can_attack:
                                j.hp -= i.atk
                                i.can_attack = False
                                if j.hp < 1:
                                    mapa[int(command[5])][int(command[6])] = j.destroy()
                                    superdict222[command[4]].remove(j)
                                    if not capital2:
                                        news = '1 win'
                                    if not capital1:
                                        news = '2 win'
                                    if not news:
                                        news = 'update destroy ' + str(j.x) + ' ' + str(j.y)
                                    break
                                if not news:
                                    news = 'update attack ' + str(j.x) + ' ' + str(j.y) + ' ' + str(j.hp)
                                break

            else:
                for i in superdict22[command[1]]:
                    if str(i.x) == command[2] and str(i.y) == command[3] and abs(
                            int(command[5]) - int(command[2])) <= i.range and abs(
                            int(command[6]) - int(command[3])) <= i.range:
                        for j in superdict111[command[4]]:
                            if str(j.x) == command[5] and str(j.y) == command[6] and i.can_attack:
                                j.hp -= i.atk
                                i.can_attack = False

                                if j.hp < 1:
                                    mapa[int(command[5])][int(command[6])] = j.destroy()
                                    superdict111[command[4]].remove(j)
                                    if not capital2:
                                        news = '1 win'
                                    if not capital1:
                                        news = '2 win'
                                    if not news:
                                        news = 'update destroy ' + str(j.x) + ' ' + str(j.y)
                                    break
                                if not news:
                                    news = 'update attack ' + str(j.x) + ' ' + str(j.y) + ' ' + str(j.hp)
                                break

        elif command[0] == 'skip':
            turn += 1

        elif command[0] == 'upgrade':  # upgrade farm
            if turn % 2 == 0:
                true = True
                true *= (superdict[command[3]][0] <= resources2['stone'])
                true *= (superdict[command[3]][1] <= resources2['gold'])
                if true:
                    levels2[command[1]] += 1

                    for i in superdict222[command[2]]:
                        i.level = levels2[command[2]]
            else:
                true = True
                true *= (superdict[command[3]][0] <= resources1['stone'])
                true *= (superdict[command[3]][1] <= resources1['gold'])
                if true:
                    levels1[command[1]] += 1
                    for i in superdict111[command[2]]:
                        i.level = levels1[command[2]]

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

    map_ = []
    for i in range(40):  # а вот это фигня с границами
        a = [0] * 40
        map_.append(a)
    risuemgranit()

    for i in superdict11.keys():
        for j in superdict11[i]:
            map_[int(j.x)][int(j.y)] = '2'
    for i in superdict22.keys():
        for j in superdict22[i]:
            map_[int(j.x)][int(j.y)] = '1'

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
    s += '/' + news
    resources_array = []
    for i in range(len(ultraresources.keys())):
        suslik = ''
        for j in ultraresources[str(i + 1)].keys():
            suslik += str(ultraresources[str(i + 1)][j]) + ' '
        resources_array.append(suslik[:-1])

    # for sock in players_sockets:
    #     try:
    #         sock.send(s.encode())
    #     except:
    #         players_sockets.remove(sock)
    #         sock.close()
    #         print('disconnected', sock)
    if need_to_sent == 20:
        need_to_sent = 0
        i = 0
        for sock in players_sockets:
            if news not in ['1 win', '2 win']:
                super_s = s + "/" + str(turn) + ' ' + resources_array[i] + " " + str(i)
            else:
                if int(news[0]) - 1 == i:
                    super_s = 'you win'
                else:
                    super_s = 'you lose'
            i += 1
            try:
                sock.send(super_s.encode())
            except:
                pass
        news = ''
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
