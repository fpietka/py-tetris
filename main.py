#!/usr/bin/env python

import pygame

from lib.game import Game

pygame.init()
pygame.mouse.set_visible(False)

# Init config
config = {}
execfile("controls.conf", config)

modes = pygame.display.list_modes()
mode = modes[-1]
# Running in smallest mode
screen = pygame.display.set_mode(mode)

D_UP = 0
D_RIGHT = 1
D_DOWN = 2
D_LEFT = 3
directions = (D_UP, D_RIGHT, D_DOWN, D_LEFT)

M_CW = 0
M_CCW = 1
motions = (M_CW, M_CCW)

game = Game(screen, config)
while game.running:
    for event in pygame.event.get():
        game.handleEvents(event)

    pygame.display.update()

print("Score: {}".format(game.score))
print("Lines: {}".format(game.lines))
print("Level: {}".format(game.level))

print("Exiting game")
