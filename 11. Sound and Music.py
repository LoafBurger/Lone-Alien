#shoot em up game

import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), "img")  #whatever file we are in and whatever the path we are in to that img
snd_dir = path.join(path.dirname(__file__), "snd")  #this is so you can access the music folder and whatever sound
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

#SCORE AND DRAWING TEXT
font_name = pygame.font.match_font("arial") #setting up the fonts in order to show for this draw text function
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)    #using the fontname
    text_surface = font.render(text, True, white)   #THE TRUE MAKES THINGS A LOT SMOOTHER (ANTI ALIASED)
    text_rect = text_surface.get_rect() #setting up the surface
    text_rect.midtop = (x,y) #middle and top
    surf.blit(text_surface, text_rect)  #draws it on the screen

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #always include this when you are creating an object using pygame
        self.image = pygame.transform.scale(player_img, (50, 38))   #this allows you to resize and transform image as well as add graphics
        self.image.set_colorkey(black)  #this allows you to get rid of a lot of the black color spaces and outline that you dont need
        self.rect = self.image.get_rect()   #gets the borders
        self.radius = 20    #this is for making improved collisions
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius) YOU CAN USE THESE LINES TO TEST THE CIRCLE BOUNDS OF AN OBJECT
        self.rect.centerx = width / 2   #positioning
        self.rect.bottom = height - 10  #positioning
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
        bullet = Bullet(self.rect.centerx, self.rect.top)   #this creates the bullet object with a certain position as parameters
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

class Mob(pygame.sprite.Sprite):   #this will be the class for the sprite of the mobs
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius) YOU CAN USE THESE LINES TO TEST THE CIRCLE BOUNDS OF AN OBJECT
        self.rect.x = random.randrange(0, width - self.rect.width)  #you can choose to leave the 0 out because python will assume its the range to the end
        self.rect.y = random.randrange(-150, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0    #THE ROCK STARTS OFF AS NOT ROTATING
        self.rot_speed = random.randrange(-8, 8)   #RANDOM NUMBER THAT WILL DETERMINE HOW FAST THE SPRITE IS ROTATING
        self.last_update = pygame.time.get_ticks()  #GET HOW MANY EVER TICKS IT HAS BEEN SINCE THE GAME STARTED

    #this whole rotate thing is a part of the sprite animation section, rotating the meteors whenever they fall
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50: #this prevents the meteors from rotating every second, makes it more realistic
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()   #make sure to call this in order to rotate the meteors
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
        self.image.set_colorkey(black)  #gets rid of the black background
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10   #this is the speed in which the bullet goes up
    
    def update(self):   
        self.rect.y += self.speedy
        if self.rect.bottom < 0:    #this is if the bullet flies off the screen then we kill it
            self.kill()


#load all game graphics (main part for part 7)
background = pygame.image.load(path.join(img_dir, "spacebg.png")).convert()
background_rect = background.get_rect() #LOADS BACKGROUND IMAGE
player_img = pygame.image.load(path.join(img_dir, "playerShip1_red.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserBlue16.png")).convert()

#in order to randomize the different types of meteors that come in, creating a list and running a loop through it will allow you to randomly select images
meteor_images = []
meteor_list = ["meteorBrown_big1.png", "meteorBrown_big2.png", "meteorBrown_big4.png", "meteorBrown_med1.png", 
               "meteorBrown_med3.png", "meteorBrown_small1.png", "meteorBrown_tiny1.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

#Load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "pew.wav")) #shooting sound
pygame.mixer.Sound.set_volume(shoot_sound, 0.3) #adjusting the volume of the sound
expl_sounds = []    #create an empty list of sounds
for snd in ["expl3.wav", "expl6.wav"]:  #taking this list of sound effects, and randomly choosing one.
    explosion_effect = pygame.mixer.Sound(path.join(snd_dir, snd))
    pygame.mixer.Sound.set_volume(explosion_effect, 0.3)
    expl_sounds.append(explosion_effect)
pygame.mixer.music.load(path.join(snd_dir, "tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.set_volume(0.4)

all_sprites = pygame.sprite.Group() #this allows us to call a group of sprites at the same time
mobs = pygame.sprite.Group()    #this will come in handy when we want to see if they collide with something
bullets = pygame.sprite.Group() #this allows us to add the bullets a part of a bullets group
player = Player()
all_sprites.add(player)
for i in range (8): #generates 8 different mobs
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

score = 0   #INITIALIZING THE SCORE BEFORE THE GAME LOOP STARTS
pygame.mixer.music.play(loops = -1) #looping the song that plays
#game loop
running = True
while running:
    clock.tick(fps)     #this solves lag

    # 1.process input(events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #check for closing the window
            running = False
        elif event.type == pygame.KEYDOWN:  #if the player decides to shoot, then check if it is the space key
            if event.key == pygame.K_SPACE: #if space key is pressed, then the player will shoot
                player.shoot()

    # 2.update
    all_sprites.update()
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)    #check to see if a bullet hits the mobs
    for hit in hits:    #if you call mobs, they will always come back
        random.choice(expl_sounds).play()
        score += 50 - hit.radius  #THIS ADDS TO THE SCORE DEPENDING ON THE SIZE OF THE METEOR
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
    draw_text(screen, str(score), 18, width / 2, 10)    #putting this after the sprites means that it will appear over the meteors
    pygame.display.flip()   #always do this last, draw everything and then flip the display


pygame.quit()