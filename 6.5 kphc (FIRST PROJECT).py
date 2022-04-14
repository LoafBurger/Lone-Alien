import pygame
import random

width = 480
height = 600
fps = 60

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("kphc")
clock = pygame.time.Clock()

font_name = pygame.font.match_font("arial")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.bottom = height / 2
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx  #always make sure you add this after the movement
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        self.rect.y += self.speedy  #always make sure you add this after the movement
        if self.rect.right < 0:     
            self.rect.right = 0
        if self.rect.left > width:      
            self.rect.right = 0
        if self.rect.top > height:
            self.rect.bottom = 0
        if self.rect.bottom < 0:
            self.rect.top = height

    def shoot_up(self):
        bullet = Bullet_top(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullet1.add(bullet)

    def shoot_down(self):
        bullet = Bullet_bottom(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        bullet2.add(bullet)


class Mob_top(pygame.sprite.Sprite):
    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3, 3)
    
    def update(self):
        self.rect.x += self.speedx  
        self.rect.y += self.speedy  
        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 20: 
            self.rect.x = random.randrange(0, width - self.rect.width)  
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Mob_bottom(pygame.sprite.Sprite):
    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, width - self.rect.width)
        self.rect.y = random.randrange(height + 10, height + 40)
        self.speedy = random.randrange(-8, -1)
        self.speedx = random.randrange(-3, 3)   

    def update(self):
        self.rect.x += self.speedx  
        self.rect.y += self.speedy  
        if self.rect.bottom < 0 - 10 or self.rect.left < -25 or self.rect.right > width + 20: 
            self.rect.x = random.randrange(0, width - self.rect.width)
            self.rect.y = random.randrange(height + 10, height + 40)
            self.speedy = random.randrange(-8, -1)

class Bullet_top(pygame.sprite.Sprite):
    def __init__ (self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Bullet_bottom(pygame.sprite.Sprite):
    def __init__ (self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.rect.bottom = y + 8
        self.rect.centerx = x
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > height:
            self.kill()


score = 0
all_sprites = pygame.sprite.Group()
mobs_top = pygame.sprite.Group()
mobs_bottom = pygame.sprite.Group()
bullet1 = pygame.sprite.Group()
bullet2 = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range (4):
    m1 = Mob_top()
    all_sprites.add(m1)
    mobs_top.add(m1)
for i in range (4):
    m2 = Mob_bottom()
    all_sprites.add(m2)
    mobs_bottom.add(m2)
    game_over = False


running = True
while running:
    
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  #make sure that if you check key down, you only do it once.
            if event.key == pygame.K_1:
                player.shoot_up()
            elif event.key == pygame.K_2:
                player.shoot_down()


    all_sprites.update()

    hits1 = pygame.sprite.groupcollide(mobs_top, bullet1, True, True)    
    for hit in hits1:    
        score += 1
        m1 = Mob_top()
        all_sprites.add(m1)
        mobs_top.add(m1)
    hits2 = pygame.sprite.groupcollide(mobs_bottom, bullet1, True, True)    
    for hit in hits2:    
        score += 1
        m2 = Mob_bottom()
        all_sprites.add(m2)
        mobs_bottom.add(m2)


    hits11 = pygame.sprite.groupcollide(mobs_top, bullet2, True, True)    
    for hit in hits11:    
        score += 1
        m11 = Mob_top()
        all_sprites.add(m11)
        mobs_top.add(m11)
    hits22 = pygame.sprite.groupcollide(mobs_bottom, bullet2, True, True)    
    for hit in hits22:    
        score += 1
        m22 = Mob_bottom()
        all_sprites.add(m22)
        mobs_bottom.add(m22)


    hits1 = pygame.sprite.spritecollide(player, mobs_top, False)    
    if hits1:    
        running = False
    hits2 = pygame.sprite.spritecollide(player, mobs_bottom, False)    
    if hits2:   
        running = False

    screen.fill(black)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, width / 2, 10)    #if you put this at the end, it will be at the very top when it comes to display
    pygame.display.flip()

pygame.quit()

