from pygame import USEREVENT


class Event():
    def __init__(self):
        self.fall = USEREVENT + 1
        self.pause = USEREVENT + 2
