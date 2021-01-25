import os
import sys
import pygame

pygame.init()

# ???? повторяет рисунок уровня бесконечно при смещении персонажа за пределы размеров уровня
pygame.key.set_repeat(200, 70)
WIDTH = 720
HEIGHT = 720
STEP = 8

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

STEPTIMER = pygame.USEREVENT + 1
pygame.time.set_timer(STEPTIMER, 0)
steps = {'l': [-1, 0], 'r': [1, 0], 'u': [0, -1], 'd': [0, 1]}


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    # чтение карты из текстового файлы
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # поиск максимально длинной строки
    max_width = max(map(len, level_map))

    # дополнение пустого места в карте точками до прямоугольника
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'f':
                Tile('empty', x, y)
            elif level[y][x] == 'w':
                Tile('wall', x, y)
            elif level[y][x] == 'y':
                Tile('empty', x, y)
                Tile('yellow', x, y) # ВМЕСТО ЭТОГО НАДО ВЫЗЫВАТЬ КЛАСС СОЗДАНИЯ ВРАГА
            elif level[y][x] == 'b':
                Tile('empty', x, y)
                Tile('blue', x, y) # ВМЕСТО ЭТОГО НАДО ВЫЗЫВАТЬ КЛАСС СОЗДАНИЯ ВРАГА
            elif level[y][x] == 'p':
                Tile('empty', x, y)
                new_player = Player(x, y)
                player_pos = [x, y]
    # вернуть матрицу с размеченными клетками и с позицией игрока на уровне
    return new_player, player_pos


def terminate():
    pygame.quit()
    sys.exit()

# Шаги
def go(way):
    pygame.time.set_timer(STEPTIMER, 10)
    s = 0
    if map[player_pos[1] + steps[way][1]][player_pos[0] + steps[way][0]] != 'w':
        print(f'start pos:{player_pos}')
        while map[player_pos[1] + steps[way][1]][player_pos[0] + steps[way][0]] != 'w':
            while s != 8:
                for event in pygame.event.get():
                    if event.type == STEPTIMER:
                        player.rect.x += steps[way][0] * STEP
                        player.rect.y += steps[way][1] * STEP
                        s += 1
                        screen.fill(pygame.Color(0, 0, 0))
                        tiles_group.draw(screen)
                        player_group.draw(screen)
                        pygame.display.flip()
                    if event.type == pygame.QUIT:
                        terminate()
            s = 0
            player_pos[0] += steps[way][0]
            player_pos[1] += steps[way][1]
        print(f'steps:{steps[way]}')
        print(f'new pos:{player_pos}', '', sep='\n')
    else:
        print(f'Nope', '', sep='\n')


def start_screen():
    scr = 0
    fon = load_image('fon.png')
    text = load_image('text.png')
    screen.blit(text, (0, 0))
    STARTTEXT = pygame.USEREVENT + 1
    pygame.time.set_timer(STARTTEXT, 700)
    run = True
    while run:
        screen.fill(0)
        screen.blit(fon, (0, 0))
        if scr == 1:
            screen.blit(text, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                run = False
            if event.type == STARTTEXT:
                scr = abs(scr - 1)
        pygame.display.flip()


tile_images = {'wall': load_image('wall.png'), 'empty': load_image('floor.png'),
               'yellow': load_image('yellow.png'), 'blue': load_image('blue.png')}
player_image = load_image('player.png')

tile_width = tile_height = 64


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 8, tile_height * pos_y + 8)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 8, tile_height * pos_y + 8)

start_screen()
map = load_level("map.txt")
player, player_pos = generate_level(map)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                go('l')
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                go('r')
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                go('u')
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                go('d')
    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
terminate()