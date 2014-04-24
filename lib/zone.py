import pygame

class Zone(pygame.Surface):
    def __init__(self, *args):
        super(Zone, self).__init__(*args)
        pygame.draw.rect(self, (255, 255, 255), self.get_rect(), 1)
        self.sprites = list()

    def checkLines(self):
        lines = dict()
        for sprite in self.sprites:
            for block in sprite.sprites():
                if block.rect.top in lines:
                    lines[block.rect.top]['count'] += 1
                    lines[block.rect.top]['sprites'].append(block)
                else:
                    lines[block.rect.top] = dict()
                    lines[block.rect.top]['count'] = 1
                    lines[block.rect.top]['sprites'] = list()
                    lines[block.rect.top]['sprites'].append(block)

        empty_lines = [(line / self.block_size, details['sprites']) for line, details in lines.iteritems() if details['count'] == 10]
        for empty_line in empty_lines:
            self.blit(self.background, (0, 0))
            for sprite in empty_line[1]:
                sprite.kill()
        for sprite in self.sprites:
            for block in sprite.sprites():
                for empty_line in empty_lines:
                    if block.rect.top / self.block_size < empty_line[0]:
                        block.rect.top += self.block_size
        for sprite in self.sprites:
            sprite.draw(self)
