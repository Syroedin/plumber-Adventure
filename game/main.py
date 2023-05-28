
import pygame
import sys

from game.globals import *
from game.world import *
from game.player import *
from game.enemy import *
from game.camera import *
from game.tiles import *
from game.score import *

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_a,
    K_s,
    K_d,
    K_r,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT,
)

################################################################################

keys = {
    K_a: True,
    K_LEFT: True,
    K_d: False,
    K_RIGHT: False
}

################################################################################

pygame.init()

FramePerSec = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plumber Adventure")

# загрузка шрифтов
FONT_BIG = pygame.freetype.Font("game/assets/font/pixel.ttf", 128)
FONT = pygame.freetype.Font("game/assets/font/pixel.ttf", 72)

################################################################################

# пустые объекты
world = None
SCALE = None
tiles = None
player = None
camera = None
score_label = None
enemy_list = None

# флаги состояния игры
dead_flag = False
win_flag = False

# запуск игры (или перезгрузка)
def start():
    global world
    global SCALE
    global tiles
    global player
    global camera
    global enemy_list
    global score_label

    dead_flag = False
    win_flag = False

    world = World()
    world.read_world("1_1")

    SCALE = HEIGHT/(world.get_size()[1] * TEXTURE_WIDTH)

    tiles = Tiles(
        scale = SCALE
    )

    player = Player(
        scale = SCALE,
        start_pos = world.player_pos,
        check_collide = world.check_collide
    )

    enemy_list = []
    for el in world.enemy:
        enemy_list.append(Enemy(
            scale = SCALE,
            start_pos = el['pos'],
            type = el['type'],
            check_collide = world.check_collide
        ))

    camera = Camera()

    score_label = Score_label(
        scale = SCALE
    )

start()

################################################################################

# полупрозрачный чёрный фон
def draw_back_bg():
    s = pygame.Surface((WIDTH, HEIGHT))
    s.set_alpha(128)
    s.fill((0,0,0))
    screen.blit(s, (0, 0))

# вывод того что мы умерли
def dead():
    draw_back_bg()
    FONT_BIG.render_to(screen, (WIDTH/2.55, HEIGHT/4 + (70 * 2)), "GAME OVER", (200,10,10))
    FONT.render_to(screen, (WIDTH/2.6, HEIGHT - HEIGHT/4), "press [R] to restart", (200,200,200))

# вывод того что мы победили
def win():
    draw_back_bg()
    FONT_BIG.render_to(screen, (WIDTH/2.55, HEIGHT/4 + (70 * 2)), "YOU WIN", (200,10,10))
    FONT.render_to(screen, (WIDTH/2.6, HEIGHT - HEIGHT/4), "press [R] to restart", (200,200,200))

################################################################################

# основной игровой цикл
while True:
    # голубой фон
    screen.fill((146, 144, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # обработка нажатия клавиш
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == K_SPACE:
                player.jump()

            if event.key in keys:
                player.move(keys[event.key])

            if event.key == K_r:
                start()

        # обработка отжатия клавиш
        elif event.type == KEYUP:
            if event.key in keys:
                player.stop_move()

            if event.key == K_SPACE:
                player.stop_jump()

    # обновляем состояния игрока и врагов если мы не умерли
    if player.lifes > 0 and not world.win_flag:
        player.update()

        for el in enemy_list:
            el.update()
            # проверка коллизиии с игроком
            el.check_collide_enemy(player.pos[0], player.pos[1], player.jump_bool, player.dead)

    # передаём камере текущую позицию игрока
    camera.set_pos(
        player.pos[0] * tiles.get_image_width()
    )

    # рисуем карту
    for y, row in enumerate(world.get()):
        for x, el in enumerate(row):
            if el != 0:
                screen.blit(
                    tiles.get_by_id(el),
                    (
                        camera.get_pos()[0] + x * tiles.get_image_width(),
                        camera.get_pos()[1] + y * tiles.get_image_width()
                    )
                )

    # если не конец игры, то рисуем игрока
    if player.lifes > 0 and not world.win_flag:
        image, pos = player.get()
        screen.blit(
            image,
            (
                WIDTH/2,
                pos[1] * tiles.get_image_width()
            )
        )

    # если враг жив, то рисуем его
    for el in enemy_list:
        if not el.dead:
            image, pos = el.get()
            screen.blit(
                image,
                (
                    camera.get_pos()[0] + pos[0] * tiles.get_image_width(),
                    camera.get_pos()[1] + pos[1] * tiles.get_image_width()
                )
            )

    # рисуем интерфейс (жизни и монеты)
    score_label.draw(screen, player.lifes, player.score)

    # в зависимости от текущего состояния выводм разные сообщения
    if player.lifes <= 0:
        dead()

    if world.win_flag:
        win()

    # обновляем экран
    pygame.display.update()
    FramePerSec.tick(FPS)
