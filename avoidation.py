import pygame
from pygame.locals import *
from sys import exit
import random
import math

class Vector:
    def __init__(self, a=0, b=0):
        if isinstance(a, Vector):
            self.x = a.x
            self.y = a.y
        elif type(a) is tuple:
            self.x = a[0]
            self.y = a[1]
        elif a == None:
            self.x = 0
            self.y = 0
        else:
            self.x = a
            self.y = b

    @classmethod
    def RandomNorm(cls, minAngle=0, maxAngle=360):
        angle = random.uniform(minAngle, maxAngle)
        x = math.sin(angle)
        y = math.cos(angle)
        return cls(x,y)

    def Angle(self):
        a = math.atan2(self.y, self.x)
        if a < 0:
            a = a + 2*math.pi
        return math.degrees(a)

    def ToTuple(self):
        return (int(self.x), int(self.y))

    def __str__(self):
        return "(%s ,%s)"%(self.x, self.y)
    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)

    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)

class GameObject:
    def __init__(self, x=0, y=0):
        self.pos = Vector(x, y)
    def Pos(self):
        return self.pos
    
class Bullet(GameObject):
    def __init__(self,pos=None, speed=None, flag=None):
        GameObject.__init__(self, pos)
        self.width = 10
        self.height = 10
        if speed != None:
            self.speed = speed
        else:
            self.speed = Vector(0,0)

    def Move(self):
        self.pos = self.pos + self.speed

class Jet(GameObject):
    def __init__(self, pos=None):
        GameObject.__init__(self, pos)
        self.width = 20
        self.height = 20

class Game:
    def __init__(self):
        self.jet = Jet((200, 200))
        self.bullets = []
        self.width = 640
        self.height = 480
        self.status = 'idle'

    # Randomly generate a bullet on the edge
    # Add this bullet in the bullet list
    def GenerateBullet(self):
        if random.randrange(0, 2) == 0:
            x = random.choice([0, self.width])
            y = self.height * random.uniform(0, 1)
        else:
            x = self.width * random.uniform(0, 1)
            y = random.choice([0, self.height])
        
        bulletPos = Vector(x, y)
        # Let the bullet point to the jet, but with +- 20 degrees of random
        distance = self.jet.Pos() - bulletPos
        angle = distance.Angle()
        speed = Vector().RandomNorm(angle-20, angle+20)
        self.bullets.append(Bullet(bulletPos, speed))
    
    def Update(self):
        for bullet in self.bullets:
            bullet.Move()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640, 480), 0, 32)
    jetImagePath = 'img/jet.png'
    bulletImagePath = 'img/bullet.png'

    jetImage = pygame.image.load(jetImagePath).convert_alpha()
    jetImage = pygame.transform.scale(jetImage, (20,20))
    bulletImage = pygame.image.load(bulletImagePath).convert_alpha()
    bulletImage = pygame.transform.scale(bulletImage, (10,10))

    clock = pygame.time.Clock()
    
    jet = Jet((200, 200))
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        if game.status == 'idle':
            pressed_keys = pygame.key.get_pressed()
            jet = game.jet
            bullets = game.bullets

            if pressed_keys[K_UP]:
                jet.pos.y -= 1
            elif pressed_keys[K_DOWN]:
                jet.pos.y += 1

            game.GenerateBullet()
            screen.fill((255,255,255))
            screen.blit(jetImage, jet.Pos().ToTuple())
            for bullet in bullets:
                screen.blit(bulletImage, bullet.Pos().ToTuple())
            game.Update()

            time_passed = clock.tick(30)
            pygame.display.update()
            print("game finish")
