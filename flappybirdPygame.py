import pygame, sys
from pygame.locals import *
import random
from GameplayClass import Gameplay
from GameplayClass import set_highscore

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 570
pygame.init()
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 60.0 # frames per second setting
fpsClock = pygame.time.Clock()
pygame.display.set_caption('Flappy Bird!')

gameplay = Gameplay()



class Obstacle(pygame.Rect):
    def __init__(self):
        super(self.__class__, self).__init__(400 ,random.randrange(200,500), 50, 400)

def collision(rect_a, rect_b):
    separate = rect_a.right < rect_b.left or rect_a.left > rect_b.right or rect_a.top > rect_b.bottom or rect_a.bottom < rect_b.top
    return not separate

def makeNewObstacle():
    obs1 = Obstacle()
    pygame.draw.rect(DISPLAYSURF, gameplay.RANDOM_OPP, obs1)
    distBtwnObst = random.randrange(125,180)
    topObs = pygame.Rect(400, obs1.top-400-distBtwnObst, 50, 400)
    goal = pygame.Rect(405, 0, 40, 1000)
    pygame.draw.rect(DISPLAYSURF, gameplay.RANDOM_OPP, topObs)
    gameplay.obstacleArray.append(obs1)
    gameplay.obstacleArray.append(topObs)
    gameplay.goalArray.append(goal)

def game_over():
    gameplay.is_game_over = True
    set_highscore(gameplay.score)
    restartFont = pygame.font.Font(None, 60)
    restarttext = restartFont.render("Restart?", 1, (10,10,10))
    restarttextpos = (SCREEN_WIDTH/2-50, SCREEN_HEIGHT/2)
    DISPLAYSURF.fill(gameplay.RANDOM_COLOR)
    DISPLAYSURF.blit(restarttext, restarttextpos)




def restart():
    global gameplay
    gameplay = Gameplay()
    makeNewObstacle()


restart()
while True: # main game loop
    if not gameplay.is_game_over:
        DISPLAYSURF.fill(gameplay.RANDOM_COLOR)

        if gameplay.timeSinceObstacle > 2:
            makeNewObstacle()
            gameplay.timeSinceObstacle = 0

        gameplay.timeSinceObstacle += 1.0/FPS

        DISPLAYSURF.blit(gameplay.flappy.img, gameplay.flappy.position)

        for goal in gameplay.goalArray:
            if collision(gameplay.flappy.bounding_rect, goal):
                gameplay.score+=1
                gameplay.goalArray.remove(goal)
            goal.left -= 2

        for rectangle in gameplay.obstacleArray:
            if collision(gameplay.flappy.bounding_rect, rectangle):
                game_over()
                break
            rectangle.left -= 2
            pygame.draw.rect(DISPLAYSURF, gameplay.RANDOM_OPP, rectangle)


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                gameplay.flappy.applyImpulse()

        gameplay.flappy.updatePosition(1.0/FPS)

        if gameplay.flappy.position[1] > 570:
            game_over()
        gameplay.scoreText = gameplay.font.render("Score: %d" % gameplay.score, 1, (10,10,10))
        DISPLAYSURF.blit(gameplay.scoreText, gameplay.textpos)
        DISPLAYSURF.blit(gameplay.highText, gameplay.highTextPos)
    else:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                restart()

    pygame.display.update()
    fpsClock.tick(FPS)


    
    
    
