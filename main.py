#!/usr/bin/env python

import pygame

from lib.game import Game

pygame.init()
pygame.mouse.set_visible(False)

# Init config
"""
with open('infile.txt') as f:
    {int(k): v for line in f for (k, v) in (line.strip().split(None, 1),)}
    """
config = {}
execfile("controls.conf", config)
print(config)

modes = pygame.display.list_modes()
mode = modes[-1]
# Running in smallest mode
screen = pygame.display.set_mode(mode)

game = Game(screen, config)
while game.running:
    for event in pygame.event.get():
        game.handleEvents(event)

    pygame.display.update()

print("Score: {}".format(game.score))
print("Lines: {}".format(game.lines))
print("Level: {}".format(game.level))

print("Exiting game")
