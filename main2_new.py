import Button
import os
import pygame
import socket
import sys
import time
import random
from oop import *

pygame.init()

buildings = [Capital(-100, -100, 0), City(-100, -100, 0), Sawmill(-100, -100, 0), Farm(-100, -100, 0),
             FishFarm(-100, -100, 0), StoneMine(-100, -100, 0), MetalMine(-100, -100, 0), PlatinumMine(-100, -100, 0),
             SuperMine(-100, -100, 0), Shipyard(-100, -100, 0),
             Tower(-100, -100, 0), Cruiser(-100, -100, 0), Explorer(-100, -100, 0), Artillery(-100, -100, 0),
             Wall(-100, -100, 0)]
my_font = 'Lato-Regular.ttf'  # шрифт
RED = (255, 50, 50)  # цвета
GREEN = (50, 255, 50)  # зелененька
RANGE_COLOUR = (128, 0, 128)  # какое то
SPEED_COLOUR = (0, 128, 128)  # другое
recources = [0, 0, 0, 0, 0, 0]


# внизу классы для кнопок и окошек
class PosButton(Button.Button):  # координаты выбранной клетки
    def __init__(self, x, y, button_text, font_size=30, font_color=RED, button_color=GREEN):
        Button.Button.__init__(self, x, y, button_text, font_size, font_color, button_color)
        self.is_active = False
        self.height = 40
        self.width = 370


class OutConsoleButton(Button.Button):
    def __init__(self, x, y, button_text, font_size=18, font_color=RED, button_color=GREEN):
        Button.Button.__init__(self, x, y, button_text, font_size, font_color, button_color)
        self.is_active = False
        self.height = 30
        self.width = 350
        self.dark_color = self.button_color


class ConsoleButton(Button.Button):  # консоль офигеть работает
    def __init__(self, x, y, button_text, font_size=18, font_color=RED, button_color=GREEN):
        Button.Button.__init__(self, x, y, button_text, font_size, font_color, button_color)
        self.is_active = False
        self.height = 100
        self.width = 350


class ResourceButton(Button.Button):  # для отображения ресурсов
    def __init__(self, x, y, button_text, font_size=30, font_color=RED, button_color=GREEN):
        Button.Button.__init__(self, x, y, button_text, font_size, font_color, button_color)
        self.is_active = False
        self.height = 40
        self.width = 120


class BuildButton(Button.Button):  # для отображения ресурсов
    def __init__(self, x, y, button_text, command='place capital 2 5', name='', font_size=30, font_color=RED,
                 button_color=GREEN):
        Button.Button.__init__(self, x, y, button_text, font_size, font_color, button_color)
        self.is_active = False
        self.height = 40
        self.width = 40
        self.command = command
        self.cnt = 0
        self.name = name

    def use(self, x, y, button, button1, button2, descriptions, costs):
        button.button_text = descriptions[self.name].split('\n')[0]
        try:
            button1.button_text = descriptions[self.name].split('\n')[1]
        except:
            pass
        button2.button_text = costs[self.name]
        self.cnt += 1

        if self.cnt % 2 == 0:
            self.command = 'READY' + self.command[:6] + str(x) + ' ' + str(y) + ' ' + self.command[7:]
            button.button_text = ''
            button1.button_text = ''
            button2.button_text = ''

    def unuse(self):
        self.cnt = 0

    def unpress(self, click_x, click_y, super_x, super_y, button, button1, button2, descriptions, costs):
        self.pressed = False
        if self.x <= click_x <= self.x + self.width and self.y + self.height >= click_y >= self.y and self.active:
            self.use(super_x // 20, super_y // 20, button, button1, button2, descriptions, costs)
        else:
            self.unuse()


class AtkButton(Button.Button):
    def __init__(self, x, y, button_text='Attack', command='attack ', name='', font_size=30, font_color=(255, 255, 255),
                 button_color=RED):
        Button.Button.__init__(self, x, y, button_text, font_size, font_color, button_color)

        self.is_active = False
        self.height = 40
        self.width = 120
        self.command = command
        self.name = name
        self.click_again = 0
        self.info = []

    def use(self, name, x, y):
        if (self.click_again == 1): self.info = []
        self.info.append(name)
        self.info.append(str(x))
        self.info.append(str(y))

        if self.click_again == 2:
            self.info = [str(i) for i in self.info]
            self.command = 'READY' + self.command + self.info[0] + ' ' + self.info[1] + ' ' + self.info[2] + ' ' + \
                           self.info[3] + ' ' + self.info[4] + ' ' + self.info[5]
            self.click_again = 0

    def unpress(self, click_x, click_y, name, x, y):
        self.pressed = False
        if self.x <= click_x <= self.x + self.width and self.y + self.height >= click_y >= self.y and self.active:
            self.click_again += 1
            self.use(name, x, y)


class MoveButton(Button.Button):
    def __init__(self, x, y, button_text='Move', command='move ', name='', font_size=30, font_color=(255, 255, 255),
                 button_color=(135, 206, 250)):
        Button.Button.__init__(self, x, y, button_text, font_size, font_color, button_color)

        self.is_active = False
        self.height = 40
        self.width = 120
        self.command = command
        self.name = name
        self.click_again = 0
        self.info = []

    def use(self, name, x, y):
        if (self.click_again == 1): self.info = []
        self.info.append(name)
        self.info.append(str(x))
        self.info.append(str(y))
        if self.click_again == 2:
            self.info = [str(i) for i in self.info]
            self.command = 'READY' + self.command + self.info[0] + ' ' + self.info[1] + ' ' + self.info[2] + ' ' + \
                           self.info[4] + ' ' + self.info[5]
            self.click_again = 0

    def unpress(self, click_x, click_y, name, x, y):
        self.pressed = False
        if self.x <= click_x <= self.x + self.width and self.y + self.height >= click_y >= self.y and self.active:
            self.click_again += 1
            self.use(name, x, y)


class RelaxButton(Button.Button):
    def __init__(self, x, y, button_text='Stop all', command='', name='', font_size=30, font_color=(255, 255, 255),
                 button_color=(77, 77, 77)):
        Button.Button.__init__(self, x, y, button_text, font_size, font_color, button_color)

        self.is_active = False
        self.height = 40
        self.width = 120
        self.command = command
        self.name = name

    def use(self, atk_button, move_button):
        try:
            atk_button.click_again = 0
            move_button.click_again = 0
        except:
            pass

    def unpress(self, click_x, click_y, atk_button, move_button):
        self.pressed = False
        if self.x <= click_x <= self.x + self.width and self.y + self.height >= click_y >= self.y and self.active:
            self.use(atk_button, move_button)


class DataThings():  # для хранения всего
    def __init__(self, name, x, y, player, hp, atk=''):
        self.name = name
        self.x = x
        self.y = y
        self.player = player
        self.hp = hp
        self.atk = atk


screen_rect = (0, 0, 1200, 800)


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


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("img1/star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 0.1

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


ultralist = []  # супер штука но забыл зачем она

console_button = ConsoleButton(820, 600, '')  # кнопочки и окошки для отображения всего
pos_button = PosButton(820, 20, "")
out_console_button = OutConsoleButton(820, 700, '')
out_console_button_2 = OutConsoleButton(820, 730, '')
out_console_button_cost = OutConsoleButton(820, 760, '')
resource_button_turn = ResourceButton(820, 80, '')
resource_button_wood = ResourceButton(820, 130, '')
resource_button_stone = ResourceButton(820, 180, '')
resource_button_gold = ResourceButton(820, 230, '')
resource_button_platinum = ResourceButton(820, 280, '')
resource_button_metal = ResourceButton(820, 330, '')
resource_button_food = ResourceButton(820, 380, '')

build_button_capital = BuildButton(980, 80, '1', 'place  capital', 'capital')
build_button_city = BuildButton(1040, 80, '2', 'place  city', 'city')
build_button_sawmill = BuildButton(980, 130, '3', 'place  sawmill', 'sawmill')
build_button_farm = BuildButton(1040, 130, '4', 'place  farm', 'farm')
build_button_fish_farm = BuildButton(980, 180, '5', 'place  fish_farm', 'fish_farm')
build_button_stone_mine = BuildButton(1040, 180, '6', 'place  stone_mine', 'stone_mine')
build_button_metal_mine = BuildButton(980, 230, '7', 'place  metal_mine', 'metal_mine')
build_button_platinum_mine = BuildButton(1040, 230, '8', 'place  plat_mine', 'plat_mine')
build_button_super_mine = BuildButton(980, 280, '9', 'place  super_mine', 'super_mine')
build_button_shipyard = BuildButton(1040, 280, 'a', 'place  shipyard', 'shipyard')
build_button_tower = BuildButton(980, 330, 'b', 'place  tower', 'tower')
build_button_explorer = BuildButton(1040, 330, 'c', ' unit  explorer', 'explorer')
build_button_artillery = BuildButton(980, 380, 'd', ' unit  artillery', 'artillery')
build_button_cruiser = BuildButton(1040, 380, 'e', ' unit  cruiser', 'cruiser')
build_button_wall = BuildButton(980, 430, 'f', 'place  wall', 'wall')

move_button = MoveButton(850, 430)
atk_button = AtkButton(871, 480)  # переделать прием команды в сервере upd уже все норм (ничего не поменялось)
relax_button = RelaxButton(889, 530)

build_button_list = [build_button_capital, build_button_city, build_button_sawmill, build_button_farm,
                     build_button_fish_farm,
                     build_button_stone_mine, build_button_metal_mine, build_button_platinum_mine,
                     build_button_super_mine, build_button_shipyard, build_button_tower,
                     build_button_explorer, build_button_artillery, build_button_cruiser, build_button_wall]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.connect(('localhost', 9999))  # делоем сервер

settings = (1200, 800)  # размер окна
screen = pygame.display.set_mode(settings, pygame.RESIZABLE)  # окошко (можно выйти)
FPS = 144
CLOCK = pygame.time.Clock()

dat = sock.recv(2 ** 20)
dat = dat.decode()
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


butcap1 = load_image("img1/butcap1.png")
butcap2 = load_image("img1/butcap2.png")
butcity1 = load_image("img1/butcity1.png")
butcity2 = load_image("img1/butcity2.png")  # мега мем: мы забыли добавить
butfarm1 = load_image("img1/butfarm1.png")  # стены в обозначения и кнопки
butfarm2 = load_image("img1/butfarm2.png")
butfish_farm1 = load_image("img1/butfishfarm1.png")
butfish_farm2 = load_image("img1/butfishfarm2.png")
butmetal_mine1 = load_image("img1/butmetal_mine1.png")
butmetal_mine2 = load_image("img1/butmetal_mine2.png")
butstone_mine1 = load_image("img1/butstone_mine1.png")
butstone_mine2 = load_image("img1/butstone_mine2.png")
butsuper_mine1 = load_image("img1/butsuper_mine1.png")
butsuper_mine2 = load_image("img1/butsuper_mine2.png")
butshipyard1 = load_image("img1/butshipyard1.png")
butshipyard2 = load_image("img1/butshipyard2.png")
butsawmill1 = load_image("img1/butsawmill1.png")
butsawmill2 = load_image("img1/butsawmill2.png")
butplat_mine1 = load_image("img1/butplat_mine1.png")
butplat_mine2 = load_image("img1/butplat_mine2.png")
butcruiser1 = load_image("img1/butcruiser1.png")
butcruiser2 = load_image("img1/butcruiser2.png")
butartillery1 = load_image("img1/butartillery1.png")
butartillery2 = load_image("img1/butartillery2.png")
butexplorer1 = load_image("img1/butexplorer1.png")
butexplorer2 = load_image("img1/butexplorer2.png")
buttow1 = load_image("img1/buttow1.png")
buttow2 = load_image("img1/buttow2.png")
butwall1 = load_image("img1/butwall1.png")
butwall2 = load_image("img1/butwall2.png")

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

dict_shipyards = {  # словарь картинок верфей
    '1': shipyard1_img,
    '2': shipyard2_img
}

buttons222 = [butcap2, butcity2, butsawmill2, butfarm2, butfish_farm2, butstone_mine2, butmetal_mine2, butplat_mine2,
              butsuper_mine2,
              butshipyard2, buttow2, butexplorer2, butartillery2, butcruiser2, butwall2]
buttons111 = [butcap1, butcity1, butsawmill1, butfarm1, butfish_farm1, butstone_mine1, butmetal_mine1, butplat_mine1,
              butsuper_mine1,
              butshipyard1, buttow1, butexplorer1, butartillery1, butcruiser1, butwall1]
superdict_butbuildings111 = {
    1: buttons111,
    2: buttons222
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
    'N': dict_towers,
    'O': dict_walls
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
    'E': 'cruiser',
    'F': 'sawmill',
    'G': 'farm',
    'H': 'fish_farm',
    'I': 'stone_mine',
    'J': 'metal_mine',
    'K': 'platinum_mine',
    'L': "super_mine",
    'M': "shipyard",
    'N': 'tower',
    'O': 'wall'
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
descriptions = {  # описание зданий и юнтов в кнопках
    'capital': 'main building. should be placement not in\ncenter gives +50 gold and -10 food per turn\n',
    'city': 'gives some territory to you(5x5)\ngives +25 gold and -5 food per turn\n',
    'explorer': 'gives some dynamic territory (3x3)\n can be used to build something at other island\n',
    'artillery': 'attacks enemies at high range\n',
    'cruiser': 'attaks enemies at middle range\n',
    'sawmill': 'produces wood.\ngives +25 wood and -5 gold per turn\n',
    'farm': 'produces food. more than fish farm\n',
    'fish_farm': 'produces food. less than normal farm\n',
    'stone_mine': 'produces stone\n',
    'metal_mine': 'produces metal\n',
    'plat_mine': 'produces platinum\n',
    'super_mine': 'produces all!\n',
    'shipyard': 'with it you can build units nearby\n',
    'tower': 'automaticly attacks nearest enemies\n',
    'wall': 'they shall not pass!\n'
}

costs = {  # цены в кнопках
    'capital': 'absolutely free',
    'city': '100 wood and 100 gold',
    'explorer': '200 wood and 250 gold',
    'artillery': '50 wood and 350 gold and 200 metal',
    'cruiser': '50 wood and 150 gold and 100 metal',
    'sawmill': '50 wood and 75 gold',
    'farm': '150 wood and 50 gold',
    'fish_farm': '50 wood and 75 gold',
    'stone_mine': '125 wood and 75 gold',
    'metal_mine': '200 wood and 200 gold',
    'plat_mine': '200 wood and 300 gold',
    'super_mine': '200 wood and 250 gold',
    'shipyard': '150 wood and 350 gold',
    'tower': '150 wood and 150 gold',
    'wall': '50 wood and 50 gold'
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


def proverka_na_port(i, x, y):  # ставить корабли только около верфи, подсветка кнопок
    true1 = False
    try:
        true1 += (mapa[x - 1][y] == 'M')
    except:
        pass
    try:
        true1 += (mapa[x + 1][y] == 'M')
    except:
        pass
    try:
        true1 += (mapa[x][y - 1] == 'M')
    except:
        pass
    try:
        true1 += (mapa[x][y + 1] == 'M')
    except:
        pass
    if not true1:
        build_button_list[i].dark_color = (255, 0, 0)
        build_button_list[i].button_color = (255, 0, 0)
    else:
        build_button_list[i].dark_color = (233, 150, 122)
        build_button_list[i].button_color = (233, 150, 122)


def ultra_render_interface111(screen, x, y):  # ультра рендер интерфейс111
    x, y = y, x
    global superdict_butbuildigs111  # словарь кнопок
    for i in range(len(buildings)):  # подсветка кнопок
        is_port = False
        if (10 < i < 14):  # units
            proverka_na_port(i, x, y)  #
            if build_button_list[i].dark_color == (255, 0, 0):
                is_port = True

        if is_port or mapa[x][y] not in buildings[i].landscape or int(map_[x][y]) != 1 + int(our_turn):
            build_button_list[i].dark_color = (255, 0, 0)
            build_button_list[i].button_color = (255, 0, 0)
        else:
            if len(buildings[i].cost) == 3:
                if buildings[i].cost[0] <= recources[0] and buildings[i].cost[1] <= recources[2] and buildings[i].cost[
                    2] <= recources[4]:
                    build_button_list[i].dark_color = (0, 255, 0)
                    build_button_list[i].button_color = (0, 255, 0)
                else:
                    build_button_list[i].dark_color = (233, 150, 122)
                    build_button_list[i].button_color = (233, 150, 122)
            elif len(buildings[i].cost) == 2:
                if buildings[i].cost[0] <= recources[0] and buildings[i].cost[1] <= recources[2]:
                    build_button_list[i].dark_color = (0, 255, 0)
                    build_button_list[i].button_color = (0, 255, 0)
                else:
                    build_button_list[i].dark_color = (233, 150, 122)
                    build_button_list[i].button_color = (233, 150, 122)
            else:
                if mapa[x][y] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    build_button_list[i].dark_color = (255, 0, 0)
                    build_button_list[i].button_color = (255, 0, 0)
                else:
                    build_button_list[i].dark_color = (0, 255, 0)
                    build_button_list[i].button_color = (0, 255, 0)
        build_button_list[i].button_color_pressed = list(
            map(lambda i: (i + 70 if i <= 185 else 255), build_button_list[i].button_color))
        build_button_list[i].dark_color_pressed = list(
            map(lambda i: (i + 70 if i <= 185 else 255), build_button_list[i].dark_color))
    kushaem_kashu = True

    for i in range(5):
        for j in range(5):
            if int(map_[(x + i - 2) % 40][(y + j - 2) % 40]) != 0:
                kushaem_kashu = False
    if not (mapa[x][y] in buildings[0].landscape and len(ultralist) < 2 and kushaem_kashu and not (
            15 < x < 26 or 15 < y < 26)):
        build_button_list[0].dark_color = (255, 0, 0)
        build_button_list[0].button_color = (255, 0, 0)
    else:
        build_button_list[0].dark_color = (0, 255, 0)
        build_button_list[0].button_color = (0, 255, 0)

    build_button_list[0].button_color_pressed = list(
        map(lambda i: (i + 70 if i <= 185 else 255), build_button_list[0].button_color))
    build_button_list[0].dark_color_pressed = list(
        map(lambda i: (i + 70 if i <= 185 else 255), build_button_list[0].dark_color))

    build_button_capital.render(screen)  # куча кнопок (рендерится)
    build_button_city.render(screen)
    build_button_sawmill.render(screen)
    build_button_farm.render(screen)
    build_button_fish_farm.render(screen)
    build_button_stone_mine.render(screen)
    build_button_metal_mine.render(screen)
    build_button_platinum_mine.render(screen)
    build_button_super_mine.render(screen)
    build_button_shipyard.render(screen)
    build_button_tower.render(screen)
    build_button_explorer.render(screen)
    build_button_artillery.render(screen)
    build_button_cruiser.render(screen)
    build_button_wall.render(screen)
    build_button_cruiser.render(screen)

    screen.blit(superdict_butbuildings111[our_turn + 1][0], (960, 80))
    screen.blit(superdict_butbuildings111[our_turn + 1][1], (1020, 80))
    screen.blit(superdict_butbuildings111[our_turn + 1][2], (960, 130))
    screen.blit(superdict_butbuildings111[our_turn + 1][3], (1020, 130))
    screen.blit(superdict_butbuildings111[our_turn + 1][4], (960, 180))
    screen.blit(superdict_butbuildings111[our_turn + 1][5], (1020, 180))
    screen.blit(superdict_butbuildings111[our_turn + 1][6], (960, 230))
    screen.blit(superdict_butbuildings111[our_turn + 1][7], (1020, 230))
    screen.blit(superdict_butbuildings111[our_turn + 1][8], (960, 280))
    screen.blit(superdict_butbuildings111[our_turn + 1][9], (1020, 280))
    screen.blit(superdict_butbuildings111[our_turn + 1][10], (960, 330))
    screen.blit(superdict_butbuildings111[our_turn + 1][11], (1020, 330))
    screen.blit(superdict_butbuildings111[our_turn + 1][12], (960, 380))
    screen.blit(superdict_butbuildings111[our_turn + 1][13], (1020, 380))
    screen.blit(superdict_butbuildings111[our_turn + 1][14], (960, 430))


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
our_turn = -2  # чтобы знать который ход наш


def resources_turn(data='0 75 0 100 0 0 100 -2'):  # тырим у сервера информацию о номере хода и наших ресурсах и рисуем
    global our_turn, recources

    data = data.split()
    recources = [int(float(data[i])) for i in range(1, 7)]
    our_turn = int(data[7])
    if our_turn > 1000:
        our_turn = 0
    foo = 0
    if int(float(data[0])) % 2 == our_turn:  # про ход и не задерживайся
        foo = "НАШ"
    elif int(float(data[0])) % 2 == our_turn + 1 or int(float(data[0])) % 2 == our_turn - 1:
        foo = "НЕТ"
    else:
        foo = "КТО"
    resource_button_turn.button_text = str(int(float(data[0]))) + " " + foo  # опять куча кнопок
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
    build_button_cruiser.render(screen)
    screen.blit(turn_img, (890, 80))
    screen.blit(wood_img, (890, 130))
    screen.blit(stone_img, (890, 180))
    screen.blit(gold_img, (890, 230))
    screen.blit(platinum_img, (890, 280))
    screen.blit(metal_img, (890, 330))
    screen.blit(food_img, (890, 380))


def draw_boards(map_):  # рисуем границы государств
    colour = [(196, 30, 58), (0, 0, 255)]
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
        pass


def draw_kvadrat(x, y, x1, y1, wdt, colour):  # инвалидное рисование квадрата через 4 линии
    if x < 0:
        pygame.draw.line(screen, colour, (0, y), (x1, y), wdt)
        pygame.draw.line(screen, colour, (0, y1), (x1, y1), wdt)
        x += 800
        pygame.draw.line(screen, colour, (x, y), (800, y), wdt)
        pygame.draw.line(screen, colour, (x, y1), (800, y1), wdt)
        x -= 800
    elif x1 > 800:
        pygame.draw.line(screen, colour, (x, y), (800, y), wdt)
        pygame.draw.line(screen, colour, (x, y1), (800, y1), wdt)
        x1 -= 800
        pygame.draw.line(screen, colour, (0, y), (x1, y), wdt)
        pygame.draw.line(screen, colour, (0, y1), (x1, y1), wdt)
        x1 += 800
    else:
        pygame.draw.line(screen, colour, (x, y), (x1, y), wdt)
        pygame.draw.line(screen, colour, (x, y1), (x1, y1), wdt)

    if y < 0:
        pygame.draw.line(screen, colour, (x, 0), (x, y1), wdt)
        pygame.draw.line(screen, colour, (x1, 0), (x1, y1), wdt)
        y += 800
        pygame.draw.line(screen, colour, (x, y), (x, 800), wdt)
        pygame.draw.line(screen, colour, (x1, y), (x1, 800), wdt)
    elif y1 > 800:
        pygame.draw.line(screen, colour, (x, y), (x, 800), wdt)
        pygame.draw.line(screen, colour, (x1, y), (x1, 800), wdt)
        y1 -= 800
        pygame.draw.line(screen, colour, (x, 0), (x, y1), wdt)
        pygame.draw.line(screen, colour, (x1, 0), (x1, y1), wdt)
    else:
        pygame.draw.line(screen, colour, (x, y), (x, y1), wdt)
        pygame.draw.line(screen, colour, (x1, y), (x1, y1), wdt)

    if x < 0:
        pygame.draw.line(screen, colour, (0, y), (x1, y), wdt)
        pygame.draw.line(screen, colour, (0, y1), (x1, y1), wdt)
        x += 800
        pygame.draw.line(screen, colour, (x, y), (800, y), wdt)
        pygame.draw.line(screen, colour, (x, y1), (800, y1), wdt)
    elif x1 > 800:
        pygame.draw.line(screen, colour, (x, y), (800, y), wdt)
        pygame.draw.line(screen, colour, (x, y1), (800, y1), wdt)
        x1 -= 800
        pygame.draw.line(screen, colour, (0, y), (x1, y), wdt)
        pygame.draw.line(screen, colour, (0, y1), (x1, y1), wdt)
    else:
        pygame.draw.line(screen, colour, (x, y), (x1, y), wdt)
        pygame.draw.line(screen, colour, (x, y1), (x1, y1), wdt)


def draw_frame(x, y):  # выделяем клетку, на которую нажали
    if need_to_frame:
        draw_kvadrat(x // 20 * 20, y // 20 * 20, x // 20 * 20 + 20, y // 20 * 20 + 20, 3, RED)


def draw_range(x, y):  # рисуем радиус атаки выбранного юнита
    if need_range:
        x, y = int(y), int(x)
        super_range = dict_range[imginfo[mapa[x // 20][y // 20]]] * 20
        x, y = y, x
        draw_kvadrat(x - super_range, y - super_range, x + super_range + 20, y + super_range + 20, 3, RANGE_COLOUR)


def draw_speed(x, y):  # рисуем границы клеток, на которые может походить выбранный юнит
    if need_for_speed:  # ржать тут
        x, y = int(y), int(x)
        super_speed = dict_speed[imginfo[mapa[x // 20][y // 20]]] * 20
        x, y = y, x
        draw_kvadrat(x - super_speed, y - super_speed, x + super_speed + 20, y + super_speed + 20, 3, SPEED_COLOUR)


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
Running = True


def main_loop():  # основной гейплей
    global map_
    global mapa  # должен был быть... теперь тут только получение карты, ха-ха
    global data
    # sock.send('give map'.encode()) # это нам больше не нужно
    data = sock.recv(2 ** 20).decode()  # получаем карту
    if data == 'you win':
        post_menu_fun()
    if data == 'you lose':
        post_menu_unfun()
    new_data = data.split('/')
    data = new_data[0]
    abcd = data[len(data) // 2:]
    abcd = abcd.split()
    data = data[:len(data) // 2]

    for i in range(40):
        for j in range(40):
            map_[i][j] = abcd[i][j]
    render_map(screen, allimg, data)

    news = new_data[1].split()

    if news:
        print(news)
        if news[0] == 'update':
            if news[1] == 'destroy':
                for i in ultralist:
                    if int(i.x) == int(news[2]) and int(i.y) == int(news[3]):
                        ultralist.remove(i)
            elif news[1] == 'move':
                for i in ultralist:
                    if int(i.x) == int(news[2]) and int(i.y) == int(news[3]):
                        i.x = news[4]
                        i.y = news[5]
            elif news[1] == 'attack':
                for i in ultralist:
                    if int(i.x) == int(news[2]) and int(i.y) == int(news[3]):
                        i.hp = news[4]
        else:
            ultralist.append(DataThings(*[i for i in news]))  # повыпендривались зато

    resources_turn(new_data[2])


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def post_menu_fun():  # активация при разрушении столицы
    global Running
    x = 0
    while Running:
        if (x % 50 == 0):
            create_particles((100, 100))
            create_particles((1000, 600))
            create_particles((600, 400))
            create_particles((100, 600))
            create_particles((1000, 100))
        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        CLOCK.tick(50)
        if x == 50 * 20:
            Running = False
    exit(0)


def post_menu_unfun():
    global Running
    x = 0
    while Running:
        if (x % 50 == 0):
            create_particles((100, 100))
            create_particles((1000, 600))
            create_particles((600, 400))
            create_particles((100, 600))
            create_particles((1000, 100))
        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        CLOCK.tick(50)
        if x == 50 * 20:
            Running = False
    exit(0)


start_menu()
xframe, yframe = 0, 0
need_main_loop = 0
draw_frame(xframe, yframe)
data1 = 0
all_sprites = pygame.sprite.Group()
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
                for button in build_button_list:
                    button.click_check(ev.pos[0], ev.pos[1])
                atk_button.click_check(ev.pos[0], ev.pos[1])
                move_button.click_check(ev.pos[0], ev.pos[1])
                relax_button.click_check(ev.pos[0], ev.pos[1])
                if ev.pos[0] < 800 and ev.pos[1] < 800:
                    data1 = None
                    for i in ultralist:
                        if int(i.y) == ev.pos[0] // 20 and int(i.x) == ev.pos[1] // 20:
                            data1 = i
                            break
                    if data1:
                        if data1.atk == '':
                            need_range = False
                            need_for_speed = False
                            pos_button.button_text = data1.name + ' ' + data1.y + "; " + data1.x + " " + data1.player + ' ' + data1.hp
                        else:
                            need_range = True
                            need_for_speed = True
                            pos_button.button_text = data1.name + ' ' + data1.y + "; " + data1.x + " " + data1.player + ' ' + data1.hp + " " + data1.atk
                    else:
                        pos_button.button_text = str(ev.pos[0] // 20) + '; ' + str(ev.pos[1] // 20) + ' ' + imginfo[
                            mapa[ev.pos[1] // 20][ev.pos[0] // 20]]
                    need_to_frame = True
                    xframe, yframe = ev.pos[0], ev.pos[1]
                    render_map(screen, allimg, data)
                    draw_frame(xframe, yframe)
                    ultra_render_interface111(screen, ev.pos[0] // 20, ev.pos[1] // 20)

        if ev.type == pygame.MOUSEBUTTONUP:

            console_button.unpress(ev.pos[0], ev.pos[1])  # консоль стала активной
            for button in build_button_list:
                button.unpress(ev.pos[0], ev.pos[1], xframe, yframe, out_console_button, out_console_button_2,
                               out_console_button_cost, descriptions, costs)
                if button.command[:5] == 'READY':
                    sock.send(button.command[5:].encode())
                    temp = button.command[5:].split()
                    if temp[0] == 'place':
                        button.command = temp[0] + '  ' + temp[3]
                    elif temp[0] == 'unit':
                        button.command = ' ' + temp[0] + '  ' + temp[3]
            try:
                try:
                    atk_button.unpress(ev.pos[0], ev.pos[1], data1.name, int(data1.x), int(data1.y))
                except:
                    pass
                try:
                    move_button.unpress(ev.pos[0], ev.pos[1], data1.name, int(data1.x), int(data1.y))
                except:
                    move_button.unpress(ev.pos[0], ev.pos[1], 'balbes', int(yframe) // 20, int(xframe) // 20)
            except:
                atk_button.pressed = False
                move_button.pressed = False

            relax_button.unpress(ev.pos[0], ev.pos[1], atk_button, move_button)
            if atk_button.command[:5] == 'READY':
                sock.send(atk_button.command[5:].encode())
                atk_button.command = 'attack '

            if move_button.command[:5] == 'READY':
                sock.send(move_button.command[5:].encode())
                move_button.command = 'move '

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
        try:
            draw_range(int(data1.y) * 20, int(data1.x) * 20)
            draw_speed(int(data1.y) * 20, int(data1.x) * 20)  # ацтань уже спать пора
        except:
            pass

        ultra_render_interface111(screen, xframe // 20, yframe // 20)
    console_button.render(screen)
    pos_button.render(screen)
    out_console_button.render(screen)
    out_console_button_2.render(screen)
    out_console_button_cost.render(screen)
    move_button.render(screen)
    atk_button.render(screen)
    relax_button.render(screen)
    draw_boards(map_)

    # write_in_file(f)

    pygame.display.update()
pygame.quit()
f.close()
