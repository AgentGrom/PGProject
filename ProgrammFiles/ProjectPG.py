import os
import sys
import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 1000
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = None
menu_group = pygame.sprite.Group()
levels_group = pygame.sprite.Group()
entity_group = pygame.sprite.Group()


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


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    scr = 0
    STARTTEXT = pygame.USEREVENT + 1
    pygame.time.set_timer(STARTTEXT, 1000)
    run = True
    while run:
        screen.fill(0)
        screen.blit(load_image('start.png'), (0, 0))
        if scr == 1:
            screen.blit(load_image('starttext.png'), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                run = False
            if event.type == STARTTEXT:
                scr = abs(scr - 1)
        pygame.display.flip()
        clock.tick(FPS)


def menu():
    screen.fill(0)
    screen.blit(load_image('menu.png'), (0, 0))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                run = False
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
print(1)
menu()
print(2)
running = True

while running:
    screen.fill(0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick(FPS)
terminate()