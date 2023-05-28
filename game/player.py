import pygame
import time
from game.globals import *

class Player:
    # конструктор класса игрока
    def __init__(self, scale=1, start_pos=[0, 0], check_collide=None):
        self.images = [[], []]
        # загрузка изображений
        for i in range(4):
            self.images[0].append(pygame.image.load(IMG_PATH + 'player/%d.png' % (i)).convert_alpha())
            self.images[0][-1] = pygame.transform.scale(self.images[0][-1], (self.images[0][-1].get_width() * scale, self.images[0][-1].get_height() * scale))
            self.images[1].append(pygame.transform.flip(self.images[0][-1], True, False))

        image = pygame.image.load(IMG_PATH + 'player/jump.png').convert_alpha()
        image = pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
        self.image_jump = [image, pygame.transform.flip(image, True, False)]

        # переменные отвечающие за передвижение
        self.jump_bool = False
        self.jump_timer = 1
        self.y_collide = True
        self.start_pos = start_pos
        self.pos = [self.start_pos[0], self.start_pos[1]]
        self.speed = 0
        self.velocity = 0
        self.move_flag = False
        self.fall_speed = PLAYER_SPEED

        # таймеры анимаций
        self.animation_frame = 0
        self.animation_delay = 0.1
        self.animation_time = time.perf_counter() + self.animation_delay

        # указатель на метод проверки коллизиии
        self.check_collide = check_collide

        # информация для интерфейса
        self.lifes = 3
        self.score = 0

    # смерть
    def dead(self):
        self.lifes -= 1
        if self.lifes <= 0:
            return
        self.pos = [self.start_pos[0], self.start_pos[1]]

    # добавление монет в копилку
    def add_score(self, score):
        self.score += score

    # передвижение
    def move(self, left=False):
        self.velocity = 1 if left else 0
        self.speed = -PLAYER_SPEED if left else PLAYER_SPEED
        self.move_flag = True

    # остановка передвижения
    def stop_move(self):
        self.move_flag = False
        self.animation_frame = 0

    # прыжок
    def jump(self):
        if not self.jump_bool and self.y_collide:
            self.jump_bool = True
            self.jump_timer = 4
            self.y_collide = False

    def stop_jump(self):
        pass
        # self.jump_timer = 0
        # self.fall_speed = PLAYER_SPEED
        # self.jump_bool = False

    # обновление состояния
    def update(self):
        try:
            set_y_flag = True
            set_x_flag = True

            if self.jump_bool:
                self.jump_timer -= 0.1
                if self.jump_timer > 0:
                    self.pos[1] -= PLAYER_SPEED*self.jump_timer
                else:
                    self.pos[1] += PLAYER_SPEED*abs(self.jump_timer)

            # проверка коллизиии по Y
            if self.check_collide(self.pos[0], self.pos[1] + self.fall_speed, add_score=self.add_score):
                self.y_collide = True
                set_y_flag = False
                self.jump_bool = False
                self.pos[1] = int(self.pos[1] + self.fall_speed)
            else:
                self.jump_bool = True

            # проверка коллизиии по X
            if self.check_collide(self.pos[0] + self.speed, self.pos[1] - 1, add_score=self.add_score):
                set_x_flag = False

            if set_y_flag:
                self.pos[1] += self.fall_speed

            if not self.move_flag:
                return

            self.animation()

            if set_x_flag:
                self.pos[0] += self.speed
        except:
            self.dead()

    # тик анимации
    def animation(self):
        if (self.animation_time <= time.perf_counter()):
            self.animation_frame += 1
            if len(self.images[0]) <= self.animation_frame:
                self.animation_frame = 1

            self.animation_time = time.perf_counter() + self.animation_delay

    # вывод изображения
    def get(self):
        if self.jump_bool:
            image = self.image_jump[self.velocity]
        else:
            image = self.images[self.velocity][self.animation_frame]
        return image, self.pos
