import pygame
import math
from itertools import cycle

white = (255, 255, 255)

D_UP = 0


class Tetrimino(pygame.sprite.OrderedUpdates):
    def __init__(self, definition, size, background):
        super(Tetrimino, self).__init__()
        self.blocks = list()
        self.color = white
        self.outline = 1
        self.direction = D_UP
        # XXX maybe have 3 separate parameters in init
        self.setName(definition['name'])
        self.setColor(definition['color'])
        self.blocks = cycle(definition['blocks'])
        self.size = size
        self.setBlocks(next(self.blocks))
        self.background = background

    def setName(self, name):
        self.name = name
        return self

    def setBlocks(self, blocks):
        """Build sprites group"""
        # use first block to draw an image
        block = pygame.Rect(blocks[0][0] * self.size, blocks[0][1] * self.size, self.size, self.size)
        image = self.buildImage(block)
        for block in blocks:
            sprite = pygame.sprite.Sprite()
            sprite.rect = pygame.Rect(block[0] * self.size, block[1] * self.size, self.size, self.size)
            sprite.image = image
            sprite.add(self)
        return self

    def buildImage(self, block):
        block.top, block.left = 0, 0
        image = pygame.Surface(block.size)
        # inner block is a little smaller
        innerblock = pygame.Rect(self.outline, self.outline, block.size[0] - self.outline * 2, block.size[1] - self.outline * 2)
        pygame.draw.rect(image, self.color, innerblock, self.outline)
        return image

    def setColor(self, color):
        """Set the color of the sprites"""
        self.color = color
        return self

    def clear(self, zone):
        super(Tetrimino, self).clear(zone, self.background)

    def moveUp(self):
        self._move('up')
        return self

    def moveDown(self):
        self._move('down')
        return self

    def moveLeft(self):
        self._move('left')
        return self

    def moveRight(self):
        self._move('right')
        return self

    def _move(self, direction):
        if direction == 'up':
            for sprite in self.sprites():
                sprite.rect.top -= self.size
        elif direction == 'down':
            for sprite in self.sprites():
                sprite.rect.top += self.size
        elif direction == 'left':
            for sprite in self.sprites():
                sprite.rect.left -= self.size
        elif direction == 'right':
            for sprite in self.sprites():
                sprite.rect.left += self.size

    def rotate(self):
        self.empty()
        self.setBlocks(next(self.blocks))

    def isColliding(self, zone_sprites_groups, zone_bottom, zone_left, zone_right):
        # Test collisions
        for group in zone_sprites_groups:
            if pygame.sprite.groupcollide(group, self, False, False):
                return True
        bottom = max(sprite.rect.bottom for sprite in self.sprites())
        if bottom > zone_bottom:
            return True
        left = min(sprite.rect.left for sprite in self.sprites())
        if left < zone_left:
            return True
        right = max(sprite.rect.right for sprite in self.sprites())
        if right > zone_right:
            return True

    def center(self, width):
        groupwidth = max(sprite.rect.right for sprite in self.sprites()) / self.size
        zonecenter = (width / self.size) / 2
        start = zonecenter - int(math.ceil(float(groupwidth) / 2))
        for sprite in self.sprites():
            sprite.rect.left += (start * self.size)
        return self
