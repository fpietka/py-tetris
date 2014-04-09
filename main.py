#!/usr/bin/python

import pygame
import random

from lib.tetrimino import Tetrimino

pygame.init()

modes = pygame.display.list_modes()
mode = modes[-1]
# Running in smallest mode
screen = pygame.display.set_mode(mode)

black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
purple = (255, 0, 255)
orange = (255, 140, 0)

D_UP = 0
D_RIGHT = 1
D_DOWN = 2
D_LEFT = 3
directions = (D_UP, D_RIGHT, D_DOWN, D_LEFT)

M_CW = 0
M_CCW = 1
motions = (M_CW, M_CCW)

Z_WIDTH, Z_HEIGHT = screen.get_size()
Z_WIDTH = Z_HEIGHT / 2

B_SIZE = (Z_WIDTH - 11) / 10

zone = pygame.Surface((Z_WIDTH, Z_HEIGHT))
zone_sprites_groups = list()
pygame.draw.rect(zone, white, zone.get_rect(), 1)

Z_LEFT = screen.get_width() / 2 - zone.get_width() / 2

screen.blit(zone, (Z_LEFT, 0))

F_TIME = 500


tetriminos_definitions = (
    {
        'name': 'O',
        'color': yellow,
        'blocks': (
            (0, 0, B_SIZE, B_SIZE),
            (B_SIZE + 2, 0, B_SIZE, B_SIZE),
            (B_SIZE + 2, B_SIZE + 2, B_SIZE, B_SIZE),
            (0, B_SIZE + 2, B_SIZE, B_SIZE)
        )
    },
    {
        'name': 'I',
        'color': cyan,
        'blocks': (
            (0, 0, B_SIZE, B_SIZE),
            (B_SIZE + 2, 0, B_SIZE, B_SIZE),
            ((B_SIZE + 2) * 2, 0, B_SIZE, B_SIZE),
            ((B_SIZE + 2) * 3, 0, B_SIZE, B_SIZE)
        )
    },
    {
        'name': 'J',
        'color': blue,
        'blocks': (
            (0, 0, B_SIZE, B_SIZE),
            (0, B_SIZE + 2, B_SIZE, B_SIZE),
            (B_SIZE + 2, B_SIZE + 2, B_SIZE, B_SIZE),
            ((B_SIZE + 2) * 2, B_SIZE + 2, B_SIZE, B_SIZE)
        )
    },
    {
        'name': 'L',
        'color': orange,
        'blocks': (
            (0, B_SIZE + 2, B_SIZE, B_SIZE),
            (B_SIZE + 2, B_SIZE + 2, B_SIZE, B_SIZE),
            ((B_SIZE + 2) * 2, B_SIZE + 2, B_SIZE, B_SIZE),
            ((B_SIZE + 2) * 2, 0, B_SIZE, B_SIZE)
        )
    },
    {
        'name': 'S',
        'color': green,
        'blocks': (
            (0, B_SIZE + 2, B_SIZE, B_SIZE),
            (B_SIZE + 2, 0, B_SIZE, B_SIZE),
            (B_SIZE + 2, B_SIZE + 2, B_SIZE, B_SIZE),
            ((B_SIZE + 2) * 2, 0, B_SIZE, B_SIZE)
        )
    },
    {
        'name': 'T',
        'color': purple,
        'blocks': (
            (0, B_SIZE + 2, B_SIZE, B_SIZE),
            (B_SIZE + 2, 0, B_SIZE, B_SIZE),
            (B_SIZE + 2, B_SIZE + 2, B_SIZE, B_SIZE),
            ((B_SIZE + 2) * 2, B_SIZE + 2, B_SIZE, B_SIZE)
        )
    },
    {
        'name': 'Z',
        'color': red,
        'blocks': (
            (0, 0, B_SIZE, B_SIZE),
            (B_SIZE + 2, 0, B_SIZE, B_SIZE),
            (B_SIZE + 2, B_SIZE + 2, B_SIZE, B_SIZE),
            ((B_SIZE + 2) * 2, B_SIZE + 2, B_SIZE, B_SIZE)
        )
    },
)

tetriminos = list()
for definition in tetriminos_definitions:
    tetriminos.append(Tetrimino(definition, B_SIZE))


L = Tetrimino(tetriminos_definitions[2], B_SIZE)
L.center(Z_WIDTH)
L.draw(zone)
screen.blit(zone, (Z_LEFT, 0))
pygame.display.update()

FALLEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(FALLEVENT, F_TIME)

clearer = pygame.Rect(0, 0, (B_SIZE + 2) * 4, (B_SIZE + 2) * 4)

# iter through tetriminos
elements = iter(tetriminos)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False
            if event.key == pygame.K_LEFT:
                L.moveLeft()
                if L.isColliding(zone_sprites_groups, zone.get_rect().bottom, 0, zone.get_rect().right):
                    L.moveRight()
                else:
                    L.clear(zone, screen)
                    L.draw(zone)
            if event.key == pygame.K_RIGHT:
                L.moveRight()
                if L.isColliding(zone_sprites_groups, zone.get_rect().bottom, 0, zone.get_rect().right):
                    L.moveLeft()
                else:
                    L.clear(zone, screen)
                    L.draw(zone)

        if event.type == FALLEVENT:
            # select next tetrimino
            try:
                tetrimino = next(elements)
            except StopIteration:
                # reset iterable
                elements = iter(tetriminos)
                tetrimino = next(elements)
            # clear screen
            pygame.draw.rect(screen, black, clearer)
            # then draw it
            tetrimino.draw(screen)

            L.moveDown()
            if L.isColliding(zone_sprites_groups, zone.get_rect().bottom, 0, zone.get_rect().right):
                L.moveUp()
                zone_sprites_groups.append(L)
                L = Tetrimino(random.choice(tetriminos_definitions), B_SIZE)
                L.center(Z_WIDTH)
                L.draw(zone)
            else:
                L.clear(zone, screen)
                L.draw(zone)
    screen.blit(zone, (Z_LEFT, 0))

    pygame.display.update()

print("Exiting game")
