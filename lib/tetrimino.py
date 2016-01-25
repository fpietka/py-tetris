import pygame
import math
from itertools import cycle

white = (255, 255, 255)

D_UP = 0


class Tetrimino(pygame.sprite.OrderedUpdates):
    def __init__(self, definition, size, background, matrix):
        pygame.sprite.OrderedUpdates.__init__(self)
        self.blocks = list()
        self.color = white
        self.outline = 1
        self.direction = D_UP
        # XXX maybe have 3 separate parameters in init
        self.setName(definition['name'])
        self.setColor(definition['color'])
        self.all_blocks = definition['blocks']
        self.blocks_cycle = cycle(self.all_blocks)
        self.size = size
        self.pivot = (0, 0)
        self.setBlocks(next(self.blocks_cycle))
        self.background = background
        self.matrix = matrix
        self.isLocked = False

    def setName(self, name):
        self.name = name
        return self

    def setBlocks(self, blocks):
        """Build sprites group"""
        # use first block to draw an image
        self.blocks = blocks
        block = pygame.Rect(blocks[0][0] * self.size,
                            blocks[0][1] * self.size,
                            self.size,
                            self.size)
        image = self.buildImage(block)
        for block in blocks:
            sprite = pygame.sprite.Sprite()
            sprite.rect = pygame.Rect(block[0] * self.size + self.pivot[0],
                                      block[1] * self.size + self.pivot[1],
                                      self.size,
                                      self.size)
            sprite.image = image
            sprite.add(self)
        return self

    def buildImage(self, block):
        block.top, block.left = 0, 0
        image = pygame.Surface(block.size)
        # inner block is a little smaller
        innerblock = pygame.Rect(self.outline,
                                 self.outline,
                                 block.size[0] - self.outline * 2,
                                 block.size[1] - self.outline * 2)
        pygame.draw.rect(image, self.color, innerblock, self.outline)
        return image

    def setColor(self, color):
        """Set the color of the sprites"""
        self.color = color
        return self

    def clear(self, matrix):
        pygame.sprite.OrderedUpdates.clear(self, matrix, self.background)

    def moveUp(self):
        self._move('up')
        return self

    def moveDown(self):
        moved = False
        self._move('down')
        if self.isColliding():
            self._move('up')
            self.isLocked = True
        else:
            moved = True
            self._redraw()
        return moved

    def moveLeft(self):
        self._move('left')
        if self.isColliding():
            self._move('right')
        else:
            self._redraw()
        return self

    def moveRight(self):
        self._move('right')
        if self.isColliding():
            self._move('left')
        else:
            self._redraw()
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

    def harddrop(self):
        harddrops = 0
        while not self.isColliding():
            self._move('down')
            harddrops += 1
        self._move('up')
        self._redraw()
        self.isLocked = True
        harddrops -= 1
        return harddrops

    def _redraw(self):
        self.clear(self.matrix)
        self.draw(self.matrix)

    def rotate(self, test_collision=True):
        # previous set of blocks base positions
        previous_positions = self.blocks
        # get current position
        positions = list()
        for sprite in self.sprites():
            positions.append((sprite.rect.left / self.size,
                              sprite.rect.top / self.size))
        # empty sprite list
        self.empty()
        # get next set of blocks
        self.setBlocks(next(self.blocks_cycle))
        new_positions = self.blocks
        # set new calculated positions
        for index, sprite in enumerate(self.sprites()):
            sprite.rect.left = (positions[index][0] -
                                previous_positions[index][0] +
                                new_positions[index][0]) * self.size
            sprite.rect.top = (positions[index][1] -
                               previous_positions[index][1] +
                               new_positions[index][1]) * self.size
        if test_collision and self.isColliding():
            # handle matrix collisions
            if self.colliding == 'left':
                left = min(sprite.rect.left for sprite
                           in self.sprites()) / self.size
                if left < 0:
                    for _ in range(0, left * - 1):
                        self.moveRight()
            elif self.colliding == 'right':
                right = max(sprite.rect.right for sprite
                            in self.sprites()) / self.size
                if right > 10:
                    for _ in range(0, right - 10):
                        self.moveLeft()
            # handle sprite group collisions
            for _ in range(1, len(self.all_blocks)):
                self.rotate(False)
            # use previous positions
            for index, sprite in enumerate(self.sprites()):
                sprite.rect.left = positions[index][0] * self.size
                sprite.rect.top = positions[index][1] * self.size
            return self.isColliding()
        return True

    def isColliding(self):
        # Test collisions between sprites
        for group in self.matrix.sprites:
            if pygame.sprite.groupcollide(group, self, False, False):
                return True
        # Test collisions with boundaries
        matrix = self.matrix.get_rect()
        bottom = max(sprite.rect.bottom for sprite in self.sprites())
        if bottom > matrix.bottom:
            self.colliding = 'bottom'
            return True
        left = min(sprite.rect.left for sprite in self.sprites())
        if left < matrix.left:
            self.colliding = 'left'
            return True
        right = max(sprite.rect.right for sprite in self.sprites())
        if right > matrix.right:
            self.colliding = 'right'
            return True
        self.colliding = None
        return False

    def center(self, width, height=0):
        top = min(sprite.rect.top for sprite in self.sprites()) / self.size
        if top > 0:
            self.moveUp()
        groupwidth = max(sprite.rect.right for sprite
                         in self.sprites()) / self.size
        matrixcenter = (width / self.size) / 2
        start = matrixcenter - int(math.ceil(float(groupwidth) / 2))
        for sprite in self.sprites():
            sprite.rect.left += (start * self.size)
            sprite.rect.top += height
        return self
