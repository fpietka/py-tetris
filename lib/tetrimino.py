import pygame


white = (255, 255, 255)

D_UP = 0

class Tetrimino(pygame.sprite.Group):
    def __init__(self, definition, size):
        super(Tetrimino, self).__init__()
        self.blocks = list()
        self.color = white
        self.outline = 1
        self.direction = D_UP
        # XXX maybe have 3 seperate parameters in init
        self.setName(definition['name'])
        self.setColor(definition['color'])
        self.setBlocks(definition['blocks'])
        self.size = size

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

    def moveDown(self):
        for sprite in self.sprites():
            sprite.rect.top += self.size +2
        return self

    def moveUp(self):
        for sprite in self.sprites():
            sprite.rect.top -= self.size +2
        return self

    def isColliding(self, zone_sprites_groups, zone_bottom):
        # Test collisions
        for group in zone_sprites_groups:
            if pygame.sprite.groupcollide(group, self, False, False):
                return True
        bottom = max(sprite.rect.bottom for sprite in self.sprites())
        if bottom > zone_bottom:
            return True

    def center(self, width):
        groupwidth = max(sprite.rect.right for sprite in self.sprites())
        for sprite in self.sprites():
            sprite.rect.left += (width / 2) - (groupwidth / 2)
        return self


