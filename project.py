import pygame
import random

pygame.init()
size = width, height = 1100, 700
screen = pygame.display.set_mode(size)
pos = (400, 350 + 175)
pos_vrag = (400, 175)
pos_shaiba = (400, 350)
x = 0
v_x = 0
v_y = 0

schet_igr = 0
schet_comp = 0
obsh_igr = 0
obsh_comp = 0
screen.fill((57, 57, 57))


class Board:  # общий для сапера и КН (они будут унаследованы)
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):  # чертит границы клеток и закрашивает их изнутри
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, (87, 87, 87), (
                    self.left + self.cell_size * i, self.top + self.cell_size * j,
                    self.cell_size, self.cell_size), 0)
                pygame.draw.rect(screen, (20, 200, 255), (
                    self.left + self.cell_size * i, self.top + self.cell_size * j,
                    self.cell_size, self.cell_size), 1)
        # global arr
        # for i in range(len(arr)):
        #     for j in range(len(arr[i])):
        #         if arr[i][j] == 10:
        #             pygame.draw.rect(screen, pygame.Color('red'), (
        #                 self.left + self.cell_size * i, self.top + self.cell_size * j,
        #                 self.cell_size, self.cell_size), 0)
        #             pygame.display.flip()


class Minesweeper(Board):  # сапер
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = self.y = 0
        self.arr = []
        self.fool = 0
        self.opened = 0
        for i in range(height):
            a = []
            for j in range(width):
                a += [0]
            self.arr += [a]

    def drawing(self):  # закрашивает поля с минами
        global arr
        if self.fool == 1:
            for i in range(8):
                for j in range(8):
                    if arr[i][j] != 10:
                        x = 0
                        for i1 in range(pos[0] - 1, pos[0] + 2):
                            for j1 in range(pos[1] - 1, pos[1] + 2):
                                if i1 in range(len(arr)) and j1 in range(len(arr[0])) and \
                                        arr[i1][j1] == 10:
                                    x += 1
                        font = pygame.font.Font(None, 30)
                        text = font.render(str(int(x)), 1, (255, 255, 255))
                        text_x = pos[0] * self.cell_size + self.cell_size * 0.5 + self.left
                        text_y = pos[1] * self.cell_size + self.cell_size * 0.5 + self.top
                        # text_w = text.get_width()
                        # text_h = text.get_height()
                        screen.blit(text, (text_x, text_y))
                        pygame.display.flip()
                    else:
                        pygame.draw.rect(screen, (108, 52, 97), (
                            self.left + self.cell_size * i, self.top + self.cell_size * j,
                            self.cell_size, self.cell_size), 0)
                        pygame.display.flip()

    def open_cell(self, pos):  # проверка хода (проиграл или нет)
        global arr, obsh_comp, obsh_igr
        if arr[pos[0]][pos[1]] == -1:
            self.opened += 1
            x = 0
            for i in range(pos[0] - 1, pos[0] + 2):
                for j in range(pos[1] - 1, pos[1] + 2):
                    if i in range(len(arr)) and j in range(len(arr[pos[0]])) and \
                            arr[i][j] == 10:
                        x += 1
            font = pygame.font.Font(None, 30)
            text = font.render(str(int(x)), 1, (255, 255, 255))
            text_x = pos[0] * self.cell_size + self.cell_size * 0.5 + self.left
            text_y = pos[1] * self.cell_size + self.cell_size * 0.5 + self.top
            # text_w = text.get_width()
            # text_h = text.get_height()
            screen.blit(text, (text_x, text_y))
            pygame.display.flip()
            arr[pos[0]][pos[1]] = 0
            if x == 0:
                for i1 in range(pos[0] - 1, pos[0] + 2):
                    for j1 in range(pos[1] - 1, pos[1] + 2):
                        if i1 in range(0, self.width) and j1 in range(0, self.height):
                            self.open_cell((i1, j1))
        elif arr[pos[0]][pos[1]] == 10:
            self.fool = 1
            obsh_comp += 1
            self.drawing()

            # board = Minesweeper(8, 8)
            # board.set_view(150 + 500 + 40, 80 + 40, 45)
            # board.render()

        if self.opened == 8 * 8 - 8:
            obsh_igr += 1

            # board = Minesweeper(8, 8)
            # board.set_view(150 + 500 + 40, 80 + 40, 45)
            # board.render()

    def get_click(self, mouse_pos):  # запускает открытие клетки
        cell = self.get_cell(mouse_pos)
        if cell:
            self.open_cell(cell)

    def get_cell(self, mouse_pos):  # проверяет предназначен ли клик именно для сапера
        if mouse_pos[0] in range(self.left, self.left + self.height * self.cell_size) and \
                mouse_pos[1] in range(self.top, self.top + self.width * self.cell_size):
            return ((mouse_pos[0] - self.left) // self.cell_size,
                    (mouse_pos[1] - self.top) // self.cell_size)
        else:
            return None


arr = []
c = 8
a = b = 8
for i in range(8):
    x = []
    for j in range(8):
        x += [-1]
    arr += [x]
arr_1 = []
for i in range(c):
    q, w = random.choice([j for j in range(a)]), random.choice([j for j in range(b)])
    while (q, w) in arr_1:
        q, w = random.choice([j for j in range(a)]), random.choice([j for j in range(b)])
    arr[q][w] = 10
    arr_1 += [(q, w)]
board = Minesweeper(8, 8)
board.set_view(150 + 500 + 40, 80 + 40, 45)
# board.drawing()
board.render()


def draw():  # рисует игровое поле для хоккея
    # screen.fill((204, 202, 202))  # светлая тема
    # screen.fill((57, 57, 57))  # темная тема
    pygame.draw.rect(screen, (57, 57, 57), (0, 0, 150, 700), 0)
    pygame.draw.rect(screen, (57, 57, 57), (650, 0, 40, 700), 0)
    pygame.draw.rect(screen, (57, 57, 57), (650, 0, 1100, 80 + 40), 0)
    pygame.draw.rect(screen, (87, 87, 87), (150, 0, 500, 700), 0)

    # pygame.draw.rect(screen, pygame.Color(230, 230, 230), (150, 0, 500, 700), 0)
    pygame.draw.rect(screen, (197, 197, 197), (150, 340, 500, 20), 0)
    pygame.draw.circle(screen, (197, 197, 197), (400, 350), 64)
    pygame.draw.rect(screen, (255, 13, 0), (300, 680, 200, 20), 0)
    pygame.draw.rect(screen, (51, 61, 255), (300, 0, 200, 20), 0)

    font = pygame.font.Font(None, 296)
    color = (100, 255, 100)

    text = font.render("4k3s", 1, color)
    text_x = 150 + 250 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    image = pygame.Surface((text.get_width(), text.get_height()))
    image.set_alpha(75)
    pygame.draw.rect(image, (87, 87, 87), (0, 0, *text.get_size()), 0)
    image.blit(text, (0, 0))
    screen.blit(image, (text_x, text_y))
    pygame.draw.rect(screen, (140, 255, 140), (150, 0, 500, 700), 3)

    font = pygame.font.Font(None, 200)
    text = font.render(str(schet_comp), 1, (51, 61, 255))
    text_y = 20
    text_x = 20
    screen.blit(text, (text_x, text_y))

    text = font.render(str(schet_igr), 1, (255, 13, 0))
    text_y = 550
    text_x = 20
    screen.blit(text, (text_x, text_y))

    font = pygame.font.Font(None, 50)
    text = font.render("User's name: " + str(obsh_igr), 1, (100, 255, 100))
    text_y = 20
    text_x = 150 + 500 + 20
    screen.blit(text, (text_x, text_y))

    text = font.render("CompudaXter: " + str(obsh_comp), 1, (100, 255, 100))
    text_y = 20 + 40
    text_x = 150 + 500 + 20
    screen.blit(text, (text_x, text_y))


def otbit():  # проверка является ли шайба отбитой игроком или компьютером
    global v_x, v_y  # 3 easy, 2 medium, 1 hard
    if (pos[0] - pos_shaiba[0]) ** 2 + (pos[1] - pos_shaiba[1]) ** 2 <= 40 ** 2:
        v_x = (-pos[0] + pos_shaiba[0]) // 2  # <-- this chislo (1, 2 ili 2)
        v_y = (-pos[1] + pos_shaiba[1]) // 2
        # budet nastraivatsya cherez PyQT (radiobutton) + tam je imya usera + cvet usera (red or blue) + tema sv or temn
    if (pos_vrag[0] - pos_shaiba[0]) ** 2 + (pos_vrag[1] - pos_shaiba[1]) ** 2 <= 40 ** 2:
        v_x = (-pos_vrag[0] + pos_shaiba[0]) // 2
        v_y = (-pos_vrag[1] + pos_shaiba[1]) // 2


def kraya():  # отражает шайбу от краев по законам физики
    global v_y, v_x
    if pos_shaiba[0] - 20 <= 150 or pos_shaiba[0] + 20 >= 150 + 500:
        v_x *= -1
        # if v_x > 0:
        #     v_x -= 2
        # elif v_x < 0:
        #     v_x += 2
    if pos_shaiba[1] - 20 <= 0 or pos_shaiba[1] + 20 >= 700:
        v_y *= -1
        # if v_y > 0:
        #     v_y -= 2
        # elif v_y < 0:
        #     v_y += 2


def vorota():  # проверяет забита ли шайба и если да то кому именно 
    global schet_comp, schet_igr, obsh_igr, obsh_comp
    if pos_shaiba[1] - 20 in range(20) or pos_shaiba[1] + 20 in range(680, 700):
        if pos_shaiba[0] in range(150 + 150, 150 + 350):
            if pos_shaiba[1] - 20 in range(20):
                schet_igr += 1
                if schet_igr == 5:
                    obsh_igr += 1
                    schet_igr = 0
                    schet_comp = 0
            else:
                schet_comp += 1
                if schet_comp == 5:
                    obsh_comp += 1
                    schet_igr = 0
                    schet_comp = 0
            vozvrat()


def vozvrat():  # возвращает игроков и шайбу на начальные места
    global pos, pos_vrag, pos_shaiba, v_y, v_x
    pos = (400, int(350 * 1.5))
    pos_shaiba = (400, 350)
    pos_vrag = (400, 175)
    v_x = v_y = 0
    # print(schet_igr, schet_comp)


draw()
pygame.display.flip()
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            vozvrat()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    draw()
    # board.drawing()
    # board.render()
    if pygame.mouse.get_focused():
        if pygame.mouse.get_pos()[0] in range(150 + 20, 150 + 500 - 20) and pygame.mouse.get_pos()[1] in \
                range(350 + 20, 700 - 20):
            pos = pygame.mouse.get_pos()
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)
    pygame.draw.circle(screen, (255, 61, 51), pos, 20)
    pygame.draw.circle(screen, (255, 13, 0), pos, 10)
    pygame.draw.circle(screen, (51, 61, 255), pos_vrag, 20)
    pygame.draw.circle(screen, (0, 13, 255), pos_vrag, 10)
    otbit()
    kraya()
    vorota()
    pos_shaiba = (pos_shaiba[0] + v_x, pos_shaiba[1] + v_y)
    if pos_vrag[0] <= pos_shaiba[0]:
        pos_vrag = (pos_vrag[0] + int(abs(v_x * 0.8)), pos_vrag[1])
    else:
        pos_vrag = (pos_vrag[0] - int(abs(v_x * 0.8)), pos_vrag[1])
    pygame.draw.circle(screen, (100, 255, 100), pos_shaiba, 20)

    pygame.display.flip()
    clock.tick(25)
