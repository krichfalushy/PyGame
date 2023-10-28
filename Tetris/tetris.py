import pygame
from copy import deepcopy
from random import choice, randrange


pygame.init()

# HEIGHT = 1000
# WIDTH = 800
COLOUR_BLACK = (0, 0, 0)
W, H = 15, 25
BAR = 45
RES = 1000, 1165
FPS = pygame.time.Clock()

screen = pygame.display.set_mode(RES)
main_display = pygame.Surface((W * BAR, H * BAR))

GRID = [pygame.Rect(x * BAR, y * BAR, BAR, BAR) for x in range(W) for y in range(H)]

FONT = pygame.font.Font("/Users/admin/pythonProject1/Tetris/cat-north-shadow.ttf", 70)
font = pygame.font.Font("/Users/admin/pythonProject1/Tetris/bpdots-squares-2.ttf", 50)
font_over = pygame.font.Font("/Users/admin/pythonProject1/Tetris/bpdots-squares-2.ttf", 120)

TITLE = FONT.render("TETRIS", True, pygame.Color("#f0932b"))
title_score = font.render("Score:", True, pygame.Color("#f0932b"))
game_over = font_over.render("GAME OVER", True, pygame.Color("#eb4d4b"))


def get_colour():
    return randrange(30, 256), randrange(30, 256), randrange(30, 256)


figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
              [(0, -1), (-1, -1), (-1, 0), (0, 0)],
              [(-1, 0), (-1, 1), (0, 0), (0, -1)],
              [(0, 0), (-1, 0), (0, 1), (-1, -1)],
              [(0, 0), (0, -1), (0, 1), (-1, -1)],
              [(0, 0), (0, -1), (0, 1), (1, -1)],
              [(0, 0), (0, -1), (0, 1), (-1, 0)]]


figures = [[pygame.Rect(x + (W // 2), y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, BAR - 2, BAR - 2)

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
colour, next_colour = get_colour(), get_colour()

anim_count, anim_speed, anim_limit = 0, 60, 2000

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

field = [[0 for i in range(W)] for j in range(H)]


def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


playing = True

while playing:
    dx, rotate = 0, False
    FPS.tick(60)
    screen.fill(pygame.Color("#34495e"))
    screen.blit(main_display, (20, 20))
    main_display.fill(pygame.Color("#34495e"))

    # draw grid
    [pygame.draw.rect(main_display, (40, 40, 40), i_rect, 1) for i_rect in GRID]

    # delay for full lines
    for i in range(lines):
        pygame.time.wait(200)

    # keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            if event.key == pygame.K_RIGHT:
                dx = 1
            if event.key == pygame.K_DOWN:
                anim_limit = 300
            if event.key == pygame.K_UP:
                anim_limit = 2000
            if event.key == pygame.K_SLASH:
                rotate = True

    figure_old = deepcopy(figure)

    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break

    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for j in range(4):
                    field[figure_old[j].y][figure_old[j].x] = colour
                figure, colour = next_figure, next_colour
                next_figure, next_colour = deepcopy(choice(figures)), get_colour()
                anim_limit = 2000
                break

    centre = figure[0]
    if rotate:
        for i in range(4):
            x = figure[i].y - centre.y
            y = figure[i].x - centre.x
            figure[i].x = centre.x - x
            figure[i].y = centre.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break

    # check last line
    line, lines = H - 1, 0
    for row in range(H-1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            anim_speed += 3
            lines += 1

    # scores
    score += scores[lines]

    # draw figure
    for i in range(4):
        figure_rect.x = figure[i].x * BAR
        figure_rect.y = figure[i].y * BAR
        pygame.draw.rect(main_display, colour, figure_rect)

    # draw bg for next figure
    pygame.draw.rect(screen, pygame.Color("#95afc0"), (745, 273, 220, 225), 5, 20)

    # draw next figure
    for i in range(4):
        figure_rect.x = next_figure[i].x * BAR + 542
        figure_rect.y = next_figure[i].y * BAR + 320
        pygame.draw.rect(screen, next_colour, figure_rect)

    # draw field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * BAR, y * BAR
                pygame.draw.rect(main_display, col, figure_rect)

    # text
    screen.blit(TITLE, (700, 30))
    screen.blit(title_score, (740, 700))
    screen.blit(font.render(str(score), True, pygame.Color("white")), (740, 770))

    # game over
    for i in range(W):
        if field[0][i]:
            text_rect = game_over.get_rect()
            screen.blit(game_over, (100, 583))
            FPS.tick(8000)
            field = [[0 for i in range(W)] for j in range(H)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            pygame.display.update()
            playing = False

    pygame.display.flip()


