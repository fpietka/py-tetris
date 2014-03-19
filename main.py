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
pygame.draw.rect(zone, white, zone.get_rect(), 1)

Z_LEFT = screen.get_width() / 2 - zone.get_width() / 2

screen.blit(zone, (Z_LEFT, 0))


class Tetrimino(pygame.sprite.Group):
    def __init__(self, name, color=white):
        super(Tetrimino, self).__init__()
        self.name = name
        self.blocks = list()
        self.setColor(color)
        self.outline = 1
        self.direction = D_UP

    def setBlocks(self, blocks):
        """Build sprites group"""
        self.blocks = blocks
        # use first block to draw an image
        block = blocks[0].copy()
        block.top, block.left = 0, 0
        image = pygame.Surface(block.size)
        pygame.draw.rect(image, self.color, block, self.outline)
        for block in blocks:
            sprite = pygame.sprite.Sprite()
            sprite.rect = block
            sprite.image = image
            sprite.add(self)
        return self

    def setColor(self, color):
        """Set the color of the sprites"""
        self.color = color
        return self

tetriminos = (
    Tetrimino('O', yellow).setBlocks((
        pygame.Rect(0, 0, B_SIZE, B_SIZE),
        pygame.Rect(B_SIZE + 2, 0, B_SIZE, B_SIZE),
        pygame.Rect(B_SIZE + 2, B_SIZE + 2, B_SIZE, B_SIZE),
        pygame.Rect(0, B_SIZE + 2, B_SIZE, B_SIZE)
    )),

    Tetrimino('I', cyan).setBlocks((
        pygame.Rect(0, 0, B_SIZE, B_SIZE),
        pygame.Rect(B_SIZE + 2, 0, B_SIZE, B_SIZE),
        pygame.Rect((B_SIZE + 2) * 2, 0, B_SIZE, B_SIZE),
        pygame.Rect((B_SIZE + 2) * 3, 0, B_SIZE, B_SIZE)
    )),

    Tetrimino('J', blue).setBlocks((
        pygame.Rect(0, 0, B_SIZE, B_SIZE),
        pygame.Rect(0, B_SIZE + 2, B_SIZE, B_SIZE),
        pygame.Rect(B_SIZE + 2, B_SIZE + 2, B_SIZE, B_SIZE),
        pygame.Rect((B_SIZE + 2) * 2, B_SIZE + 2, B_SIZE, B_SIZE)
    )),

    Tetrimino('L', orange).setBlocks((
        pygame.Rect(0, B_SIZE + 2, B_SIZE, B_SIZE),
        pygame.Rect(B_SIZE + 2, B_SIZE + 2, B_SIZE, B_SIZE),
        pygame.Rect((B_SIZE + 2) * 2, B_SIZE + 2, B_SIZE, B_SIZE),
        pygame.Rect((B_SIZE + 2) * 2, 0, B_SIZE, B_SIZE)
    )),

    Tetrimino('S', green).setBlocks((
        pygame.Rect(0, B_SIZE + 2, B_SIZE, B_SIZE),
        pygame.Rect(B_SIZE + 2, 0, B_SIZE, B_SIZE),
        pygame.Rect(B_SIZE + 2, B_SIZE + 2, B_SIZE, B_SIZE),
        pygame.Rect((B_SIZE + 2) * 2, 0, B_SIZE, B_SIZE)
    )),

    Tetrimino('T', purple).setBlocks((
        pygame.Rect(0, B_SIZE + 2, B_SIZE, B_SIZE),
        pygame.Rect(B_SIZE + 2, 0, B_SIZE, B_SIZE),
        pygame.Rect(B_SIZE + 2, B_SIZE + 2, B_SIZE, B_SIZE),
        pygame.Rect((B_SIZE + 2) * 2, B_SIZE + 2, B_SIZE, B_SIZE)
    )),

    Tetrimino('Z', red).setBlocks((
        pygame.Rect(0, 0, B_SIZE, B_SIZE),
        pygame.Rect(B_SIZE + 2, 0, B_SIZE, B_SIZE),
        pygame.Rect(B_SIZE + 2, B_SIZE + 2, B_SIZE, B_SIZE),
        pygame.Rect((B_SIZE + 2) * 2, B_SIZE + 2, B_SIZE, B_SIZE)
    )),
)

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
    tetrimino.draw(screen)
    pygame.display.update()
    # wait a second
    pygame.time.wait(1000)


print("Exiting game")
