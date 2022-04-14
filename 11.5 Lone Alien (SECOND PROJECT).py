#add collisions to the meteors

from random import random
import pygame
import random
from os import path

#setting up all the paths that will be needed for graphics and audio
img_dir = path.join(path.dirname(__file__), "img")
sound_dir = path.join(path.dirname(__file__), "snd")

#setting up constants that include dimensions as well as colors
width = 480
height = 600
fps = 60
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

#initializing the game needs all of these components
pygame.init()
pygame.mixer.init() #this will be needed in order to use audio
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Lone Alien")
clock = pygame.time.Clock()

font_name = pygame.font.match_font("comic sans ms")
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)    
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect() 
    text_rect.midtop = (x,y) 
    surface.blit(text_surface, text_rect)  

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (55, 65))
        self.image.set_colorkey(black)
        #self.image = pygame.Surface((50, 40))
        #self.image.fill(green)
        self.rect = self.image.get_rect()
        self.radius = 25
        #pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.centerx = width / 2
        self.rect.bottom = height / 2
        self.speedx = 0
        self.speedy = 0
     
    def update(self):
        #basic controls
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        self.rect.y += self.speedy

        #basic rules of movement if off screen
        if self.rect.left > width:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = width
        if self.rect.bottom < 0:
            self.rect.top = height
        if self.rect.top > height:
            self.rect.bottom = 0       

    def shoot_left(self):
            bullet = Bullet_Left(self.rect.centerx - 20, self.rect.top + 40) 
            all_sprites.add(bullet)
            bullets_left.add(bullet) 
            shoot_sound.play()

    def shoot_right(self):
            bullet = Bullet_Right(self.rect.centerx + 20, self.rect.top + 40) 
            all_sprites.add(bullet)
            bullets_right.add(bullet)
            shoot_sound.play()

class Bullet_Left(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(laser_left_img, 90)
        self.image.set_colorkey(black)
        #self.image = pygame.Surface((10, 20))
        #self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.radius = 25
        #pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = -10

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0:
            self.kill()

class Bullet_Right(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(laser_right_img, -90)
        self.image.set_colorkey(black)
        #self.image = pygame.Surface((10, 20))
        #self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.radius = 25
        #pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 10

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > width:
            self.kill()

class Mob_Left(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mobs_left_img, (55, 65))
        self.image.set_colorkey(black)
        #self.image = pygame.Surface((30, 40))
        #self.image.fill(red)
        self.rect = self.image.get_rect()
        self.radius = 25
        self.rect.x = random.randrange(-100, -40)  
        self.rect.y = random.randrange(0, height - self.rect.height)
        self.speedy = random.randrange(-3, 3)
        self.speedx = random.randrange(1, 8)

    def update(self):
        self.rect.x += self.speedx 
        self.rect.y += self.speedy  
        if self.rect.left > width or self.rect.top > height or self.rect.bottom < 0: 
            self.rect.x = random.randrange(-100, -40) 
            self.rect.y = random.randrange(0, height) 
            self.speedx = random.randrange(1, 8)

class Meteor_Top(pygame.sprite.Sprite):
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

    #THIS ADDS TO THE ANIMATION
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    def update(self):
        self.rotate()
        self.rect.x += self.speedx  
        self.rect.y += self.speedy  
        if self.rect.top > height + 20 or self.rect.left < -100 or self.rect.right > width + 100: 
            self.rect.x = random.randrange(0, width - self.rect.width)  
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Meteor_Bottom(pygame.sprite.Sprite):
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

    #THIS ADDS TO THE ANIMATION
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx  
        self.rect.y += self.speedy  
        if self.rect.bottom < 0 - 20 or self.rect.left < -100 or self.rect.right > width + 100: 
            self.rect.x = random.randrange(0, width - self.rect.width)
            self.rect.y = random.randrange(height + 10, height + 40)
            self.speedy = random.randrange(-8, -1)

class Mob_Right(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mobs_right_img, (55, 65))
        self.image.set_colorkey(black)
        #self.image = pygame.Surface((30, 40))
        #self.image.fill(red)
        self.rect = self.image.get_rect()
        self.radius = 25
        self.rect.x = random.randrange(width + 40, width + 100)  
        self.rect.y = random.randrange(0, height - self.rect.height)
        self.speedy = random.randrange(-3, 3)
        self.speedx = random.randrange(-8, -1)

    def update(self):
        self.rect.x += self.speedx  
        self.rect.y += self.speedy  
        if self.rect.right < 0 or self.rect.top > height or self.rect.bottom < 0: 
            self.rect.x = random.randrange(width + 40, width + 100)  
            self.rect.y = random.randrange(0, height - self.rect.height)
            self.speedy = random.randrange(-3, 3)


background = pygame.image.load(path.join(img_dir, "spacebg.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "proj_blue_ship.png")).convert()
mobs_left_img = pygame.image.load(path.join(img_dir, "proj_pink_ship.png")).convert()
mobs_right_img = pygame.image.load(path.join(img_dir, "proj_yellow_ship.png")).convert()
laser_left_img = pygame.image.load(path.join(img_dir, "laserBlueLeft.png")).convert()
laser_right_img = pygame.image.load(path.join(img_dir, "laserBlueRight.png")).convert()
meteor_images = []
meteor_list = ["meteorBrown_big1.png", "meteorBrown_big2.png", "meteorBrown_big4.png", "meteorBrown_med1.png", 
               "meteorBrown_med3.png", "meteorBrown_small1.png", "meteorBrown_tiny1.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

shoot_sound = pygame.mixer.Sound(path.join(sound_dir, "pew.wav"))
pygame.mixer.Sound.set_volume(shoot_sound, 0.1)
expl_sounds = []
for snd in ["expl3.wav", "expl6.wav"]:  
    explosion_effect = pygame.mixer.Sound(path.join(sound_dir, snd))
    pygame.mixer.Sound.set_volume(explosion_effect, 0.1)
    expl_sounds.append(explosion_effect)
pygame.mixer.music.load(path.join(sound_dir, "tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.set_volume(0.1)

all_sprites = pygame.sprite.Group()
mobs_left = pygame.sprite.Group()
mobs_right = pygame.sprite.Group()
meteor_top = pygame.sprite.Group()
meteor_bottom = pygame.sprite.Group()
bullets_left = pygame.sprite.Group()
bullets_right = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range (1):
    m = Mob_Left()
    all_sprites.add(m)
    mobs_left.add(m)

for i in range(1):
    m = Mob_Right()
    all_sprites.add(m)
    mobs_right.add(m)

for i in range (2):
    m = Meteor_Top()
    all_sprites.add(m)
    meteor_top.add(m)

for i in range (2):
    m = Meteor_Bottom()
    all_sprites.add(m)
    meteor_bottom.add(m)

score = 0
wave = 1
pygame.mixer.music.play(loops = -1)

#the game loop
running = True
while running:
    clock.tick(fps)
    
    #1. processing inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                player.shoot_left()
            elif event.key == pygame.K_2:
                player.shoot_right()

    #2. updates
    all_sprites.update()
    hits_left = pygame.sprite.groupcollide(mobs_left, bullets_left, True, True, pygame.sprite.collide_circle)
    for hit in hits_left:
        random.choice(expl_sounds).play()
        score += 1
        if score % 10 == 0:
            wave += 1
        m = Mob_Left()
        all_sprites.add(m)
        mobs_left.add(m)

    hits_right = pygame.sprite.groupcollide(mobs_left, bullets_right, True, True, pygame.sprite.collide_circle)
    for hit in hits_right:
        random.choice(expl_sounds).play()
        score += 1
        if score % 10 == 0:
            wave += 1
        m = Mob_Left()
        all_sprites.add(m)
        mobs_left.add(m)

    hits_left2 = pygame.sprite.groupcollide(mobs_right, bullets_left, True, True, pygame.sprite.collide_circle)
    for hit in hits_left2:
        random.choice(expl_sounds).play()
        score += 1
        if score % 10 == 0:
            wave += 1
        m = Mob_Right()
        all_sprites.add(m)
        mobs_right.add(m)

    hits_right2 = pygame.sprite.groupcollide(mobs_right, bullets_right, True, True, pygame.sprite.collide_circle)
    for hit in hits_right2:
        random.choice(expl_sounds).play()
        score += 1
        if score % 10 == 0:
            wave += 1
        m = Mob_Right()
        all_sprites.add(m)
        mobs_right.add(m)
        

    hits_from_left = pygame.sprite.spritecollide(player, mobs_left, False, pygame.sprite.collide_circle)
    if hits_from_left:
        print("hit!")
        #running = False
    
    hits_from_right = pygame.sprite.spritecollide(player, mobs_right, False, pygame.sprite.collide_circle)
    if hits_from_right:
        print("hit!")
        #running = False

    hits_from_meteor_top = pygame.sprite.spritecollide(player, meteor_top, False, pygame.sprite.collide_circle)
    if hits_from_meteor_top:
        print("hit!")
        #running = False

    hits_from_meteor_bottom = pygame.sprite.spritecollide(player, meteor_bottom, False, pygame.sprite.collide_circle)
    if hits_from_meteor_bottom:
        print("hit!")
        #running = False

    #3. drawing
    screen.fill(black)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, "wave: " + str(wave), 20, width / 2, 10)
    draw_text(screen, "score: " + str(score), 20, width / 2, 30)
    pygame.display.flip()

pygame.quit()