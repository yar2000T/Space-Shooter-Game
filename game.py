import pygame
from time import sleep
import sys
from pygame.locals import *
from random import randrange

pygame.init()
screen = pygame.display.set_mode((0,0),pygame.RESIZABLE)
clock = pygame.time.Clock()

#----GAME VARIABLES-----
WIDTH = screen.get_width()
HEIGHT = screen.get_height()
player = pygame.transform.scale(pygame.image.load("assests\\spaceship.png").convert_alpha(), (100,100))
asteroid = pygame.transform.scale(pygame.image.load("assests\\asteroid.png").convert_alpha(),(50,50))
player_x = 100
player_y = HEIGHT-200
running = True
start = pygame.time.get_ticks()

fade = 255
for i in range(0,85):
    screen.fill((fade,fade,fade))
    pygame.display.flip()
    sleep(0.03)
    fade -= 3

asteroids = []
bullets = []
player_rect = player.get_rect()

player_rect.center = (WIDTH / 2, HEIGHT / 2)
shootLoop = 0

while running:
    screen.fill((0,0,0))
    screen.blit(player, (player_x, player_y))
    if asteroids:
        for i in asteroids:
            screen.blit(asteroid, (i[0],i[1]))

        for i in range(0,len(asteroids)):
            asteroids[i] = (asteroids[i][0],asteroids[i][1]+asteroids[i][2],asteroids[i][2])

    if (pygame.time.get_ticks() - start) > 500 and shootLoop == 1:
        shootLoop = 0
        start = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()

    if keys[K_RIGHT]:
        if player_x < WIDTH-125:
            player_x += 15
    if keys[K_LEFT]:
        if player_x > 15:
            player_x -= 15
    if keys[K_ESCAPE]:
        running = False
    if keys[K_SPACE] and shootLoop == 0:
        bullets.append((player_x + 45, player_y, 10, 20, 5)) # x, y, width, height, speed
        shootLoop = 1

    for i in range(0,len(bullets)):
        try:
            pygame.draw.rect(screen, (255, 255, 0), (bullets[i][0], bullets[i][1], bullets[i][2], bullets[i][3]))
            bullets[i] = (bullets[i][0], bullets[i][1]-bullets[i][4], bullets[i][2], bullets[i][3], bullets[i][4])

            for j in range(0,len(asteroids)):
                if bullets[i][1] < asteroids[j][1] + 50 and bullets[i][1] + bullets[i][3] > asteroids[j][1]:
                    if bullets[i][0] + bullets[i][2] > asteroids[j][0] and bullets[i][0] < asteroids[j][0] + 50:
                        asteroids.pop(j)
                        bullets.pop(i)
                        break
        except:
            pass

    if randrange(1,50) == 2:
        asteroids.append((randrange(30,WIDTH-130),0,randrange(1,3)))

    for i in asteroids:
        if i[1] + 50 > player_y and i[1] < player_y + 100:
            if i[0] + 50 > player_x and i[0] < player_x + 100:
                running = False

    pygame.display.update()
    pygame.event.pump()
    clock.tick(60)

font = pygame.font.Font(None, 70)
text = font.render("Game Over!", True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.center = (WIDTH / 2, HEIGHT / 2)

screen.blit(text,(WIDTH / 2-100, HEIGHT / 2))
pygame.display.update()

sleep(5)
pygame.quit()