#!/usr/bin/python

import pygame

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
orange = (255, 255, 0)

class Tetrimino():
    def __init__(self, name):
        self.name = name
        self.blocks = list()
        self.color = white

    def setBlocks(self, blocks):
        self.blocks = blocks
        return self

    def setColor(self, color):
        self.color = color
        return self

tetriminos = (
    Tetrimino('O').setBlocks((
            pygame.Rect(0, 0, 10, 10),
            pygame.Rect(12, 0, 10, 10),
            pygame.Rect(12, 12, 10, 10),
            pygame.Rect(0, 12, 10, 10)
    )).setColor(yellow),

    Tetrimino('I').setBlocks((
            pygame.Rect(0, 0, 10, 10),
            pygame.Rect(12, 0, 10, 10),
            pygame.Rect(24, 0, 10, 10),
            pygame.Rect(36, 0, 10, 10)
    )).setColor(cyan),

    Tetrimino('J').setBlocks((
            pygame.Rect(0, 0, 10, 10),
            pygame.Rect(0, 12, 10, 10),
            pygame.Rect(12, 12, 10, 10),
            pygame.Rect(24, 12, 10, 10)
    )).setColor(blue),

    Tetrimino('L').setBlocks((
            pygame.Rect(0, 12, 10, 10),
            pygame.Rect(12, 12, 10, 10),
            pygame.Rect(24, 12, 10, 10),
            pygame.Rect(24, 0, 10, 10)
    )).setColor(orange),

    Tetrimino('S').setBlocks((
            pygame.Rect(0, 12, 10, 10),
            pygame.Rect(12, 0, 10, 10),
            pygame.Rect(12, 12, 10, 10),
            pygame.Rect(24, 0, 10, 10)
    )).setColor(green),

    Tetrimino('T').setBlocks((
            pygame.Rect(0, 12, 10, 10),
            pygame.Rect(12, 0, 10, 10),
            pygame.Rect(12, 12, 10, 10),
            pygame.Rect(24, 12, 10, 10)
    )).setColor(purple),

    Tetrimino('Z').setBlocks((
            pygame.Rect(0, 0, 10, 10),
            pygame.Rect(12, 0, 10, 10),
            pygame.Rect(12, 12, 10, 10),
            pygame.Rect(24, 12, 10, 10)
    )).setColor(red),
)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False

print("Exiting game")
