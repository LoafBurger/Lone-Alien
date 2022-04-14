#until this point, we have been using aabb or axis aligned bounding box. In order to improve collision accuracy, we are going to start using circular bounds
#fun thought is that you dont have to be perfect because if a player is able to dodge it, they might think they are really good and stuff


#shoot em up game
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), "img")  #whatever file we are in and whatever the path we are in to that img


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
yellow = (255, 255, 0)  

#initialize pygame and create window
pygame.init()   #always have this for your game to run
pygame.mixer.init() #this mixer handles all the music and sound effects
screen = pygame.display.set_mode((width, height))   #this will configure the dimensions of your game
pygame.display.set_caption("shmup") #the name of the application when it's open
clock = pygame.time.Clock() #creates an object that helps track time (fps)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))   #this allows you to resize and transform image as well as add graphics
        self.image.set_colorkey(black)  #this allows you to get rid of a lot of the black color spaces and outline that you dont need
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius) YOU CAN USE THESE LINES TO TEST THE CIRCLE BOUNDS OF AN OBJECT
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.speedx = 0     #this will tell us the speed the player gets whenever it moves

    def update(self):   #remember, this method is called one everytime the game updates(called in the update section below)
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

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pygame.sprite.Sprite):   #this will be the class for the sprite of the mobs
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = meteor_img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius) YOU CAN USE THESE LINES TO TEST THE CIRCLE BOUNDS OF AN OBJECT
        self.rect.x = random.randrange(0, width - self.rect.width)  #you can choose to leave the 0 out because python will assume its the range to the end
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx  #this makes the enemy sprite move left and right randomly
        self.rect.y += self.speedy  #this makes the enemy sprite move down at random speeds
        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 20: #if it ever goes back to the bottom, we randomize the location back at the top. or if it goes off screen on the left or the right
            self.rect.x = random.randrange(0, width - self.rect.width)  #you can choose to leave the 0 out because python will assume its the range to the end
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    
    def update(self):   
        self.rect.y += self.speedy
        if self.rect.bottom < 0:    #this is if the bullet flies off the screen then we kill it
            self.kill()


#load all game graphics (main part for part 7)
background = pygame.image.load(path.join(img_dir, "spacebg.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_red.png")).convert()
meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserBlue16.png")).convert()



all_sprites = pygame.sprite.Group() #this allows us to call a group of sprites at the same time
mobs = pygame.sprite.Group()    #this will come in handy when we want to see if they collide with something
bullets = pygame.sprite.Group() #this allows us to add the bullets a part of a bullets group
player = Player()
all_sprites.add(player)
for i in range (8): #generates 8 different mobs
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

#game loop
running = True
while running:
    clock.tick(fps)     #this solves lag

    # 1.process input(events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #check for closing the window
            running = False
        elif event.type == pygame.KEYDOWN:  #if the player decides to shoot, then check if it is the space key
            if event.key == pygame.K_SPACE:
                player.shoot()

    # 2.update
    all_sprites.update()
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)    #check to see if a bullet hits the mobs
    for hit in hits:    #if you call mobs, they will always come back
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)  #MAKE SURE TO ADD THE LAST PARAMETER TO MAKE IT CIRCLE BOUNDS INSTEAD OF DEFAULT BOX BOUNDS    #we are going to check to see if a mob hit the player. The false is asking if you should delete upon collision. This thing will return a list
    if hits:    #if a list is empty, it is false. if hits has something, then it is true
        running = False


    # 3.draw or render
    screen.fill(black)
    screen.blit(background, background_rect)   #THIS ALLOWS YOU TO HAVE A BACKGROUND
    all_sprites.draw(screen)    #this is where the sprite group comes in handy
    pygame.display.flip()   #always do this last, draw everything and then flip the display


pygame.quit()