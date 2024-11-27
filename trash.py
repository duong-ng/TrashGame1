# Importing the pygame module
import pygame
import random
from pygame.locals import *

#Initialize pygame
pygame.init()

#create the surface
screen = pygame.display.set_mode((800,700))

#fps settings
clock = pygame.time.Clock()

#Title and icon
pygame.display.set_caption("TrashGame")
icon = pygame.image.load('recycle-bin.png')
pygame.display.set_icon(icon)

#background
bg = pygame.image.load('background.jpg')

#CONSTANT VARIABLES
color = (48, 25, 25)

#Font
font = pygame.font.SysFont('lucidaconsole', 30, True)
font1 = pygame.font.SysFont('lucidaconsole', 50, True)

#Music
music = pygame.mixer.music.load('backgroundmusic.mp3')
pygame.mixer.music.play(-1)
collectSound = pygame.mixer.Sound('collect.wav')
ratSound = pygame.mixer.Sound('rat.wav')

def update():
    pygame.display.update()

def reDraw():
    screen.blit(bg, (0,0))
    score_text = font.render("Score: " + str(score), 1, color) 
    best_score_text = font.render("Record: " + str(best_score), 1, color)
    screen.blit(score_text, (50, 40))
    screen.blit(best_score_text, (50, 10))
    bin.draw(screen)
   
# build a character

PlayerImg = pygame.image.load('trash-can.png')

class Player(object):
    def __init__(self, X, Y, VELOCITY, JUMP) -> None:
        self.x = X
        self.y = Y
        self.speed = 10
        self.vel = VELOCITY
        self.isJump = JUMP
        self.mass = 1
        self.hitbox = (self.x , self.y, 82, 116)
    #move character
    def move(self, controller):
        if controller[pygame.K_a] and self.x > self.vel:
            self.x -= self.vel
        if controller[pygame.K_d] and self.x <= 725:
            self.x += self.vel
        #jump
        if not (self.isJump):
            if controller[pygame.K_SPACE]:
                self.isJump = True
        if self.isJump :
            if self.speed >= -10:
                neg = 1
                if self.speed < 0:
                    neg = -1
                self.y -= (self.speed**2) * self.mass * (0.5)* neg
                self.speed -= 1
            else:
                self.isJump = False
                self.speed = 10
    #draw the character
    def draw(self, screen):
        pygame.time.delay(10)
        screen.blit(PlayerImg,(self.x , self.y))
        self.hitbox = (self.x , self.y, 82, 116)
        #pygame.draw.rect(screen,(255,0,0), self.hitbox, 2)

#characters variables
bin = Player(270, 500,5,  False)


#missile on !!!

MissileImg = pygame.image.load('missile.png')
MissileImg = pygame.transform.rotate(MissileImg, -45)

class Missile(object):
    def __init__(self, X, Y, VELOCITY):
        self.x = X
        self.y = Y
        self.vel = VELOCITY
    def drawMissile(self, screen):
        pygame.time.delay(1)            
        screen.blit(MissileImg,(self.x , self.y))

missiles = []
def MissileOn():
    #shooting stuffs lmao
    for ms in missiles:
        if ms.x < 800:
            ms.x += ms.vel
        else:
            missiles.pop(missiles.index(ms))
        ms.drawMissile(screen)    
    if keys[pygame.K_f]: 
        if len(missiles) < 1:
            ms = Missile(bin.x + 10, bin.y, 10)
            missiles.append(ms)


# Create the enemies (rats)

RatImg =  pygame.image.load('rat.png')
RatImg = pygame.transform.flip(RatImg, True, False)

class Rat(object):
    def __init__(self, X, Y, SPEED):
        self.x = X
        self.y = Y
        self.speed = SPEED
        self.hitbox = (self.x, self.y, 30, 40)
    def move(self):
        self.x -= self.speed
    def draw(self, screen): 
        pygame.time.delay(2)
        screen.blit(RatImg, (self.x, self.y))
        self.hitbox = (self.x, self.y, 30, 40)
        #pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)
        
enemies = []
touch = False

def ratAttack():
    for enemy in enemies:
        if enemy.x > 0 and enemy.x <= 800:
            enemy.move()
            if isCollision(bin.hitbox, enemy.hitbox):
                enemies.pop(enemies.index(enemy))
                return True 
        else:
            enemies.pop(enemies.index(enemy))
        enemy.draw(screen)
    enemy = Rat(800, 580, 4)
    if len(enemies) < 1:
        ratSound.play()
        enemies.append(enemy)

    
# Create the falling stuffs
stuffs = ['apple.png', 'fish-bone.png', 'banana-peel.png']

class Leftover(object):
    def __init__(self, X, Y, SPEED, IMAGE):
        self.x = X
        self.y = Y
        self.speed = SPEED
        self.hitbox = (self.x, self.y, 50, 50)
        self.Img = IMAGE
    def move(self):
        self.y += self.speed
    def draw(self, screen):
        screen.blit(self.Img, (self.x, self.y))
        self.hitbox = (self.x, self.y, 50, 50)
        #pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)
        
leftover = []

#falling effects
def leftover_fall():
    for piece in leftover:
        if piece.y <= 800 and piece.y >= 0:
            piece.move()
            if isCollision(bin.hitbox, piece.hitbox):
                leftover.pop(leftover.index(piece))
                collectSound.play()
                return True
        else:
            leftover.pop(leftover.index(piece))
        piece.draw(screen)
    if len(leftover) < 5:
        leftoverImg = pygame.image.load(random.choice(stuffs))
        piece = Leftover(random.randint(0, 750), random.randint(0, 10), random.randint(2, 5), leftoverImg)
        leftover.append(piece)


#Check if collision appears

def isCollision(hitbox1, hitbox2):
    rect1 = Rect(hitbox1)
    rect2 = Rect(hitbox2)
    return pygame.Rect.colliderect(rect1, rect2)



#if the player touch the rat
def stopGameplay():
    pygame.mixer.music.stop()
    screen.fill((0,0,0))
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    play_again_text = font.render("Press f to play again", True, (255,0,0))
    screen.blit(game_over_text, (300, 300))
    screen.blit(play_again_text, (200, 400))
#loop status
running = True
game_over = False


#SCORE 
score = 0
best_score = 0


#loop 
while running:
    pygame.time.delay(2)
    clock.tick(400)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if game_over and keys[pygame.K_f]:
        score = 0
        game_over = False
        bin = Player(270, 500,5,  False)
        pygame.mixer.music.play(-1)
    if not (game_over):
        bin.move(keys)
        reDraw()
        touch = ratAttack()
        get_point = leftover_fall()
        if get_point:
            score += 1
            best_score = max(score, best_score)
        if touch:
            while len(enemies) > 1:
                enemies.pop(1)
            while len(leftover) > 1:
                leftover.pop(1)
            game_over = True
    else :
        stopGameplay()
    #MissileOn()
    update()
    
pygame.quit()