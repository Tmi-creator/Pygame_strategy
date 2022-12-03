import pygame

my_font = 'Lato-Regular.ttf'
RED = (255, 50, 50)
GREEN = (50, 255, 50)


class Button:
    def __init__(self, x, y, button_text, font_size=20, font_color=RED, button_color=GREEN, font_style=my_font):
        self.button_text = button_text
        self.font_size = font_size
        if len(self.button_text) > 20:
            self.width = len(self.button_text) * self.font_size * 0.45 + 4
        elif len(self.button_text) > 4:
            self.width = len(self.button_text) * self.font_size * 0.6 + 4
        else:
            self.width = len(self.button_text) * self.font_size * 0.5 + 10
        self.x = x - (self.width / 2)
        self.y = y
        self.font_style = font_style
        self.button_color = button_color
        self.dark_color = list(map(lambda i: i / 2, button_color))
        self.button_color_pressed = list(map(lambda i: (i + 70 if i <= 185 else 255), button_color))
        self.dark_color_pressed = list(map(lambda i: (i + 70 if i <= 185 else 255), self.dark_color))

        self.font_color = font_color

        self.height = self.font_size + 3
        self.active = True
        self.pressed = False

        pygame.font.init()

        self.font = pygame.font.Font(font_style, font_size)

    def render(self, screen):
        if not self.pressed:
            pygame.draw.rect(screen, self.dark_color, (self.x - 11, self.y - 5, self.width + 10, self.height + 10))

            pygame.draw.rect(screen, self.button_color, (self.x - 6, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.dark_color_pressed,
                             (self.x - 7, self.y - 6, self.width + 10, self.height + 10))
            pygame.draw.rect(screen, self.button_color_pressed, (self.x - 2, self.y - 1, self.width, self.height))
        screen.blit(self.font.render(self.button_text, 0, self.font_color), (self.x, self.y))

    def click_check(self, click_x, click_y):
        # if click_x >= self.x and click_y <= self.y + self.height and click_y  >= self.y and click_x <= self.x +
        # self.width and self.active == True:

        if self.x <= click_x <= self.x + self.width and self.y + self.height >= click_y >= self.y and self.active:
            self.pressed = True

    def unpress(self, click_x, click_y):
        self.pressed = False
        if self.x <= click_x <= self.x + self.width and self.y + self.height >= click_y >= self.y and self.active:
            self.use()

    def use(self):
        self.is_active = True
        print('is active')


class PlayButton(Button):
    def __init__(self, x, y, button_text, font_size=20, font_color=RED, button_color=GREEN):
        Button.__init__(self, x, y, button_text, font_size, font_color, button_color)
        self.count = 0

    def use(self):
        self.count += 1


