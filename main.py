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
orange = (255, 140, 0)


class Tetrimino():
    def __init__(self, name, color=white):
        self.name = name
        self.blocks = list()
        self.color = color

    def setBlocks(self, blocks):
        self.blocks = blocks
        return self

    def setColor(self, color):
        self.color = color
        return self

tetriminos = (
    Tetrimino('O', yellow).setBlocks((
        pygame.Rect(0, 0, 10, 10),
        pygame.Rect(12, 0, 10, 10),
        pygame.Rect(12, 12, 10, 10),
        pygame.Rect(0, 12, 10, 10)
    )),

    Tetrimino('I', cyan).setBlocks((
        pygame.Rect(0, 0, 10, 10),
        pygame.Rect(12, 0, 10, 10),
        pygame.Rect(24, 0, 10, 10),
        pygame.Rect(36, 0, 10, 10)
    )),

    Tetrimino('J', blue).setBlocks((
        pygame.Rect(0, 0, 10, 10),
        pygame.Rect(0, 12, 10, 10),
        pygame.Rect(12, 12, 10, 10),
        pygame.Rect(24, 12, 10, 10)
    )),

    Tetrimino('L', orange).setBlocks((
        pygame.Rect(0, 12, 10, 10),
        pygame.Rect(12, 12, 10, 10),
        pygame.Rect(24, 12, 10, 10),
        pygame.Rect(24, 0, 10, 10)
    )),

    Tetrimino('S', green).setBlocks((
        pygame.Rect(0, 12, 10, 10),
        pygame.Rect(12, 0, 10, 10),
        pygame.Rect(12, 12, 10, 10),
        pygame.Rect(24, 0, 10, 10)
    )),

    Tetrimino('T', purple).setBlocks((
        pygame.Rect(0, 12, 10, 10),
        pygame.Rect(12, 0, 10, 10),
        pygame.Rect(12, 12, 10, 10),
        pygame.Rect(24, 12, 10, 10)
    )),

    Tetrimino('Z', red).setBlocks((
        pygame.Rect(0, 0, 10, 10),
        pygame.Rect(12, 0, 10, 10),
        pygame.Rect(12, 12, 10, 10),
        pygame.Rect(24, 12, 10, 10)
    )),
)

clearer = pygame.Rect(0, 0, 48, 48)

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

    # select next tetrimino
    try:
        tetrimino = next(elements)
    except StopIteration:
        # reset iterable
        elements = iter(tetriminos)
        tetrimino = next(elements)
    #clear screen
    pygame.draw.rect(screen, black, clearer)
    # then draw it
    for rect in tetrimino.blocks:
        pygame.draw.rect(screen, tetrimino.color, rect, 1)
    pygame.display.update()
    # wait a second
    pygame.time.wait(1000)


print("Exiting game")
