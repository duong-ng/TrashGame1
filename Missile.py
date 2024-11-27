import pygame

pygame.init()

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

#missile on
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