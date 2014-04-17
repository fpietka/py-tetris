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

        empty_lines = list()
        for line, details in lines.iteritems():
            if details['count'] == 10:
                for sprite in details['sprites']:
                    group = pygame.sprite.Group()
                    group.add(sprite)
                    group.clear(self, self.background)
                    sprite.kill()
                    # XXX sprite is gone, but we need to erase the line
                    #       then move every other sprites down
                    #sprite.clear(self, self.background)
                    empty_lines.append(line)

        if empty_lines:
            self.blit(self.background, (0, 0))

        for empty_line in empty_lines:
            for line, details in lines.iteritems():
                if line > empty_line:
                    for sprite in details['sprites']:
                        sprite.rect.top -= self.block_size
                        self.draw(sprite)

