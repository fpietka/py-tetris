#!/usr/bin/env python

import pygame
import random

from lib.tetrimino import Tetrimino
from lib.matrix import Matrix

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mouse.set_visible(False)

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

SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
Z_WIDTH, Z_HEIGHT = screen.get_size()
Z_WIDTH = Z_HEIGHT / 2

B_SIZE = Z_WIDTH / 10

matrix = Matrix((Z_WIDTH, Z_HEIGHT))

background = matrix.copy()
matrix.background = background
matrix.block_size = B_SIZE

Z_LEFT = screen.get_width() / 2 - matrix.get_width() / 2

screen.blit(matrix, (Z_LEFT, 0))

"""
Handle speed:
    Level, Frames/drop, Period (sec/drop), Speed (drops/sec)
    ---------------------
    0,    48, .799,  1.25
    1,    43, .715,  1.40
    2,    38, .632,  1.58
    3,    33, .549,  1.82
    4,    28, .466,  2.15
    5,    23, .383,  2.61
    6,    18, .300,  3.34
    7,    13, .216,  4.62
    8,     8, .133,  7.51
    9,     6, .100, 10.02
    10-12, 5, .083, 12.02
    13-15, 4, .067, 15.05
    16-18, 3, .050, 20.03
    19-28, 2, .033, 30.05
    29+,   1, .017, 60.10

"""
SPEEDS = (
        799,
        715,
        632,
        549,
        466,
        383,
        300,
        216,
        133,
        100,
        83,
        67,
        50,
        33,
        17)

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
        ), (
            (2, 0),
            (2, 1),
            (2, 2),
            (1, 2)
        ), (
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 2)
        ), (
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
        ), (
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2)
        ), (
            (0, 0),
            (0, 1),
            (1, 0),
            (2, 0)
        ), (
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
        ), (
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
        ), (
            (0, 0),
            (0, 1),
            (1, 1),
            (0, 2)
        ), (
            (0, 0),
            (1, 0),
            (1, 1),
            (2, 0)
        ), (
            (2, 0),
            (1, 1),
            (2, 1),
            (2, 2)
        ))
    },
    {
        'name': 'Z',
        'color': red,
        'blocks': ((
            (1, 0),
            (0, 0),
            (1, 1),
            (2, 1)
        ), (
            (1, 1),
            (1, 0),
            (0, 1),
            (0, 2)
        ))
    }
)


L = Tetrimino(tetriminos_definitions[2], B_SIZE, background, matrix)
L.center(Z_WIDTH)
L.draw(matrix)
screen.blit(matrix, (Z_LEFT, 0))
pygame.display.update()

FALLEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(FALLEVENT, SPEEDS[0])

lines = 0
score = 0
level = 0

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
                    L.clear(matrix)
                    L.draw(matrix)
            if event.key == config['KEY_RIGHT']:
                L.moveRight()
                if L.isColliding():
                    L.moveLeft()
                else:
                    L.clear(matrix)
                    L.draw(matrix)
            if event.key == config['KEY_DOWN']:
                L.moveDown()
                if L.isColliding():
                    L.moveUp()
                else:
                    L.clear(matrix)
                    L.draw(matrix)
            if event.key in config['KEY_ROTATE_RIGHT']:
                if L.rotate():
                    sounds["rotate"].play()
                    L.clear(matrix)
                    L.draw(matrix)
            if event.key == config['KEY_HARD_DROP']:
                while not L.isColliding():
                    L.moveDown()
                L.moveUp()
                L.clear(matrix)
                L.draw(matrix)

        if event.type == FALLEVENT:
            L.moveDown()
            if L.isColliding():
                sounds["fall"].play()
                L.moveUp()
                matrix.sprites.append(L)
                L = Tetrimino(
                    random.choice(tetriminos_definitions),
                    B_SIZE,
                    background,
                    matrix
                )
                L.center(Z_WIDTH)
                empty_lines, points = matrix.checkLines()

                if empty_lines:
                    # calculcate
                    lines += empty_lines
                    score += points * (level + 1)
                    level = int(lines / 10)

                    pygame.time.set_timer(FALLEVENT, SPEEDS[level])

                L.draw(matrix)
            else:
                L.clear(matrix)
                L.draw(matrix)
    screen.blit(matrix, (Z_LEFT, 0))

    pygame.display.update()

print("Exiting game")
