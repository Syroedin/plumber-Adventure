
from game.globals import *

class Camera:
    def __init__(self):
        self.pos = [0, 0]

    # установка позиции игрока
    def set_pos(self, x):
        self.pos[0] = (WIDTH/2) -x

    # получение позиции игрока
    def get_pos(self):
        return self.pos
