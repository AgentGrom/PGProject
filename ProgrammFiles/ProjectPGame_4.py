import os
import sys
import pygame

pygame.init()

WIDTH = 720
HEIGHT = 720
STEP = 8
FPS = 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

STARTTEXT = pygame.USEREVENT + 1
pygame.time.set_timer(STARTTEXT, 1000)

player = None
floor_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
vrag_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()

STEPTIMER = pygame.USEREVENT + 2
pygame.time.set_timer(STEPTIMER, 10)
steps = {'l': [-1, 0], 'r': [1, 0], 'u': [0, -1], 'd': [0, 1]}
global floors, col
coords = {'rules': [35, 20, 200, 80], 'styles': [260, 20, 200, 80], 'settings': [485, 20, 200, 80], '1': [90, 150, 150, 150],
          '2': [285, 150, 150, 150], '3': [480, 150, 150, 150], '4': [90, 345, 150, 150], '5': [285, 345, 150, 150],
          '6': [480, 345, 150, 150], '7': [85, 540, 150, 150], '8': [285, 540, 150, 150], '9': [480, 540, 150, 150]}
pause_button = [635, 25, 59, 59]
pause_menu = {'restart': [147, 360, 196, 82], 'menu': [374, 360, 196, 82]}

VRAGTIMER = pygame.USEREVENT + 3
pygame.time.set_timer(VRAGTIMER, 20)


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
    filename = "levels/" + filename
    # чтение карты из текстового файлы
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # дополнение пустого места в карте точками до прямоугольника
    return level_map


def generate_level(level):
    new_player, x, y = None, None, None
    global floors
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'f':
                Tile('empty', x, y)
                floors += 1
            elif level[y][x] == 'w':
                Wall('wall', x, y)
            elif level[y][x] == 'o':
                Tile('paint', x, y)
            elif level[y][x] == 'y':
                Tile('empty', x, y)
                Vrag('yellow', x, y) # ВМЕСТО ЭТОГО НАДО ВЫЗЫВАТЬ КЛАСС СОЗДАНИЯ ВРАГА
                floors += 1
            elif level[y][x] == 'b':
                Tile('empty', x, y)
                Vrag('blue', x, y) # ВМЕСТО ЭТОГО НАДО ВЫЗЫВАТЬ КЛАСС СОЗДАНИЯ ВРАГА
                floors += 1
            elif level[y][x] == 'p':
                Tile('empty', x, y)
                new_player = Player(x, y)
                player_pos = [x, y]
                floors += 1
    # вернуть матрицу с размеченными клетками и с позицией игрока на уровне
    return new_player, player_pos


def terminate():
    pygame.quit()
    sys.exit()


def go(way):
    s = 0
    global floors, col
    if map[player_pos[1] + steps[way][1]][player_pos[0] + steps[way][0]] != 'w':
        while map[player_pos[1] + steps[way][1]][player_pos[0] + steps[way][0]] != 'w':
            while s != 8:
                for event in pygame.event.get():
                    if event.type == STEPTIMER:
                        player.rect.x += steps[way][0] * STEP
                        player.rect.y += steps[way][1] * STEP
                        s += 1
                        floor_group.update()
                        floor_group.draw(screen)
                    if event.type == VRAGTIMER:
                        vrag_group.update()
                    if event.type == pygame.QUIT:
                        terminate()
                    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(num_buttons=3)[0]:
                        pos = pygame.mouse.get_pos()
                        if pause_button[0] < pos[0] < pause_button[0] + pause_button[2] and pause_button[1] < \
                                pos[1] < pause_button[1] + pause_button[3]:
                            p = pause()
                            if p == 'men':
                                return 'menu'
                            elif p == 'res':
                                return 'dead'
                if pygame.sprite.spritecollideany(player, vrag_group) != None:
                    p = pause()
                    if p == 'men':
                        return 'menu'
                    elif p == 'res':
                        return 'dead'
                screen.fill(pygame.Color(0, 0, 0))
                tiles_group.draw(screen)
                player_group.draw(screen)
                vrag_group.draw(screen)
                screen.blit(menu_images['pause_button'], (0, 0))
                pygame.display.flip()
            s = 0
            player_pos[0] += steps[way][0]
            player_pos[1] += steps[way][1]


def start_screen():
    scr = 0
    fon = load_image('fon.png')
    text = load_image('text.png')
    screen.blit(text, (0, 0))
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


def game():
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
            if event.type == VRAGTIMER:
                vrag_group.update()
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(num_buttons=3)[0]:
                pos = pygame.mouse.get_pos()
                if pause_button[0] < pos[0] < pause_button[0] + pause_button[2] and pause_button[1] < pos[1] < \
                        pause_button[1] + pause_button[3]:
                    p = pause()
                    if p == 'men':
                        return 'menu'
                    elif p == 'res':
                        return 'dead'
        screen.fill(pygame.Color(0, 0, 0))
        all_sprites.draw(screen)
        vrag_group.draw(screen)
        player_group.draw(screen)
        screen.blit(menu_images['pause_button'], (0, 0))
        if pygame.sprite.spritecollideany(player, vrag_group) != None:
            p = pause()
            if p == 'men':
                return 'menu'
            elif p == 'res':
                return 'dead'
        if floors == col:
            return 'win'
        pygame.display.flip()
    terminate()


def pause():
    screen.fill(pygame.Color(0, 0, 0))
    all_sprites.draw(screen)
    vrag_group.draw(screen)
    player_group.draw(screen)
    screen.blit(menu_images['pause_button'], (0, 0))
    screen.blit(menu_images['pause_menu'], (0, 0))
    if pygame.sprite.spritecollideany(player, vrag_group) != None:
        screen.blit(menu_images['dead'], (0, 0))
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(num_buttons=3)[0]:
                pos = pygame.mouse.get_pos()
                for i in pause_menu:
                    if pause_menu[i][0] < pos[0] < pause_menu[i][0] + pause_menu[i][2] and pause_menu[i][1] < pos[1] < pause_menu[i][1] + pause_menu[i][3]:
                        if i == 'restart':
                            return 'res'
                        elif i == 'menu':
                            return 'men'
                else:
                    return 'go'


tile_images = {'wall': load_image('wall.png'), 'empty': load_image('floor.png'),
               'yellow': load_image('yellow.png'), 'blue': load_image('blue.png'),
               'paint': load_image('painted_floor.png')}
menu_images = {'pause_button': load_image('pause.png'), 'pause_menu': load_image('pause_menu.png'),
               'dead': load_image('dead.png'), 'win': load_image('win.png')}
player_image = load_image('player.png')

tile_width = tile_height = 64


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, floor_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 8, tile_height * pos_y + 8)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if pygame.sprite.spritecollideany(player, floor_group) != None:
            pygame.sprite.spritecollideany(player, floor_group).image = tile_images['paint']
            floor_group.remove(pygame.sprite.spritecollideany(player, floor_group))
            global col
            col += 1


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, wall_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 8, tile_height * pos_y + 8)
        self.mask = pygame.mask.from_surface(self.image)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 20, tile_height * pos_y + 20)
        self.mask = pygame.mask.from_surface(self.image)


class Vrag(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, vrag_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 12, tile_height * pos_y + 12)
        self.mask = pygame.mask.from_surface(self.image)
        self.tip = tile_type
        self.x = pos_x
        self.y = pos_y
        self.n = 0
        self.cuda = 1
        self.cuda1 = 1

    def update(self):
        for i in vrag_group:
            if pygame.sprite.spritecollideany(i, wall_group) != None and i.image == tile_images['yellow']:
                self.cuda *= -1
            elif pygame.sprite.spritecollideany(i, wall_group) != None and i.image == tile_images['blue']:
                self.cuda1 *= -1
            if self.tip == 'yellow':
                self.rect = self.rect.move(self.cuda, 0)
            elif self.tip == 'blue':
                self.rect = self.rect.move(0, self.cuda1)


all_sprites = pygame.sprite.Group()
start_screen()
home = True
men = load_image('menu_razr.png')
screen.blit(men, (0, 0))
while home:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(num_buttons=3)[0]:
            pos = pygame.mouse.get_pos()
            for i in coords:
                if coords[i][0] < pos[0] < coords[i][0] + coords[i][2] and coords[i][1] < pos[1] < coords[i][1] + coords[i][3]:
                    if len(i) == 1:
                        floors, col = 0, 0
                        all_sprites.empty()
                        tiles_group.empty()
                        player_group.empty()
                        wall_group.empty()
                        floor_group.empty()
                        vrag_group.empty()
                        map = load_level(f'level{i}.txt')
                        player, player_pos = generate_level(map)
                        g = ''
                        while g != 'menu' and g != 'win':
                            g = game()
                            floors, col = 0, 0
                            all_sprites.empty()
                            tiles_group.empty()
                            player_group.empty()
                            wall_group.empty()
                            floor_group.empty()
                            vrag_group.empty()
                            map = load_level(f'level{i}.txt')
                            player, player_pos = generate_level(map)
                        screen.blit(men, (0, 0))
                        if g == 'win':
                            screen.blit(menu_images['win'], (0, 0))
                            pygame.time.set_timer(STARTTEXT, 2000)
                    else:
                        pass
                else:
                    pass
        if event.type == STARTTEXT:
            screen.blit(men, (0, 0))
            pygame.time.set_timer(STARTTEXT, 0)
    pygame.display.flip()
terminate()