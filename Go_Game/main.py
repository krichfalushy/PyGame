import random
import os
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_w, K_a, K_s, K_d


pygame.init()

FPS = pygame.time.Clock()
HEIGHT = 1000
WIDTH = 1600

FONT = pygame.font.SysFont("Chicago", 124)

COLOUR_WHITE = (255, 255, 255)
COLOUR_BLACK = (0, 0, 0)
COLOUR_ENEMY = (255, 120, 130)
COLOUR_BONUS = (200, 170, 50)

bg = pygame.image.load("/Users/admin/pythonProject1/Go_Game/images/bg.png")
bg_x1 = 0
bg_x2 = bg.get_width()
bg_move = 3

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

player = pygame.image.load("/Users/admin/pythonProject1/Go_Game/images/bird.png").convert_alpha() # pygame.Surface((20, 20))
player_rect = player.get_rect()
player_rect.center = (200, 500)


player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_left = [-4, 0]
player_move_right = [4, 0]


def create_enemy():
    enemy = pygame.image.load("/Users/admin/pythonProject1/Go_Game/images/rocks/rock.png").convert_alpha()
    enemy_rect = pygame.Rect(WIDTH, random.randint(enemy.get_height() + 30,
                                                   HEIGHT-enemy.get_height()-30), *enemy.get_size())
    enemy_move = [-3, 0]
    return [enemy, enemy_rect, enemy_move]


def create_bonus():
    bonus = pygame.image.load("/Users/admin/pythonProject1/Go_Game/images/IMG_9372.png").convert_alpha()
    # bonus.fill(COLOUR_BONUS)
    bonus_rect = pygame.Rect(random.randint(70, WIDTH-70), -bonus.get_height(), *bonus.get_size())
    bonus_move = [0, random.randint(1, 3)]
    return [bonus, bonus_rect, bonus_move]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 3000)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2400)


IMAGES_PATH = "/Users/admin/pythonProject1/Go_Game/images/rocks"
ENEMY_IMAGES = os.listdir(IMAGES_PATH)
IMAGE_INDEX = 0


enemies = []
bonuses = []
score = 0

playing = True

while playing:
    FPS.tick(300)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
            CHANGE_IMAGE = pygame.USEREVENT + 3
            pygame.time.set_timer(CHANGE_IMAGE, 6000)

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

    bg_x1 -= bg_move
    bg_x2 -= bg_move

    if bg_x1 < -bg.get_width():
        bg_x1 = bg.get_width()
    if bg_x2 < -bg.get_width():
        bg_x2 = bg.get_width()

    main_display.blit(bg, (bg_x1, 0))
    main_display.blit(bg, (bg_x2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] or keys[K_s] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] or keys[K_w] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_LEFT] or keys[K_a] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    if keys[K_RIGHT] or keys[K_d] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    for enemy in enemies:
        enemy[0] = pygame.image.load(os.path.join(IMAGES_PATH, ENEMY_IMAGES[IMAGE_INDEX]))
        IMAGE_INDEX += 1
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
        if player_rect.colliderect(enemy[1]):
            playing = False
        if IMAGE_INDEX >= len(ENEMY_IMAGES):
            IMAGE_INDEX = 0

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOUR_WHITE), (WIDTH-160, 40))
    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
