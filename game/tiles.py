import pygame
import os
from game.globals import *

# индификатор и названия файлов к ним
TEXTURE_KEYS = {
    0: None,
    1: "wall",
    2: "brick",
    3: "bricks",
    4: "stone",
    5: "coin",
    6: "end"
}

# получить список всех папок (в нужной нам директории)
def read_folders(path):
    return [e for e in os.listdir(path) if os.path.isdir(path + e)]

# получить список всех файлов (в нужной нам директории)
def read_files(path):
    return [e for e in os.listdir(path) if not os.path.isdir(path + e)]

# класс который хранит картинки мира
class Tiles:
    def __init__(self, scale=1):
        self.tiles_img = {}
        # загрузка изображений
        self.image_width = TEXTURE_WIDTH * scale
        for file in read_files(IMG_PATH + "world/"):
            image = pygame.image.load(IMG_PATH + "world/%s" % (file)).convert_alpha()
            image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
            self.tiles_img[file.split(".")[0]] = image

    # получить ширину 1 изображения (они все одинаковые)
    def get_image_width(self):
        return self.image_width

    # получить изображение 1 тайла
    def get_by_id(self, id):
        return self.tiles_img[TEXTURE_KEYS[id]]
