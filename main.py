#!/usr/bin/python

import pygame
import random

from lib.tetrimino import Tetrimino
from lib.zone import Zone

pygame.init()

# Init config
config = {}
execfile("controls.conf", config)

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

B_SIZE = Z_WIDTH / 10

zone = Zone((Z_WIDTH, Z_HEIGHT))

background = zone.copy()

Z_LEFT = screen.get_width() / 2 - zone.get_width() / 2

screen.blit(zone, (Z_LEFT, 0))

F_TIME = 500


tetriminos_definitions = (
    {
        'name': 'O',
        'color': yellow,
        'blocks': ((
            (0, 0),
            (1, 0),
            (1, 1),
            (0, 1)
        ),)
    },
    {
        'name': 'I',
        'color': cyan,
        'blocks': ((
            (1, 1),
            (0, 1),
            (2, 1),
            (3, 1)
        ), (
            (1, 1),
            (1, 0),
            (1, 2),
            (1, 3)
        ))
    },
    {
        'name': 'J',
        'color': blue,
        'blocks': ((
            (0, 0),
            (1, 0),
            (2, 0),
            (2, 1)
        ),(
            (2, 0),
            (2, 1),
            (2, 2),
            (1, 2)
        ),(
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 2)
        ),(
            (0, 0),
            (1, 0),
            (0, 1),
            (0, 2)
        ))
    },
    {
        'name': 'L',
        'color': orange,
        'blocks': ((
            (0, 2),
            (1, 2),
            (2, 2),
            (2, 1)
        ),(
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2)
        ),(
            (0, 0),
            (0, 1),
            (1, 0),
            (2, 0)
        ),(
            (2, 0),
            (2, 1),
            (2, 2),
            (1, 0)
        ))
    },
    {
        'name': 'S',
        'color': green,
        'blocks': ((
            (1, 0),
            (0, 1),
            (1, 1),
            (2, 0)
        ),(
            (1, 1),
            (1, 0),
            (2, 1),
            (2, 2)
        ))
    },
    {
        'name': 'T',
        'color': purple,
        'blocks': ((
            (0, 2),
            (1, 1),
            (1, 2),
            (2, 2)
        ),(
            (0, 0),
            (0, 1),
            (1, 1),
            (0, 2)
        ),(
            (0, 0),
            (1, 0),
            (1, 1),
            (2, 0)
        ),(
            (2, 0),
            (1, 1),
            (2, 1),
            (2, 2)
        ),)
    },
    {
        'name': 'Z',
        'color': red,
        'blocks': ((
            (1, 0),
            (0, 0),
            (1, 1),
            (2, 1)
        ),(
            (1, 1),
            (1, 0),
            (0, 1),
            (0, 2)
        ))
    }
)


L = Tetrimino(tetriminos_definitions[2], B_SIZE, background, zone)
L.center(Z_WIDTH)
L.draw(zone)
screen.blit(zone, (Z_LEFT, 0))
pygame.display.update()

FALLEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(FALLEVENT, F_TIME)

# sounds
sounds = dict()
sounds["rotate"] = pygame.mixer.Sound("res/rotate.wav")
sounds["fall"] = pygame.mixer.Sound("res/fall.wav")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False
            if event.key == config['KEY_LEFT']:
                L.moveLeft()
                if L.isColliding():
                    L.moveRight()
                else:
                    L.clear(zone)
                    L.draw(zone)
            if event.key == config['KEY_RIGHT']:
                L.moveRight()
                if L.isColliding():
                    L.moveLeft()
                else:
                    L.clear(zone)
                    L.draw(zone)
            if event.key == config['KEY_DOWN']:
                L.moveDown()
                if L.isColliding():
                    L.moveUp()
                else:
                    L.clear(zone)
                    L.draw(zone)
            if event.key == config['KEY_ROTATE']:
                if L.rotate():
                    sounds["rotate"].play()
                    L.clear(zone)
                    L.draw(zone)

        if event.type == FALLEVENT:
            L.moveDown()
            if L.isColliding():
                sounds["fall"].play()
                L.moveUp()
                zone.sprites.append(L)
                L = Tetrimino(random.choice(tetriminos_definitions), B_SIZE, background, zone)
                L.center(Z_WIDTH)
                L.draw(zone)
            else:
                L.clear(zone)
                L.draw(zone)
    screen.blit(zone, (Z_LEFT, 0))

    pygame.display.update()

print("Exiting game")
