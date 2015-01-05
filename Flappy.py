import pygame, sys
from pygame.locals import *

class Flappy:
    def __init__(self):
        self.diameter = 50 #change this value to change flappy's size
        self.img = pygame.transform.scale(pygame.image.load('flappy.png'), (self.diameter,self.diameter))
        self.bounding_rect = pygame.Rect(10,100, self.diameter, self.diameter)
        self.velocity = (0.0,0.0)
        self.position = (10.0,100.0)
        self.acceleration = (0.0, 1000.0)

    def updatePosition(self,delta):
        self.velocity = (self.velocity[0]+self.acceleration[0]*delta, self.velocity[1]+self.acceleration[1]*delta)
        self.velocity = (self.velocity[0], clamp(self.velocity[1],-350,500))
        self.position = (self.position[0]+self.velocity[0]*delta, self.position[1]+self.velocity[1]*delta)
        self.bounding_rect = pygame.Rect(self.position[0],self.position[1], self.diameter, self.diameter)

    def applyImpulse(self):
        impulse = -450
        self.velocity = (self.velocity[0], impulse)


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)
