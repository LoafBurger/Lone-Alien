#This will be your pygame template or skeleton for all your games
#resources: https://opengameart.org/
#resources: kite will be a good place to understand pygame methods

import pygame
import random

#setting up constants
width = 360
height = 480
fps = 30

#define color constants
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#initialize pygame and create window
pygame.init()   #always have this for your game to run
pygame.mixer.init() #this mixer handles all the music and sound effects
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Prototype")
clock = pygame.time.Clock()


all_sprites = pygame.sprite.Group() #this allows us to call a group of sprites at the same time
#game loop
running = True
while running:
    clock.tick(fps)     #this solves lag

    # 1.process input(events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #check for closing the window
            running = False

    # 2.update
    all_sprites.update()

    # 3.draw or render
    screen.fill(black)
    all_sprites.draw(screen)    #this is where the sprite group comes in handy
    pygame.display.flip()   #always do this last, draw everything and then flip the display

pygame.quit()