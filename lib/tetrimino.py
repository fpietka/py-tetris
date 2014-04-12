import pygame
import math

white = (255, 255, 255)

D_UP = 0


class Tetrimino(pygame.sprite.Group):
    def __init__(self, definition, size, background):
        super(Tetrimino, self).__init__()
        self.blocks = list()
        self.color = white
        self.outline = 1
        self.direction = D_UP
        # XXX maybe have 3 separate parameters in init
        self.setName(definition['name'])
        self.setColor(definition['color'])
        self.setBlocks(definition['blocks'])
        self.size = size
        self.background = background

    def setName(self, name):
        self.name = name
        return self

    def setBlocks(self, blocks):
        """Build sprites group"""
        self.blocks = blocks
        # use first block to draw an image
        block = pygame.Rect(blocks[0])
        block.top, block.left = 0, 0
        image = pygame.Surface(block.size)
        pygame.draw.rect(image, self.color, block, self.outline)
        for block in blocks:
            sprite = pygame.sprite.Sprite()
            sprite.rect = pygame.Rect(block)
            sprite.image = image
            sprite.add(self)
        return self

    def setColor(self, color):
        """Set the color of the sprites"""
        self.color = color
        return self

    def clear(self, zone):
        super(Tetrimino, self).clear(zone, self.background)

    def moveDown(self):
        for sprite in self.sprites():
            sprite.rect.top += self.size +2
        return self

    def moveUp(self):
        for sprite in self.sprites():
            sprite.rect.top -= self.size +2
        return self

    def moveLeft(self):
        for sprite in self.sprites():
            sprite.rect.left -= self.size +2
        return self

    def moveRight(self):
        for sprite in self.sprites():
            sprite.rect.left += self.size +2
        return self

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
        print self.size
        for sprite in self.sprites():
            # why +7 here?
            sprite.rect.left += (start * self.size) + 7
        return self
