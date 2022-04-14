#shoot em up

import pygame
import random

#setting up constants
width = 480
height = 600
fps = 60

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
pygame.display.set_caption("shmup")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.speedx = 0     #this will tell us the speed the player gets whenever it moves

    def update(self):   #remember, this method is called one everytime the game updates
        self.speedx = 0
        keystate = pygame.key.get_pressed()     #this gives us the values of the keys that are being pressed at that instant
        if keystate[pygame.K_LEFT]:     #if you want to use the a key, do K_a
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:    #if you want to use the d key, do K_d
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.right > width:     #instead of lesson 2 where we bring them back, this stops the player from moving
            self.rect.right = width
        if self.rect.left < 0:      #instead of lesson 2 where we bring them back, this stops the player from moving
            self.rect.left = 0


all_sprites = pygame.sprite.Group() #this allows us to call a group of sprites at the same time
player = Player()
all_sprites.add(player)
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