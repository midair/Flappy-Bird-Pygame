import pygame, sys
from pygame.locals import *
import random


# Need to create class for these global varables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 570
pygame.init()
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 60.0 # frames per second setting
fpsClock = pygame.time.Clock()
# set up the colors
red = random.randrange(0,255)
green = random.randrange(0,255)
blue = random.randrange(0,255)
RANDOM_COLOR = (red, green, blue)
RANDOM_OPP = (255-red,255-green,255-blue)
is_game_over = False

DISPLAYSURF.fill(RANDOM_COLOR)
pygame.display.set_caption('Flappy Bird!')

obstacleArray = []
goalArray = []


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


class Flappy:
    def __init__(self):
        self.img = pygame.transform.scale(pygame.image.load('blackball.png'), (50,50))
        self.bounding_rect = pygame.Rect(10,100, 50, 50)
        self.velocity = (0.0,0.0)
        self.position = (10.0,100.0)
        self.acceleration = (0.0, 800.0)

    def updatePosition(self,delta):
        self.velocity = (self.velocity[0]+self.acceleration[0]*delta, self.velocity[1]+self.acceleration[1]*delta)
        self.velocity = (self.velocity[0], clamp(self.velocity[1],-250,500))
        self.position = (self.position[0]+self.velocity[0]*delta, self.position[1]+self.velocity[1]*delta)
        self.bounding_rect = pygame.Rect(self.position[0],self.position[1], 50, 50)

    def applyImpulse(self):
        impulse = -350
        self.velocity = (self.velocity[0], impulse)

class Obstacle(pygame.Rect):
    def __init__(self):
        super(self.__class__, self).__init__(400 ,random.randrange(200,500), 50, 400)


def collision(rect_a, rect_b):
    separate = rect_a.right < rect_b.left or rect_a.left > rect_b.right or rect_a.top > rect_b.bottom or rect_a.bottom < rect_b.top
    return not separate

def makeNewObstacle():
    obs1 = Obstacle()
    pygame.draw.rect(DISPLAYSURF, RANDOM_OPP, obs1)
    distBtwnObst = random.randrange(125,180)
    topObs = pygame.Rect(400, obs1.top-400-distBtwnObst, 50, 400)
    goal = pygame.Rect(405, 0, 40, 1000)
    pygame.draw.rect(DISPLAYSURF, RANDOM_OPP, topObs)
    obstacleArray.append(obs1)
    obstacleArray.append(topObs)
    goalArray.append(goal)

def game_over():
    global is_game_over
    is_game_over = True
    set_highscore(score)
    restartFont = pygame.font.Font(None, 60)
    restarttext = restartFont.render("Restart?", 1, (10,10,10))
    restarttextpos = (SCREEN_WIDTH/2-50, SCREEN_HEIGHT/2)
    DISPLAYSURF.fill(RANDOM_COLOR)
    DISPLAYSURF.blit(restarttext, restarttextpos)


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


flappy = Flappy()
timeSinceObstacle = 0
score = 0
highScore = set_highscore(score)
font = pygame.font.Font(None, 36)
scoreText = font.render("Score: %d" % score, 1, (10,10,10))
highText = font.render("High Score: %d" % highScore, 1, (10,10,10))
highTextPos = highText.get_rect(centerx=2*SCREEN_WIDTH/5)
textpos = scoreText.get_rect(centerx=4*SCREEN_WIDTH/5)
red = random.randrange(0,255)
green = random.randrange(0,255)
blue = random.randrange(0,255)
RANDOM_COLOR = (red, green, blue)
RANDOM_OPP = (255-red,255-green,255-blue)
is_game_over = False

def restart():
    global obstacleArray, goalArray, flappy, score, scoreText, highText, textpos, highTextPos, timeSinceObstacle, RANDOM_COLOR, RANDOM_OPP, is_game_over
    obstacleArray = []
    goalArray = []
    flappy = Flappy()
    makeNewObstacle()
    timeSinceObstacle = 0
    score = 0
    highScore = set_highscore(score)
    font = pygame.font.Font(None, 36)
    scoreText = font.render("Score: %d" % score, 1, (10,10,10))
    highText = font.render("High Score: %d" % highScore, 1, (10,10,10))
    highTextPos = highText.get_rect(centerx=2*SCREEN_WIDTH/5)
    textpos = scoreText.get_rect(centerx=4*SCREEN_WIDTH/5)
    red = random.randrange(0,255)
    green = random.randrange(0,255)
    blue = random.randrange(0,255)
    RANDOM_COLOR = (red, green, blue)
    RANDOM_OPP = (255-red,255-green,255-blue)
    is_game_over = False



restart()
while True: # main game loop
    if not is_game_over:
        DISPLAYSURF.fill(RANDOM_COLOR)

        if timeSinceObstacle > 2:
            makeNewObstacle()
            timeSinceObstacle = 0

        timeSinceObstacle += 1.0/FPS

        DISPLAYSURF.blit(flappy.img, flappy.position)

        for goal in goalArray:
            if collision(flappy.bounding_rect, goal):
                score+=1
                goalArray.remove(goal)
            goal.left -= 2

        for rectangle in obstacleArray:
            if collision(flappy.bounding_rect, rectangle):
                game_over()
                break
            rectangle.left -= 2
            pygame.draw.rect(DISPLAYSURF, RANDOM_OPP, rectangle)


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                flappy.applyImpulse()

        flappy.updatePosition(1.0/FPS)

        if flappy.position[1] > 570:
            game_over()
        scoreText = font.render("Score: %d" % score, 1, (10,10,10))
        DISPLAYSURF.blit(scoreText, textpos)
        DISPLAYSURF.blit(highText, highTextPos)
    else:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                restart()

    pygame.display.update()
    fpsClock.tick(FPS)


    
    
    
