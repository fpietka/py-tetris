import pygame


class Matrix(pygame.Surface):
    def __init__(self, *args):
        pygame.Surface.__init__(self, *args)
        pygame.draw.rect(self, (255, 255, 255), self.get_rect(), 1)
        self.sprites = list()
        self.sounds = dict()
        self.sounds["line"] = pygame.mixer.Sound("res/line.wav")
        self.sounds["tetris"] = pygame.mixer.Sound("res/tetris.wav")
        self.scores = (40, 100, 300, 1200)

    def checkLines(self):
        lines = dict()
        # loop for all groups of sprites
        for sprite in self.sprites:
            # then all sprites within
            for block in sprite.sprites():
                # group them by line
                if block.rect.top in lines:
                    lines[block.rect.top]['count'] += 1
                    lines[block.rect.top]['sprites'].append(block)
                else:
                    lines[block.rect.top] = dict()
                    lines[block.rect.top]['count'] = 1
                    lines[block.rect.top]['sprites'] = list()
                    lines[block.rect.top]['sprites'].append(block)

        empty_lines = [(line / self.block_size, details['sprites'])
                       for line, details
                       in lines.iteritems()
                       if details['count'] == 10]
        for empty_line in empty_lines:
            # clear matrix
            self.blit(self.background, (0, 0))
            for sprite in empty_line[1]:
                sprite.kill()
        move_down_blocks = list()
        for sprite in self.sprites:
            for block in sprite.sprites():
                for empty_line in empty_lines:
                    # move sprites down
                    if block.rect.top / self.block_size < empty_line[0]:
                        move_down_blocks.append(block)
        # then move down for each occurence in the list
        for block in move_down_blocks:
            block.rect.top += self.block_size

        score = 0
        if empty_lines:
            score = self.scores[len(empty_lines) - 1]

            # redraw sprites
            for sprite in self.sprites:
                sprite.draw(self)
            if len(empty_lines) == 4:
                self.sounds["tetris"].play()
            else:
                self.sounds["line"].play()
        return len(empty_lines), score
