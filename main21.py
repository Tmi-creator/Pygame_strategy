import os
from pprint import pprint
from random import randint

import pygame

pygame.init()
import socket
import Button

my_font = 'Lato-Regular.ttf'
RED = (255, 50, 50)
GREEN = (50, 255, 50)


class PosButton(Button.Button):  # координаты выбранной клетки
    def __init__(self, x, y, button_text, font_size=30, font_color=RED, button_color=GREEN):
        Button.Button.__init__(self, x, y, button_text, font_size, font_color, button_color)
        self.is_active = False
        self.height = 40
        self.width = 300


class OutConsoleButton(Button.Button):
    def __init__(self, x, y, button_text, font_size=20, font_color=RED, button_color=GREEN):
        Button.Button.__init__(self, x, y, button_text, font_size, font_color, button_color)
        self.is_active = False
        self.height = 100
        self.width = 200


class ConsoleButton(Button.Button):  # консоль офигеть работает
    def __init__(self, x, y, button_text, font_size=20, font_color=RED, button_color=GREEN):
        Button.Button.__init__(self, x, y, button_text, font_size, font_color, button_color)
        self.is_active = False
        self.height = 100
        self.width = 200


console_button = ConsoleButton(900, 600, '')
pos_button = PosButton(820, 20, "")
out_console_button = OutConsoleButton(900, 700, '')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.connect(('localhost', 9999))  # делоем сервер

settings = (1200, 800)
screen = pygame.display.set_mode(settings, pygame.RESIZABLE)
FPS = 30
CLOCK = pygame.time.Clock()

dat = sock.recv(2 ** 20)
dat = dat.decode()
f = open("input.txt", "w+")
f.write(dat)
f.close()
f = open("input.txt", "r+")
mapa = []
for i in range(40):
    a = str(f.readline())  # короче это карта с местностью и зданием
    b = []
    for k in range(40):
        b.append(a[k])
    mapa.append(b)

map_ = []
for i in range(40):  # а вот это фигня с границами
    a = ["0"] * 40
    map_.append(a)
# x1, y1 = 9 + randint(-3, 3), 9 + randint(-3, 3)
# x2, y2 = 29 + randint(-3, 3), 29 + randint(-3, 3)
# #mapa[x1][y1] = ":"
# #mapa[x2][y2] = ":"  # столица 2 выше столица 1

# # x3, y3 = 79 + randint(-5, 5), 19+ randint(-5, 5)
# # x4, y4 = 79 + randint(-5, 5), 79+ randint(-5, 5)

# for i in range(3):
#     for j in range(3):
#         map_[x1 - 1 + i][y1 - 1 + j] = 1  # границы столиц
# for i in range(3):
#     for j in range(3):
#         map_[x2 - 1 + i][y2 - 1 + j] = 2

# for i in range(3):
#     for j in range(3):
#         map_[x3 - 1 + i][y3 - 1 + j] = 3
# for i in range(3):
#     for j in range(3):
#         map_[x4 - 1 + i][y4 - 1 + j] = 4


base_path = os.path.dirname(__file__)
water_path = os.path.join(base_path, "img1/water.png")
earth_path = os.path.join(base_path, "img1/earth.png")
forest_path = os.path.join(base_path, "img1/forest.png")
mountain_path = os.path.join(base_path, "img1/mountain.png")
black_earth_path = os.path.join(base_path, "img1/black_earth.png")
cave_path = os.path.join(base_path, "img1/cave.png")
civ_path = os.path.join(base_path, "img1/civ.png")
plat_path = os.path.join(base_path, "img1/plat.png")
hill_path = os.path.join(base_path, "img1/hill.png")
all_path = os.path.join(base_path, "img1/all.png")
cap1_path = os.path.join(base_path, "img1/cap1.png")
cap2_path = os.path.join(base_path, "img1/cap2.png")
# cap3_path = os.path.join(base_path, "img1/cap3.png")
# cap4_path = os.path.join(base_path, "img1/cap4.png")
city1_path = os.path.join(base_path, "img1/city1.png")
city2_path = os.path.join(base_path, "img1/city2.png")
# city3_path = os.path.join(base_path, "img/city3.png")
# city4_path = os.path.join(base_path, "img/city4.png")
tow1_path = os.path.join(base_path, "img1/tow1.png")
tow2_path = os.path.join(base_path, "img1/tow2.png")
# tow3_path = os.path.join(base_path, "img/tow3.png")
# tow4_path = os.path.join(base_path, "img/tow4.png")
wall1_path = os.path.join(base_path, "img1/wall1.png")
wall2_path = os.path.join(base_path, "img1/wall2.png")
# wall3_path = os.path.join(base_path, "img/wall3.png")*/
# wall4_path = os.path.join(base_path, "img/wall4.png")
background_path = os.path.join(base_path, "img1/background_img.jpg")  # картинки
interfaceimg_path = os.path.join(base_path, "img1/interfaceimg.png")

water_img = pygame.image.load(water_path).convert()
earth_img = pygame.image.load(earth_path).convert()
forest_img = pygame.image.load(forest_path).convert()
mountain_img = pygame.image.load(mountain_path).convert()
black_earth_img = pygame.image.load(black_earth_path).convert()
cave_img = pygame.image.load(cave_path).convert()
civ_img = pygame.image.load(civ_path).convert()
plat_img = pygame.image.load(plat_path).convert()
hill_img = pygame.image.load(hill_path).convert()
all_img = pygame.image.load(all_path).convert()
cap1_img = pygame.image.load(cap1_path).convert()
cap2_img = pygame.image.load(cap2_path).convert()
# cap3_img = pygame.image.load(cap3_path).convert()
# cap4_img = pygame.image.load(cap4_path).convert()
city1_img = pygame.image.load(city1_path).convert()
city2_img = pygame.image.load(city2_path).convert()
# city3_img = pygame.image.load(city3_path).convert()
# city4_img = pygame.image.load(city4_path).convert()
tow1_img = pygame.image.load(tow1_path).convert()
tow2_img = pygame.image.load(tow2_path).convert()
# tow3_img = pygame.image.load(tow3_path).convert()
# tow4_img = pygame.image.load(tow4_path).convert()
wall1_img = pygame.image.load(wall1_path).convert()
wall2_img = pygame.image.load(wall2_path).convert()
# wall3_img = pygame.image.load(wall3_path).convert()
# wall4_img = pygame.image.load(wall4_path).convert() #картинки
background_img = pygame.image.load(background_path).convert()
interfaceimg_img = pygame.image.load(interfaceimg_path).convert()

pygame.display.set_caption("Яфант")
dict_caps = {
    '0': plat_img,  # это для дебага

    '1': cap1_img,  # это рабочее
    '2': cap2_img
    # 3: cap3_img,/* # это ненужное
    # 4: cap4_img
}
dict_cities = {
    '1': city1_img,
    '2': city2_img
    #   3: city3_img,
    #     4: city4_img
}
dict_towers = {
    '1': tow1_img,
    '2': tow2_img
    #     3: tow3_img,
    #     4: tow4_img
}
dict_walls = {
    '1': wall1_img,
    '2': wall2_img
    #     3: wall3_img,
    #     4: wall4_img #ура ура, еще куча картинок....
}

allimg = {
    '0': water_img,
    '1': earth_img,
    '2': forest_img,
    '3': hill_img,
    '4': black_earth_img,
    '5': mountain_img,
    '6': cave_img,
    '7': civ_img,
    '8': plat_img,
    '9': all_img,
    'd': dict_caps,
    ';': dict_cities,
    '<': dict_walls,
    'B': dict_towers
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
    'd': 'capital',
    ';': 'city',
    '<': 'wall',
    'B': 'tower'
}


# def render_map(screen, b, f): #рендер мап из файла
#     f.seek(0)
#     for i in range(100):
#         a = str(f.readline())
#         for j in range(100):
#             try:
#                 print(a[j])
#                 screen.blit(b[int(a[j])], (j * 9, i * 9))
#             except:
#                 print(i, j)
#                 pprint(map_)
#                 screen.blit(b[ord(mapa[i][j]) - 48][map_[i][j]], (j * 9, i * 9))
# if a[j].isdigit():
#     screen.blit(b[int(a[j])], (j * 9, i * 9))
# else:*/*//*
#     screen.blit(b[ord(a[j]) - 48][mapa[i][j]], (j * 9, i * 9))


def render_map(screen, allimg, data):  # пытаемся рендерить с сервера или че то типа того
    global mapa
    mapa = data.split()
    for i in range(40):
        a = mapa[i]
        for j in range(40):
            try:
                screen.blit(allimg[a[j]], (j * 20, i * 20))
            except:
                screen.blit(allimg[mapa[i][j]][str(map_[i][j])], (j * 20, i * 20))


# def write_in_file(f):
#     f.close()
#     f = open('input.txt', 'w')
#     for i in range(100):
#         gh = []
#         for k in range(100):
#             gh.append(mapa[i][k])
#         f.write(''.join(gh))
#         f.write('\n')
#     f.close()


in_menu = True
gameplay = False

need_to_frame = False


def draw_boards(map_):
    colour = [(0, 255, 0), (0, 0, 255)]
    try:
        for i in range(40):
            for j in range(40):
                if int(map_[i][j]) != 0:
                    try:
                        if map_[i][j + 1] != map_[i][j]:
                            pygame.draw.line(screen, colour[int(map_[i][j]) - 1], (j * 20 + 19, i * 20),
                                             (j * 20 + 19, i * 20 + 20), 3)
                    except:
                        pass
                    try:
                        if map_[i + 1][j] != map_[i][j]:
                            pygame.draw.line(screen, colour[int(map_[i][j]) - 1], (j * 20, i * 20 + 19),
                                             (j * 20 + 20, i * 20 + 19), 3)
                    except:
                        pass
                    try:
                        if map_[i - 1][j] != map_[i][j]:
                            pygame.draw.line(screen, colour[int(map_[i][j]) - 1], (j * 20, i * 20 + 1),
                                             (j * 20 + 20, i * 20 + 1), 3)
                    except:
                        pass
                    try:
                        if map_[i][j - 1] != map_[i][j]:
                            pygame.draw.line(screen, colour[int(map_[i][j]) - 1], (j * 20 + 1, i * 20),
                                             (j * 20 + 1, i * 20 + 20), 3)
                    except:
                        pass
    except:
        print("BALBES")


def draw_frame(x, y):
    if need_to_frame:
        pygame.draw.line(screen, RED, (x // 20 * 20, y // 20 * 20), (x // 20 * 20, y // 20 * 20 + 20), 3)
        pygame.draw.line(screen, RED, (x // 20 * 20, y // 20 * 20), (x // 20 * 20 + 20, y // 20 * 20), 3)
        pygame.draw.line(screen, RED, (x // 20 * 20 + 20, y // 20 * 20), (x // 20 * 20 + 20, y // 20 * 20 + 20), 3)
        pygame.draw.line(screen, RED, (x // 20 * 20, y // 20 * 20 + 20), (x // 20 * 20 + 20, y // 20 * 20 + 20), 3)


def start_menu():  # стартовая менюшка чтобы начать игру
    global in_menu, Running
    play_level_one_button = Button.PlayButton(1050, 100, "PLAY", 20, (255, 0, 0), (0, 0, 255))

    while in_menu:  # хз че тут происходит честно
        events = pygame.event.get()
        for ev in events:
            if ev.type == pygame.QUIT:
                in_menu = False
                Running = False


            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    play_level_one_button.click_check(ev.pos[0], ev.pos[1])
            elif ev.type == pygame.MOUSEBUTTONUP:
                if play_level_one_button.pressed:
                    play_level_one_button.unpress(ev.pos[0], ev.pos[1])

        CLOCK.tick(FPS)
        screen.blit(background_img, (0, 0))
        play_level_one_button.render(screen)
        pygame.display.update()
        if play_level_one_button.count > 0:
            global map_
            sock.send("give map".encode())
            data = sock.recv(2 ** 20).decode()  # получаем карту
            print(data)
            abcd = data[len(data) // 2:]
            abcd = abcd.split()
            data = data[:len(data) // 2]

            for i in range(40):
                for j in range(40):
                    map_[i][j] = abcd[i][j]
            render_map(screen, allimg, data)
            pygame.display.update()
            gameplay = True
            in_menu = False


def main_loop():  # основной гейплей
    global map_
    data = sock.recv(2 ** 20).decode()  # получаем карту
    print(data)
    abcd = data[len(data) // 2:]
    abcd = abcd.split()
    data = data[:len(data) // 2]

    for i in range(40):
        for j in range(40):
            map_[i][j] = abcd[i][j]
    render_map(screen, allimg, data)


Running = True
start_menu()
xframe, yframe = 0, 0
while Running:  # основной цикл с рендером и геймплеем
    # f.seek(0)
    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT:
            Running = False
        if ev.type == pygame.MOUSEBUTTONDOWN:  # тут нажимаются кнопочки
            if ev.button == 1:
                console_button.click_check(ev.pos[0], ev.pos[1])
                if ev.pos[0] < 800 and ev.pos[1] < 800:
                    pos_button.button_text = str(ev.pos[0] // 20) + '; ' + str(ev.pos[1] // 20) + ' ' + imginfo[
                        mapa[ev.pos[1] // 20][ev.pos[0] // 20]]
                    need_to_frame = True
                    xframe, yframe = ev.pos[0], ev.pos[1]
                    draw_frame(xframe, yframe)

        if ev.type == pygame.MOUSEBUTTONUP:
            console_button.unpress(ev.pos[0], ev.pos[1])  # консоль стала активной

        # if (pause_button.count % 2) == 1:
        #     paused = True
        # else:
        #     paused = False

        if ev.type == pygame.KEYDOWN:
            if console_button.is_active:
                if ev.key == pygame.K_RETURN:

                    sock.send(console_button.button_text.encode())  # отправляем на сервер
                    console_button.button_text = ''
                    console_button.is_active = False
                    # data = sock.recv(2 ** 20)  # получаем карту
                    # data = data.decode()
                    # out_console_button.button_text = data[3280:]

                elif ev.key == pygame.K_BACKSPACE:
                    console_button.button_text = console_button.button_text[:-1]  # стираем текст
                else:
                    console_button.button_text += ev.unicode  # добавляем текст в консоль

    CLOCK.tick(FPS)
    main_loop()
    screen.blit(interfaceimg_img, (800, 0))
    console_button.render(screen)
    pos_button.render(screen)
    out_console_button.render(screen)
    draw_boards(map_)
    draw_frame(xframe, yframe)
    # write_in_file(f)
    f = open('input.txt', 'r+')

    pygame.display.update()
pygame.quit()
f.close()
