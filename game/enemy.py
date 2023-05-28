import pygame
import time
from game.globals import *

class Enemy:
    # конструктор класса врага
    def __init__(self, scale, start_pos=[0, 0], type="grib", check_collide=None):
        self.images = []
        # загрузка изображений
        for i in range(2):
            self.images.append(pygame.image.load(IMG_PATH + 'enemy/%s/%d.png' % (type, i)).convert_alpha())
            self.images[-1] = pygame.transform.scale(self.images[-1], (self.images[-1].get_width() * scale, self.images[-1].get_height() * scale))

        # таймеры анимаций
        self.animation_frame = 0
        self.animation_delay = 0.2
        self.animation_time = time.perf_counter() + self.animation_delay

        # текущая поцзиция
        self.pos = start_pos
        self.align = 0 # 0 - left; 1 - right

        # указатель на метод проверки коллизиии
        self.check_collide = check_collide

        self.dead = False
        self.speed = PLAYER_SPEED/2

    # смерть
    def dead_func(self):
        self.dead = True

    # тик анимации
    def animate(self):
        if (self.animation_time <= time.perf_counter()):
            self.animation_frame += 1
            if len(self.images) <= self.animation_frame:
                self.animation_frame = 0

            self.animation_time = time.perf_counter() + self.animation_delay

    # обновление состояния
    def update(self):
        speed = -self.speed if self.align == 0 else self.speed
        # проверка коллизии по X (если столкнулись, то меняем направление движения)
        if self.check_collide(self.pos[0] + speed, self.pos[1] - 2, enemy=True):
            self.align = 1 if self.align == 0 else 0
            return

        self.animate()
        self.pos[0] += speed

    # проверка коллизии с игроком
    def check_collide_enemy(self, x, y, jump=False, dead_func=None):
        xx = round(x)
        yy = round(y)

        if (round(self.pos[0]) == xx) and (round(self.pos[1]) == (yy + 2)):
            self.dead_func()

        if (round(self.pos[0]) == xx) and (round(self.pos[1]) == (yy + 1)) and not self.dead:
            dead_func()

    # вывод изображения
    def get(self):
        return self.images[self.animation_frame], self.pos
