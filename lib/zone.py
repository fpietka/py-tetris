import pygame

class Zone(pygame.Surface):
    def __init__(self, *args):
        super(Zone, self).__init__(*args)
        pygame.draw.rect(self, (255, 255, 255), self.get_rect(), 1)
        self.sprites = list()
