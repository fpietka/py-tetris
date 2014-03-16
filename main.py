#!/usr/bin/python

import pygame

pygame.init()

modes = pygame.display.list_modes()
mode = modes[-1]
# Running in smallest mode
screen = pygame.display.set_mode(mode)

yellow = (255, 255, 0)
cyan = (0, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
purple = (255, 0, 255)
orange = (255, 255, 0)

class Tetrimino():
    def __init__(self, name):
        self.name = name
        self.blocks = list()
        self.color = (255, 255, 255)

    def setBlocks(self, blocks):
        self.blocks = blocks
        return self

    def setColor(self, color):
        self.color = color
        return self

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False

print("Exiting game")
