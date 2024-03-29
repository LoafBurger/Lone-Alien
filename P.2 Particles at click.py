# Setup Python ----------------------------------------------- #
import pygame, sys, random
 
# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((500, 500),0,32)
 
 
# [loc, velocity, timer]
particles = []
 

clicking = False
 
# Loop ------------------------------------------------------- #
while True:
    
    # Background --------------------------------------------- #
    screen.fill((0,0,0))
    mx, my = pygame.mouse.get_pos()
 
    # Particles ---------------------------------------------- #
    if clicking:
        for i in range(20):
            particles.append([[mx, my], [random.randint(0, 42) / 6 - 3.5, random.randint(0, 42) / 6 - 3.5], random.randint(4, 6)])
 
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.035
        particle[1][1] += 0.15
        pygame.draw.circle(screen, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        if particle[2] <= 0:
            particles.remove(particle)
 
    
    # Buttons ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
 
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                clicking = True
 
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                clicking = False
                
    # Update ------------------------------------------------- #
    pygame.display.update()
    mainClock.tick(60)