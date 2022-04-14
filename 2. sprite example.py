import pygame
import random

#setting up constants
width = 800
height = 600
fps = 30

#define color constants
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

class Player(pygame.sprite.Sprite): #sprite for the player class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)   #you always have to include this line otherwise it won't function
        self.image = pygame.Surface((50, 50))   #surface is a thing you can draw on in pygame
        self.image.fill(green)
        self.rect = self.image.get_rect()   #the rect is almost like the hitbox. It allows you to know where it is and where you want it to be
        self.rect.center = (width / 2, height / 2)

    def update(self):   #whenever there the update loop is running, these things will happen to the player
        self.rect.x += 5    #keep moving the player to the right by 5 pixels
        if self.rect.left > width:  #if the left side of the rect is greater than the width
            self.rect.right = 0   #shift the right side of the rect back to 0. This will keep the rect from going off screen

#initialize pygame and create window
pygame.init()   #always have this for your game to run
pygame.mixer.init() #this mixer handles all the music and sound effects
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Prototype")
clock = pygame.time.Clock()


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



