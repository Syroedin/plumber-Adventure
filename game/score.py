import pygame
from game.globals import *

class Score_label:
    def __init__(self, scale=1):
        # загрузка картинки сердца
        self.life_img = pygame.image.load(IMG_PATH + 'life.png').convert_alpha()
        self.life_img = pygame.transform.scale(self.life_img, (self.life_img.get_width() * scale, self.life_img.get_height() * scale))

        # загрузка картинки монеты
        self.coin_img = pygame.image.load(IMG_PATH + 'world/coin.png').convert_alpha()
        self.coin_img = pygame.transform.scale(self.coin_img, (self.coin_img.get_width() * scale, self.coin_img.get_height() * scale))

        # загрузка шрифта (для вывода количества монет)
        self.font = pygame.freetype.Font("game/assets/font/pixel.ttf", 72)

    # рисуем интерфейс
    def draw(self, screen, lifes, coins):
        # количество жизней
        for i in range(lifes):
            screen.blit(
                self.life_img,
                (
                    WIDTH/20 + (self.life_img.get_width() * i + self.life_img.get_width()/4),
                    HEIGHT/20
                )
            )

        # количество собранных монет
        screen.blit(
            self.coin_img,
            (
                WIDTH/20,
                HEIGHT/20 + self.life_img.get_width() * 1.2
            )
        )

        self.font.render_to(screen, (WIDTH/20 + self.life_img.get_width() * 1.2, HEIGHT/20 + self.life_img.get_width() * 1.4), str(coins), (200,200,200))
