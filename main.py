import pygame
import random
from pygame import mixer

# Functions
def startpage():
    screen.blit(Game['start-bg'], (0,0))

def bird(x,y):
    screen.blit(Game['bird'], (x,y))

def gameover():
    over_text = font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200,275))
    
    mixer.Sound('assets/gameover.mp3').play()

def showScore(x, y):
    score_board = scoreFont.render(str(score), True, (0,0,0))
    screen.blit(score_board, (385,75))

pygame.init()

fpsclock = pygame.time.Clock()
fps = 32

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Flappy Bird')
# icon = pygame.image.load('')
# pygame.diplay.set_icon()

# Game Sprites
Game = {}
Game['bird'] = pygame.image.load('assets/bird.png')
Game['start-bg'] = pygame.image.load('assets/start-background.png')
Game['bg'] = pygame.image.load('assets/bg.png')
Game['up-pipe'] = pygame.transform.scale(pygame.image.load('assets/pipe.png'), (250,400))
Game['down-pipe'] = pygame.transform.rotate(Game['up-pipe'], 180)

# Variables
birdx = 100
birdy = 236
birdAcc = 40
pipex = 800
speed = 2
flapped = False
over = False
score = 0
font = pygame.font.Font('freesansbold.ttf', 64)
scoreFont = pygame.font.Font('freesansbold.ttf', 50)

upPipes = []
downPipes = []

# Background Music
mixer.music.load('assets/background.mp3')
mixer.music.play(-1)

# Game loop
running = True
start = False
num = 0

while running:
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not start and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = True

        if start and event.type == pygame.KEYDOWN and not over:
            if event.key == pygame.K_SPACE:
                birdy -= birdAcc
                mixer.Sound('assets/fly.mp3').play()                
                flapped = True

    if not start:
        startpage()        
    else:
        screen.fill((255,255,255))
        screen.blit(Game['bg'], (0,0))

        if num%100 == 0 and not over:
            downy = random.randint(-270, -80)

            downPipes.insert(len(downPipes), [pipex, downy])
            upPipes.insert(len(upPipes), [pipex, (520 + downy)])

        for i in range(len(downPipes)):
            screen.blit(Game['down-pipe'], (downPipes[i][0], downPipes[i][1]))
            screen.blit(Game['up-pipe'], (upPipes[i][0], upPipes[i][1]))

        if not flapped and num%10 == 0 and not over:
            birdy += 10
            # mixer.Sound('fall.mp3').play()            

        bird(birdx, birdy)

        # Collision Detection
        for i in range(len(downPipes)):
            upPipe =  upPipes[i][1]
            downPipe = 400 + downPipes[i][1]

            xpos = upPipes[i][0]

            if xpos+50 <= birdx and xpos+125 > birdx:
                if birdy+45 >= upPipe or birdy+20 <= downPipe:
                    gameover()
                    over = True 

            if xpos+125 < birdx:
                score = i+1

        if birdy >= 480:
            gameover()
            over = True

        flapped = False
        num += 1
        showScore(50, 50)
        
        if not over:
            for i in range(len(downPipes)):
                downPipes[i] = [downPipes[i][0]-speed, downPipes[i][1]]
                upPipes[i] = [upPipes[i][0]-speed, upPipes[i][1]]
        
    pygame.display.update()