import pygame
import json
from game.globals import *

def save_dict(dict, name):
    json.dump(dict, open(str(name) + '.json','w'), indent=2)

def read_dict(name):
    with open(str(name) + '.json', encoding='utf-8') as fh:
        data = json.load(fh)
    return data

# класс отвечающий за загрузку мира и коллизию с ним
class World:
    def __init__(self):
        self.map = []
        self.obj = None
        self.size = [0, 0]
        self.win_flag = False

    # загрузка карты
    def read_world(self, name):
        self.obj = read_dict("levels/" + name)
        self.map = self.obj['world']
        self.size = [
            len(self.map[0]),
            len(self.map)
        ]
        self.player_pos = self.obj['player']
        self.enemy = self.obj['enemy']

    # проверить коллизию с миром по позиции
    def check_collide(self, x, y, enemy=False, add_score=None):
        xx = int(x)
        yy = int(y)

        # дойти до фалага
        if (self.map[yy + 2][int(x + 0.5)] in [6]):
            self.win_flag = True

        # забрать монету
        if add_score != None:
            if (self.map[yy + 2][int(x + 0.5)] in [5]):
                self.map[yy + 2][int(x + 0.5)] = 0
                add_score(1)

            if (self.map[yy + 1][int(x + 0.5)] in [5]):
                self.map[yy + 1][int(x + 0.5)] = 0
                add_score(1)

        return (self.map[yy + 2][xx] in COLLISION_BLOCKS) or (self.map[yy + 2][xx + 1] in COLLISION_BLOCKS)

    # получить размер мира
    def get_size(self):
        return self.size

    # получить мир (2 мерный массив)
    def get(self):
        return self.map
