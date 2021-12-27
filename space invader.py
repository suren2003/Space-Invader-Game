#TO - DO 
# change end point back to playerY - 64 ie 480 - 64 ****DONE*****
# make game states 
#   0 pre game
#   1 running game ******DONE******
#   2 post game  *******DONE*******
#       in pre and post game no keyboard inputs will move player or shoot, and there will be no enemies shown
# set up pre and post game keyboard inputs where any key will start the game and use designated key press for post game
# increase enemmy speed every 5 or 10 points scored     ******DONE*******
# after every collision change the speed the kunai moves *****DONE*****
# vary the range more of the enemies spawn position (maybe 0 to 200) ********DONE*******
# add sound maybe
# clean up the code to look prettier and more organized and write notes such as fdrs and what function does better

#--test code will be space invaders--
import pygame
from pygame.display import set_caption
import random
import math

#initialize the pygame
pygame.init()

#create the screen 800 pixel width, 600 height
screen = pygame.display.set_mode((800, 600))

#title and icon
pygame.display.set_caption("Space Narutos")    #setting title
icon = pygame.image.load('naruto.png')   #setting icon
pygame.display.set_icon(icon)


#game state
game_state = 1
# 0 is pregame state
# 1 is play state
# 2 is after game state
#background creation
background = pygame.image.load('background.png')

#player image creation
playerImg = pygame.image.load('naruto.png')
playerX = 372
playerY = 480
player_changeX = 0         #rate of change of X
player_changeY = 0

#enemy image creation
#list of enemies
numOfEnemies = 6
enemyImg = []
enemyX = []
enemyY = []
enemy_changeX = []         #rate of change of X
enemy_changeY = 10
for i in range(0, numOfEnemies):
    enemyImg += [pygame.image.load('ninja.png')]
    enemyX += [random.randint(1,735) ]     #random start location, goes from 1 - 735 so it doesnt spawn on edges
    enemyY += [random.randint(0, 175)]
    enemy_changeX += [1]        #rate of change of X

#kunai image load
kunaiImg = pygame.image.load('kunai.png')
kunaiY = playerY       #same height as naruto
kunaiX = 0
kunai_changeY = random.randint(1,10)    #kunai speed changes after each point scored
kunai_state = 'ready'      #kunai has a ready state, where its ready to shoot but not seen, and fire state where its moving

#score 
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)     #font type, size
                        #free predownloaded font
textX = 10
textY = 10

#game over text
gameOver_font = pygame.font.Font('freesansbold.ttf', 64)



#draws player and enemy image
def player(x, y):
    screen.blit(playerImg, (x, y))   #blit means draw to screen pretty much

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))   #blit means draw to screen pretty much

#moving kunai
def fire_kunai(x, y):
    global kunai_state
    kunai_state = 'fire'
    screen.blit(kunaiImg, (x + 16, y + 10)) #putting kunai in centre of character

#collision detection
def isCollision(enemyX, enemyY, kunaiX, kunaiY):
    distance = math.sqrt((enemyX - kunaiX)**2 + (enemyY - kunaiY)**2)       #distance between two points function
    if distance < 27:   #if distance between both are under 27 pixel return True since they collided
        return True
    else: 
        return False

#showing score
def showScore(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

#showing gameover
def gameOver():
    over_text = gameOver_font.render('GAME OVER', True, (255, 255, 255))
    next_step_1 = font.render('Press <SPACE> to play again', True, (255, 255, 255)) #line 1 of next step
    next_step_2 = font.render('Press <q> to play again', True, (255, 255, 255))     #line 2 of next steps
    screen.blit(over_text, (200, 250))
    screen.blit(next_step_1, (175, 350))
    screen.blit(next_step_2, (220, 400))


#game loop
running = True
#for difficulty change
changed = 0 #since user can be on same score for a while the speed would keep changing at this point
        #so changed will track if speed has been changed for current score interval
while running:
    #filled with RGB
    screen.fill((0, 0, 0))    #setting display background colour
    screen.blit(background, (-150, 0))     #drawing background

    
#==============================GAME STATE 1: PLAY STATE==================================      
    if game_state == 1:
        #checking thru events
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:   #if current event is quit we quit, close button is quit
                running = False
            #if keystoke is pressed, check if its left or right arrow
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: #press of 'a' key
                    player_changeX = -6
                if event.key == pygame.K_d: #'d' key
                    player_changeX = 6
                if event.key == pygame.K_SPACE:
                    if kunai_state == 'ready':
                        kunaiX = playerX
                        fire_kunai(kunaiX, kunaiY)
            if event.type == pygame.KEYUP:
                player_changeX = 0
        
        #checking if game is over
        for i in range(numOfEnemies):
            if enemyY[i] >= playerY - 50:
                game_state = 2
                break
                
        playerX += player_changeX 
        

        #boundaries for spaceship
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736
        
        #enemy movement
        for i in range(numOfEnemies):
            enemyX[i] += enemy_changeX[i]
            if enemyX[i] <= 0 or enemyX[i] >= 736:
                enemy_changeX[i] *= -1
                enemyY[i] += enemy_changeY

        #kunai movement
        #if state is fire, continually redraw moving kunai thru the while loop, state can only become fire is spacebar is pressed
        if kunai_state == 'fire':
            fire_kunai(kunaiX, kunaiY)
            kunaiY -= kunai_changeY
        if kunaiY <= 0:     #can only fire second kunai after former has reached top of screen
            kunai_state = 'ready'
            kunaiY = playerY
            
        #collision check
        for i in range(numOfEnemies):
            if isCollision(enemyX[i], enemyY[i], kunaiX, kunaiY):
                kunai_state = 'ready'
                kunaiY = playerY            #resetting the kunai to be shot again
                score_value += 1
                enemyX[i] = random.randint(1,735)      #respawning in random location
                enemyY[i] =random.randint(50, 150)
                kunai_changeY = random.randint(1,10)

        #difficulty increaser every 10 points scored, by multiplying current speed by 1.5
        #since 0 % 10 gives 0, checking to make sure score is not 0 
        if score_value > 0 and score_value % 10 == 0 and changed == 0:
            changed = 1
            for i in range(numOfEnemies):
                enemy_changeX[i] *= 1.5
        elif score_value % 10 != 0 and changed == 1:
            changed = 0
            
        player(playerX, playerY)            #latest call to display is what is shown most up front
                                #if screen.fill is infront, player wont be seen 
        for i in range(numOfEnemies):
            enemy(enemyX[i], enemyY[i], i)


#=========================GAME STATE 2: POST GAME STATE=============================
    if game_state == 2:
        gameOver()
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:   #if current event is quit we quit, close button is quit
                running = False
            #if keystoke is pressed, check if its left or right arrow
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: #press of 'a' key
                    running = False
                if event.key == pygame.K_SPACE:
                    game_state = 1      #if user press space, they play again, so going back to play state
                    for j in range(numOfEnemies):
                        enemyX[j] = random.randint(1,735)   #moving enemies to a different location
                        enemyY[j] = random.randint(50, 150) 
                        enemy_changeX[j] = 1    
                    score_value = 0
    #making invaders move faster as score increases

    showScore(textX, textY)
    pygame.display.update()     #updating the display



