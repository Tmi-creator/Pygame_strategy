import os
import time
import sys
import pygame

pygame.init()
import socket
import Button

my_font = 'Lato-Regular.ttf'  # шрифт
RED = (255, 50, 50)  # цвета
GREEN = (50, 255, 50)
RANGE_COLOUR = (128, 0, 128)
SPEED_COLOUR = (0, 128, 128)


# внизу классы для кнопок и окошек
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
        self.width = 250


class ConsoleButton(Button.Button):  # консоль офигеть работает
    def __init__(self, x, y, button_text, font_size=20, font_color=RED, button_color=GREEN):
        Button.Button.__init__(self, x, y, button_text, font_size, font_color, button_color)
        self.is_active = False
        self.height = 100
        self.width = 250


class ResourceButton(Button.Button):
    def __init__(self, x, y, button_text, font_size=30, font_color=RED, button_color=GREEN):
        Button.Button.__init__(self, x, y, button_text, font_size, font_color, button_color)
        self.is_active = False
        self.height = 40
        self.width = 120


class DataThings():
    def __init__(self, name, x, y, player, hp, atk=''):
        self.name = name
        self.x = x
        self.y = y
        self.player = player
        self.hp = hp
        self.atk = atk

    def destroy(self):
        self.kill()  # суецыд вы ход и те


ultralist = []

console_button = ConsoleButton(900, 600, '')  # кнопочки и окошки для отображения всего
pos_button = PosButton(820, 20, "")
out_console_button = OutConsoleButton(900, 700, '')
resource_button_turn = ResourceButton(820, 80, '')
resource_button_wood = ResourceButton(820, 130, '')
resource_button_stone = ResourceButton(820, 180, '')
resource_button_gold = ResourceButton(820, 230, '')
resource_button_platinum = ResourceButton(820, 280, '')
resource_button_metal = ResourceButton(820, 330, '')
resource_button_food = ResourceButton(820, 380, '')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.connect(('localhost', 9999))  # делоем сервер

settings = (1200, 800)  # размер окна
screen = pygame.display.set_mode(settings, pygame.RESIZABLE)  # окошко (можно выйти)
FPS = 144
CLOCK = pygame.time.Clock()

dat = sock.recv(2 ** 20)
dat = dat.decode()
print(dat)
f = open("output.txt", "w+")
f.write(dat)
f.close()  # что это за бесполезная строка? w+ же и так позволяет читать...
f = open("output.txt", "r+")
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
def load_image(name, colorkey=None):
    fullname = os.path.join(os.path.dirname(__file__), name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey:
        image.set_colorkey(colorkey)
    return image


water_img = load_image("img1/water.png")
earth_img = load_image("img1/earth.png")
forest_img = load_image("img1/forest.png")
mountain_img = load_image("img1/mountain.png")
black_earth_img = load_image("img1/black_earth.png")
cave_img = load_image("img1/cave.png")
civ_img = load_image("img1/civ.png")
plat_img = load_image("img1/plat.png")
hill_img = load_image("img1/hill.png")
all_img = load_image("img1/all.png")
cap1_img = load_image("img1/cap1.png")
cap2_img = load_image("img1/cap2.png")
# cap3_img = pygame.image.load(cap3_path).convert()
# cap4_img = pygame.image.load(cap4_path).convert()
city1_img = load_image("img1/city1.png")
city2_img = load_image("img1/city2.png")
# city3_img = pygame.image.load(city3_path).convert()
# city4_img = pygame.image.load(city4_path).convert()
tow1_img = load_image("img1/tow1.png")
tow2_img = load_image("img1/tow2.png")
# tow3_img = pygame.image.load(tow3_path).convert()
# tow4_img = pygame.image.load(tow4_path).convert()
wall1_img = load_image("img1/wall1.png")
wall2_img = load_image("img1/wall2.png")
# wall3_img = pygame.image.load(wall3_path).convert()
# wall4_img = pygame.image.load(wall4_path).convert() #картинки
background_img = load_image("img1/background_img.jpg")
interfaceimg_img = load_image("img1/interfaceimg.png")
farm1_img = load_image("img1/farm1.png")
farm2_img = load_image("img1/farm2.png")
explorer1_img = load_image("img1/explorer1.png")
explorer2_img = load_image("img1/explorer2.png")
artillery1_img = load_image("img1/artillery1.png")
artillery2_img = load_image("img1/artillery2.png")
cruiser1_img = load_image("img1/cruiser1.png")
cruiser2_img = load_image("img1/cruiser2.png")
sawmill1_img = load_image("img1/sawmill1.png")
sawmill2_img = load_image("img1/sawmill2.png")
fish_farm1_img = load_image("img1/fish_farm1.png")
fish_farm2_img = load_image("img1/fish_farm2.png")
stone_mine1_img = load_image("img1/stone_mine1.png")
stone_mine2_img = load_image("img1/stone_mine2.png")
metal_mine1_img = load_image("img1/metal_mine1.png")
metal_mine2_img = load_image("img1/metal_mine2.png")
plat_mine1_img = load_image("img1/plat_mine1.png")
plat_mine2_img = load_image("img1/plat_mine2.png")
super_mine1_img = load_image("img1/super_mine1.png")
super_mine2_img = load_image("img1/super_mine2.png")
shipyard1_img = load_image("img1/shipyard1.png")
shipyard2_img = load_image("img1/shipyard2.png")
wood_img = load_image("img1/wood.png", colorkey=(255, 255, 255))
stone_img = load_image("img1/stone.png", colorkey=(255, 255, 255))
gold_img = load_image("img1/gold.png", colorkey=(255, 255, 255))
platinum_img = load_image("img1/platinum.png", colorkey=(255, 255, 255))
metal_img = load_image("img1/metal.png", colorkey=(255, 255, 255))
food_img = load_image("img1/food.png", colorkey=(255, 255, 255))
turn_img = load_image("img1/turn.png", colorkey=(255, 255, 255))

pygame.display.set_caption("Гнег")
dict_caps = {  # внизу просто куча словарей с картинками
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

dict_explorers = {
    '1': explorer1_img,
    '2': explorer2_img
}

dict_artilleries = {
    '1': artillery1_img,
    '2': artillery2_img
}

dict_cruisers = {
    '1': cruiser1_img,
    '2': cruiser2_img
}

dict_sawmills = {
    '1': sawmill1_img,
    '2': sawmill2_img
}

dict_farms = {
    '1': farm1_img,
    '2': farm2_img
}

dict_fish_farms = {
    '1': fish_farm1_img,
    '2': fish_farm2_img
}

dict_stone_mines = {
    '1': stone_mine1_img,
    '2': stone_mine2_img
}

dict_metal_mines = {
    '1': metal_mine1_img,
    '2': metal_mine2_img
}

dict_plat_mines = {
    '1': plat_mine1_img,
    '2': plat_mine2_img
}

dict_super_mines = {
    '1': super_mine1_img,
    '2': super_mine2_img
}

dict_shipyards = {
    '1': shipyard1_img,
    '2': shipyard2_img
}

allimg = {  # картинки для всего, что стоит на карте
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
    'A': dict_caps,
    'B': dict_cities,
    'C': dict_explorers,
    'D': dict_artilleries,
    'E': dict_cruisers,
    'F': dict_sawmills,
    'G': dict_farms,
    'H': dict_fish_farms,
    'I': dict_stone_mines,
    'J': dict_metal_mines,
    'K': dict_plat_mines,
    'L': dict_super_mines,
    'M': dict_shipyards,
    'N': dict_towers
}

imginfo = {  # обозначения всего на карте
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

dict_range = {  # радиус атаки всех юнитов
    'tower': 6,
    'artillery': 7,
    'cruiser': 5,
    'explorer': 2
}

dict_speed = {  # скорость всех юнитов
    'tower': 0,
    'artillery': 2,
    'cruiser': 3,
    'explorer': 4
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
    global map_
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
#     f.close()/*/*/*/*/*/*/*/*


in_menu = True  # для запуска стартового меню
gameplay = False  # для запуска самой игры

need_to_frame = False  # для выделения клетки
need_range = False  # для радиуса атаки выделенного юнита
need_for_speed = False  # для радиуса ходьбы выбранного юнита

capital_cords = []  # для определения номера игрока
is_capital = True  # для определения постановки столицы
our_turn = -2


def resources_turn(data='0 75 0 100 0 0 100 -2'):  # тырим у сервера информацию о номере хода и наших ресурсах
    global our_turn
    our_turn = int(data[7])
    data = data.split()
    foo = 0
    if int(float(data[0])) % 2 == our_turn:
        foo = "НАШ"
    elif int(float(data[0])) % 2 == our_turn + 1 or int(float(data[0])) % 2 == our_turn - 1:
        foo = "НЕТ"
    else:
        foo = "BES"
    resource_button_turn.button_text = str(int(float(data[0]))) + " " + foo
    resource_button_wood.button_text = str(int(float(data[1])))
    resource_button_stone.button_text = str(int(float(data[2])))
    resource_button_gold.button_text = str(int(float(data[3])))
    resource_button_platinum.button_text = str(int(float(data[4])))
    resource_button_metal.button_text = str(int(float(data[5])))
    resource_button_food.button_text = str(int(float(data[6])))
    resource_button_turn.render(screen)
    resource_button_wood.render(screen)
    resource_button_stone.render(screen)
    resource_button_gold.render(screen)
    resource_button_platinum.render(screen)
    resource_button_metal.render(screen)
    resource_button_food.render(screen)
    screen.blit(turn_img, (890, 80))
    screen.blit(wood_img, (890, 130))
    screen.blit(stone_img, (890, 180))
    screen.blit(gold_img, (890, 230))
    screen.blit(platinum_img, (890, 280))
    screen.blit(metal_img, (890, 330))
    screen.blit(food_img, (890, 380))


def draw_boards(map_):  # рисуем границы государств
    colour = [(0, 255, 0), (0, 0, 255)]
    try:
        for i in range(40):
            for j in range(40):
                if int(map_[i][j]) != 0:
                    try:
                        if str(map_[i][j + 1]) != str(map_[i][j]):
                            pygame.draw.line(screen, colour[int(map_[i][j]) - 1], (j * 20 + 19, i * 20),
                                             (j * 20 + 19, i * 20 + 20), 3)
                    except:
                        pass
                    try:
                        if str(map_[i + 1][j]) != str(map_[i][j]):
                            pygame.draw.line(screen, colour[int(map_[i][j]) - 1], (j * 20, i * 20 + 19),
                                             (j * 20 + 20, i * 20 + 19), 3)
                    except:
                        pass
                    try:
                        if str(map_[i - 1][j]) != str(map_[i][j]):
                            pygame.draw.line(screen, colour[int(map_[i][j]) - 1], (j * 20, i * 20 + 1),
                                             (j * 20 + 20, i * 20 + 1), 3)
                    except:
                        pass
                    try:
                        if str(map_[i][j - 1]) != str(map_[i][j]):
                            pygame.draw.line(screen, colour[int(map_[i][j]) - 1], (j * 20 + 1, i * 20),
                                             (j * 20 + 1, i * 20 + 20), 3)
                    except:
                        pass
    except:
        print("BALBES")


def draw_frame(x, y):  # выделяем клетку, на которую нажали
    if need_to_frame:
        pygame.draw.line(screen, RED, (x // 20 * 20, y // 20 * 20), (x // 20 * 20, y // 20 * 20 + 20), 3)
        pygame.draw.line(screen, RED, (x // 20 * 20, y // 20 * 20), (x // 20 * 20 + 20, y // 20 * 20), 3)
        pygame.draw.line(screen, RED, (x // 20 * 20 + 20, y // 20 * 20), (x // 20 * 20 + 20, y // 20 * 20 + 20), 3)
        pygame.draw.line(screen, RED, (x // 20 * 20, y // 20 * 20 + 20), (x // 20 * 20 + 20, y // 20 * 20 + 20), 3)


def draw_range(x, y):  # рисуем радиус атаки выбранного юнита
    if need_range:
        pygame.draw.rect(screen, RANGE_COLOUR, (
            x - dict_range[imginfo[mapa[x, y]]], y - dict_range[imginfo[mapa[x, y]]],
            x + dict_range[imginfo[mapa[x, y]]],
            y + dict_range[imginfo[mapa[x, y]]], 3))


def draw_speed(x, y):  # рисуем границы клеток, на которые может походить выбранный юнит
    if need_for_speed:
        pygame.draw.rect(screen, SPEED_COLOUR, (
            x - dict_speed[imginfo[mapa[x, y]]], y - dict_speed[imginfo[mapa[x, y]]],
            x + dict_speed[imginfo[mapa[x, y]]],
            y + dict_speed[imginfo[mapa[x, y]]], 3))


def start_menu():  # стартовая менюшка чтобы начать игру
    global in_menu, Running
    play_level_one_button = Button.PlayButton(1050, 100, "PLAY", 20, (255, 0, 0), (0, 0, 255))

    while in_menu:  # хз че тут происходит честно
        events = pygame.event.get()  # на самом деле тут мы просто ждем, пока нажмут кнопку PLAY
        for ev in events:  # потом тут еще будет кнопка для просмотра обучения и возможно что-то еще
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
            gameplay = True
            in_menu = False
            resources_turn()


data = 0


def main_loop():  # основной гейплей
    global map_
    global mapa  # должен был быть... теперь тут только получение карты, ха-ха
    global data
    sock.send('give map'.encode())
    data = sock.recv(2 ** 20).decode()  # получаем карту
    new_data = data.split('/')
    data = new_data[0]
    # print(data)
    abcd = data[len(data) // 2:]
    abcd = abcd.split()
    data = data[:len(data) // 2]

    for i in range(40):
        for j in range(40):
            map_[i][j] = abcd[i][j]
    render_map(screen, allimg, data)

    news = new_data[1].split()
    if news:
        if news[0] == 'update':
            if news[1] == 'destroy':
                for i in ultralist:
                    if int(i.x) == int(news[2]) and int(i.y) == int(news[3]):
                        i.destroy()
            elif news[1] == 'move':
                for i in ultralist:
                    if int(i.x) == int(news[2]) and int(i.y) == int(news[3]):
                        i.x = news[4]
                        i.y = news[5]
            elif news[1] == 'attack':
                pass
            # дописать обновление хп при атаке

        else:
            ultralist.append(DataThings(*[i for i in news]))  # повыпендривались зато

    resources_turn(new_data[2])


def post_menu():  # активация при разрушении столицы
    pass


Running = True
start_menu()
xframe, yframe = 0, 0
need_main_loop = 0
while Running:  # основной цикл с рендером и геймплеем
    need_main_loop += 1

    # f.seek(0)
    events = pygame.event.get()
    for ev in events:
        if ev.type == pygame.QUIT:
            Running = False
        if ev.type == pygame.MOUSEBUTTONDOWN:  # тут нажимаются кнопочки

            if ev.button == 1:
                console_button.click_check(ev.pos[0], ev.pos[1])
                if ev.pos[0] < 800 and ev.pos[1] < 800:
                    data1 = None
                    for i in ultralist:
                        if int(i.y) == ev.pos[0] // 20 and int(i.x) == ev.pos[1] // 20:
                            data1 = i
                            break
                    if data1:
                        data1.x, data1.y = data1.y, data1.x
                        if data1.atk == '':
                            pos_button.button_text = data1.name + ' ' + data1.x + "; " + data1.y + " " + data1.player + ' ' + data1.hp
                        else:
                            pos_button.button_text = data1.name + ' ' + data1.x + "; " + data1.y + " " + data1.player + ' ' + data1.hp + " " + data1.atk
                            draw_range(int(data1.x), int(data1.y))
                            draw_speed(int(data1.x), int(data1.y))

                    else:
                        pos_button.button_text = str(ev.pos[0] // 20) + '; ' + str(ev.pos[1] // 20) + ' ' + imginfo[
                            mapa[ev.pos[1] // 20][ev.pos[0] // 20]]
                    need_to_frame = True
                    xframe, yframe = ev.pos[0], ev.pos[1]
                    render_map(screen, allimg, data)
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
                    sock.send((console_button.button_text + " ").encode())  # отправляем на сервер
                    if is_capital:
                        temp = console_button.button_text.split()
                        capital_cords = [temp[1], temp[2]]
                        is_capital = False

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
    if need_main_loop == 5:
        screen.blit(interfaceimg_img, (800, 0))
        main_loop()
        need_main_loop = 0
        draw_frame(xframe, yframe)
    console_button.render(screen)
    pos_button.render(screen)
    out_console_button.render(screen)
    draw_boards(map_)

    # write_in_file(f)

    pygame.display.update()
pygame.quit()
f.close()
