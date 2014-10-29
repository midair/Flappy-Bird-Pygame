import pygame, sys
from pygame.locals import *
import random
from Flappy import Flappy

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 570

class Gameplay:

    def __init__(self):

        self.obstacleArray = []
        self.goalArray = []
        self.flappy = Flappy()
        self.timeSinceObstacle = 0
        self.score = 0
        self.highScore = set_highscore(self.score)
        self.font = pygame.font.Font(None, 36)
        self.scoreText = self.font.render("Score: %d" % self.score, 1, (10,10,10))
        self.highText = self.font.render("High Score: %d" % self.highScore, 1, (10,10,10))
        self.highTextPos = self.highText.get_rect(centerx=2*SCREEN_WIDTH/5)
        self.textpos = self.scoreText.get_rect(centerx=4*SCREEN_WIDTH/5)
        self.red = random.randrange(0,255)
        self.green = random.randrange(0,255)
        self.blue = random.randrange(0,255)
        self.RANDOM_COLOR = (self.red, self.green, self.blue)
        self.RANDOM_OPP = (255-self.red,255-self.green,255-self.blue)
        self.is_game_over = False

def set_highscore(current_score):
    high_score = 0
    high_score_file = open("high_score.txt", "r")
    high_score = int(high_score_file.read())
    high_score_file.close()

    if current_score > high_score:
        high_score_file = open("high_score.txt", "w")
        high_score_file.write(str(current_score))
        high_score_file.close()

    return max(current_score, high_score)
