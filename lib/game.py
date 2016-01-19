import pygame
import random
from itertools import cycle
from event import Event
from tetrimino import Tetrimino
from matrix import Matrix

"""
Handle speed:
    Level, Frames/drop, Period (sec/drop), Speed (drops/sec)
    ---------------------
    0,    48, .799,  1.25
    1,    43, .715,  1.40
    2,    38, .632,  1.58
    3,    33, .549,  1.82
    4,    28, .466,  2.15
    5,    23, .383,  2.61
    6,    18, .300,  3.34
    7,    13, .216,  4.62
    8,     8, .133,  7.51
    9,     6, .100, 10.02
    10-12, 5, .083, 12.02
    13-15, 4, .067, 15.05
    16-18, 3, .050, 20.03
    19-28, 2, .033, 30.05
    29+,   1, .017, 60.10

"""
SPEEDS = (
        799,
        715,
        632,
        549,
        466,
        383,
        300,
        216,
        133,
        100,
        83,
        67,
        50,
        33,
        17)

black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
purple = (255, 0, 255)
orange = (255, 140, 0)

tetriminos_definitions = (
    {
        'name': 'O',
        'color': yellow,
        'blocks': ((
            (0, 0),
            (1, 0),
            (1, 1),
            (0, 1)
        ),)
    },
    {
        'name': 'I',
        'color': cyan,
        'blocks': ((
            (1, 1),
            (0, 1),
            (2, 1),
            (3, 1)
        ), (
            (1, 1),
            (1, 0),
            (1, 2),
            (1, 3)
        ))
    },
    {
        'name': 'J',
        'color': blue,
        'blocks': ((
            (0, 0),
            (1, 0),
            (2, 0),
            (2, 1)
        ), (
            (2, 0),
            (2, 1),
            (2, 2),
            (1, 2)
        ), (
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 2)
        ), (
            (0, 0),
            (1, 0),
            (0, 1),
            (0, 2)
        ))
    },
    {
        'name': 'L',
        'color': orange,
        'blocks': ((
            (0, 2),
            (1, 2),
            (2, 2),
            (2, 1)
        ), (
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2)
        ), (
            (0, 0),
            (0, 1),
            (1, 0),
            (2, 0)
        ), (
            (2, 0),
            (2, 1),
            (2, 2),
            (1, 0)
        ))
    },
    {
        'name': 'S',
        'color': green,
        'blocks': ((
            (1, 0),
            (0, 1),
            (1, 1),
            (2, 0)
        ), (
            (1, 1),
            (1, 0),
            (2, 1),
            (2, 2)
        ))
    },
    {
        'name': 'T',
        'color': purple,
        'blocks': ((
            (0, 2),
            (1, 1),
            (1, 2),
            (2, 2)
        ), (
            (0, 0),
            (0, 1),
            (1, 1),
            (0, 2)
        ), (
            (0, 0),
            (1, 0),
            (1, 1),
            (2, 0)
        ), (
            (2, 0),
            (1, 1),
            (2, 1),
            (2, 2)
        ))
    },
    {
        'name': 'Z',
        'color': red,
        'blocks': ((
            (1, 0),
            (0, 0),
            (1, 1),
            (2, 1)
        ), (
            (1, 1),
            (1, 0),
            (0, 1),
            (0, 2)
        ))
    }
)

pygame.mixer.pre_init(44100, -16, 1, 256)
pygame.mixer.init()
# sounds
sounds = dict()
sounds["rotate"] = pygame.mixer.Sound("res/rotate.wav")
sounds["fall"] = pygame.mixer.Sound("res/fall.wav")


class Game():
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.running = True
        self.paused = False

        # init fall
        self.event = Event()
        pygame.time.set_timer(self.event.fall, SPEEDS[0])

        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = screen.get_size()

        self.Z_WIDTH, self.Z_HEIGHT = screen.get_size()
        self.Z_WIDTH = self.Z_HEIGHT / 2

        self.B_SIZE = self.Z_WIDTH / 10

        matrix = Matrix((self.Z_WIDTH, self.Z_HEIGHT))

        self.full_background = screen.copy()
        self.background = matrix.copy()
        matrix.background = self.background
        matrix.block_size = self.B_SIZE

        Z_LEFT = screen.get_width() / 2 - matrix.get_width() / 2
        self.Z_LEFT = Z_LEFT

        screen.blit(matrix, (Z_LEFT, 0))

        # init tetriminos
        self.tetrimino = Tetrimino(
                random.choice(tetriminos_definitions),
                self.B_SIZE,
                self.background,
                matrix)
        self.tetrimino.center(self.Z_WIDTH)
        self.tetrimino.draw(matrix)
        screen.blit(matrix, (Z_LEFT, 0))

        self.next_random = random.choice(tetriminos_definitions)
        self.next_tetrimino = Tetrimino(
                self.next_random,
                self.B_SIZE,
                self.full_background,
                screen)
        self.next_tetrimino.center(self.SCREEN_WIDTH + self.Z_WIDTH * 2,
                                   self.SCREEN_HEIGHT / 2)
        self.next_tetrimino.draw(screen)

        self.myfont = pygame.font.Font("res/VCR_OSD_MONO_1.001.ttf", 15)

        level_label = self.myfont.render("Level: {}".format(0), False, white)
        score_label = self.myfont.render("Score: {}".format(0), False, white)
        line_label = self.myfont.render("Lines: {}".format(0), False, white)
        screen.blit(level_label, (self.SCREEN_WIDTH - 180, 50))
        screen.blit(score_label, (self.SCREEN_WIDTH - 180, 75))
        screen.blit(line_label, (self.SCREEN_WIDTH - 180, 100))

        next_label = self.myfont.render("Next", False, white)
        screen.blit(next_label, (self.SCREEN_WIDTH - 120, 200))

        self.pause_font_size = self.myfont.size("PAUSED")
        self.pause_label = self.myfont.render("PAUSED", False, white)

        PAUSE = False
        self.lines = 0
        self.score = 0
        self.level = 0
        self.softdrops = 0
        self.harddrops = 0

        self.matrix = matrix

        pygame.display.update()

    def handleKey(self, key):
        tetrimino = self.tetrimino
        if key in (pygame.K_ESCAPE, pygame.K_q):
            self.running = False
        if key == pygame.K_p:
            if self.paused:
                pygame.time.set_timer(self.event.pause, 0)
                self.matrix = self.game_matrix
                self.paused = False
            else:
                pygame.time.set_timer(self.event.pause, 1000)
                self.paused = True

                self.game_matrix = self.matrix
                unpaused_matrix = self.matrix.copy()
                paused_matrix = self.matrix.copy()

                paused_matrix.blit(self.pause_label,
                                   ((self.Z_WIDTH / 2) - (self.pause_font_size[0] / 2),
                                    (self.Z_HEIGHT / 2) - self.pause_font_size[1]))
                self.pause_matrix = cycle((paused_matrix, unpaused_matrix))

                self.matrix = self.pause_matrix.next()
        if self.paused:
            # do not process any further key
            return
        if key == self.config['KEY_LEFT']:
            tetrimino.moveLeft()
            if tetrimino.isColliding():
                tetrimino.moveRight()
            else:
                tetrimino.clear(self.matrix)
                tetrimino.draw(self.matrix)
        if key == self.config['KEY_RIGHT']:
            tetrimino.moveRight()
            if tetrimino.isColliding():
                tetrimino.moveLeft()
            else:
                tetrimino.clear(self.matrix)
                tetrimino.draw(self.matrix)
        if key == self.config['KEY_DOWN']:
            tetrimino.moveDown()
            if tetrimino.isColliding():
                tetrimino.moveUp()
            else:
                self.softdrops += 1
                tetrimino.clear(self.matrix)
                tetrimino.draw(self.matrix)
        if key in self.config['KEY_ROTATE_RIGHT']:
            if tetrimino.rotate():
                sounds["rotate"].play()
                tetrimino.clear(self.matrix)
                tetrimino.draw(self.matrix)
        if key == self.config['KEY_HARD_DROP']:
            while not tetrimino.isColliding():
                self.harddrops += 1
                tetrimino.moveDown()
            tetrimino.moveUp()
            self.harddrops -= 1
            tetrimino.clear(self.matrix)
            tetrimino.draw(self.matrix)

    def handleFall(self):
        tetrimino = self.tetrimino
        tetrimino.moveDown()
        if tetrimino.isColliding():
            sounds["fall"].play()
            tetrimino.moveUp()
            if tetrimino.isColliding():
                self.running = False
                return
            self.matrix.sprites.append(tetrimino)
            # current from previous next
            tetrimino = Tetrimino(
                self.next_random,
                self.B_SIZE,
                self.background,
                self.matrix
            )
            self.tetrimino = tetrimino
            tetrimino.center(self.Z_WIDTH)
            # random next
            self.next_tetrimino.clear(pygame.Surface((self.SCREEN_WIDTH - self.Z_WIDTH, self.SCREEN_HEIGHT)))
            self.next_tetrimino.clear(self.screen)
            self.next_random = random.choice(tetriminos_definitions)
            self.next_tetrimino = Tetrimino(
                    self.next_random,
                    self.B_SIZE,
                    self.full_background,
                    self.screen)
            self.next_tetrimino.center(self.SCREEN_WIDTH + self.Z_WIDTH * 2,
                                       self.SCREEN_HEIGHT / 2)
            self.next_tetrimino.draw(self.screen)

            if tetrimino.isColliding():
                # gameover
                self.running = False
                return

            empty_lines, points = self.matrix.checkLines()

            self.score += self.softdrops
            self.score += (self.harddrops * 2)
            self.harddrops = 0
            self.softdrops = 0

            if empty_lines:
                # calculcate and display
                self.lines += empty_lines
                self.score += points * (self.level + 1)
                self.level = int(self.lines / 10)

                pygame.time.set_timer(self.event.fall, SPEEDS[self.level])

            level_label = self.myfont.render("Level: {}".format(self.level), False, white)
            score_label = self.myfont.render("Score: {}".format(self.score), False, white)
            line_label = self.myfont.render("Lines: {}".format(self.lines), False, white)

            # reset score zone
            rect = pygame.Rect(self.SCREEN_WIDTH - 180, 0, self.SCREEN_WIDTH, 200)
            self.screen.fill(black, rect)

            self.screen.blit(level_label, (self.SCREEN_WIDTH - 180, 50))
            self.screen.blit(score_label, (self.SCREEN_WIDTH - 180, 75))
            self.screen.blit(line_label, (self.SCREEN_WIDTH - 180, 100))

            tetrimino.draw(self.matrix)
        else:
            tetrimino.clear(self.matrix)
            tetrimino.draw(self.matrix)

    def handleEvents(self, event):
        if event.type == pygame.KEYDOWN:
            self.handleKey(event.key)

        if event.type == self.event.pause:
            self.matrix = self.pause_matrix.next()

        if self.paused:
            self.screen.blit(self.matrix, (self.Z_LEFT, 0))
            return self.running

        if event.type == self.event.fall:
            self.handleFall()

        self.screen.blit(self.matrix, (self.Z_LEFT, 0))
        return self.running
