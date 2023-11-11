import pygame
import random
import math
from pygame import mixer

pygame.init()

# displaywindow
screen = pygame.display.set_mode((1200, 800))

# background
bg = pygame.image.load("background2.jpg")

# bgmusic
mixer.music.load('bgm.mp3')
mixer.music.play(-1)

# Title nd Icon
pygame.display.set_caption("GALAGA")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# playerspaceship
playerimg = pygame.image.load('spaceship.png')
playerx = 570
playery = 680
playerx_change = 0

# alienspaceship
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num = 6
for i in range(num):
    enemyimg.append(pygame.image.load('alien.png'))
    enemyx.append(random.randint(0, 1136))
    enemyy.append(random.randint(50, 300))
    enemyx_change.append(4)
    enemyy_change.append(40)

# bullet
bulletimg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 680
bulletx_change = 0
bullety_change = 10
bulletstate = 'ready'

# score
score_val = 0
font = pygame.font.Font('Nervous.ttf', 32)
fx = 10
fy = 10

# gameover
gofont = pygame.font.Font('Gameplay.ttf', 84)


def scores(x, y):
    score = font.render("Score :" + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def gameover():
    go = gofont.render("Game Over", True, (255, 255, 255))
    screen.blit(go, (300, 350))


def player(x, y):
    screen.blit(playerimg, (x, y))


def alien(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def bullet(x, y):
    global bulletstate
    bulletstate = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))


def collision(enemyx, enemyy, bulletx, bullety):
    dis = math.sqrt(math.pow(enemyx - bulletx, 2) + math.pow(enemyy - bullety, 2))
    if dis < 27:
        return True
    else:
        return False


# gameloop
running = True
while running:
    # rgbsetting
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keypressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -4
            if event.key == pygame.K_RIGHT:
                playerx_change = 4
            if event.key == pygame.K_SPACE:
                if bulletstate == 'ready':
                    bsound = mixer.Sound('laser.mp3')
                    bsound.play()
                    bulletx = playerx
                    bullet(bulletx, bullety)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # plsyermovement
    playerx += playerx_change

    if playerx <= 0:
        playerx = 0
    elif playerx >= 1136:
        playerx = 1136

    # enemymovement
    for i in range(num):

        # game over
        if enemyy[i] > 640:
            for j in range(num):
                enemyy[j] = 2000
            gameover()
            break

        enemyx[i] += enemyx_change[i]

        if enemyx[i] <= 0:
            enemyx_change[i] = 2
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 1136:
            enemyx_change[i] = -2
            enemyy[i] += enemyy_change[i]

        # coliision
        col = collision(enemyx[i], enemyy[i], bulletx, bullety)
        if col:
            colsound = mixer.Sound('explosion.wav')
            colsound.play()
            bullety = 680
            bulletstate = 'ready'
            score_val += 1
            enemyx[i] = random.randint(0, 1136)
            enemyy[i] = random.randint(50, 300)

        alien(enemyx[i], enemyy[i], i)

    # bulletmovement
    if bullety <= 0:
        bullety = 680
        bulletstate = 'ready'

    if bulletstate == "fire":
        bullet(bulletx, bullety)
        bullety -= bullety_change

    player(playerx, playery)
    scores(fx, fy)
    pygame.display.update()
