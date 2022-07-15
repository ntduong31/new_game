import pygame
from pygame import mixer
import random 
import math

pygame.init()

screen = pygame.display.set_mode((500,743))
pygame.display.set_caption('Sky')
background = pygame.image.load('bg.png')
mixer.music.load('audio/background.wav')
mixer.music.play(-1)

player_img = pygame.image.load('space.png')
playerX = 210
playerY = 653
playerX_change = 0
playerY_change = 0

def player(x,y):
    screen.blit(player_img, (x,y))

enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('tattoo.png'))
    enemyX.append(random.randint(0,430))
    enemyY.append(random.randint(100,150))
    enemyX_change.append(0.2)
    enemyY_change.append(40)

def enemy(x,y,i):
    screen.blit(enemy_img[i], (x,y))

bullet_img = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 653
bulleyX_change = 0
bulletY_change = 1
bullet_state = 'ready'

def bullet_fire(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x+16,y+10))

def isCollision(x,y,z,t):
    distance = math.sqrt((z-x)**2+(t-y)**2)
    if distance < 27:
        return True
    else:
        return False

game_over = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = game_over.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (50,340))

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 24)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

running = True
while running:

    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_UP:
                playerY_change = -0.3
            if event.key == pygame.K_DOWN:
                playerY_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_sound = mixer.Sound('audio/laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    bullet_fire(bulletX, bulletY)
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
    

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 436:
        playerX = 436

    playerY += playerY_change
    if playerY <= 0:
        playerY = 0
    elif playerY >=679:
        playerY = 679

    if bulletY <= 0:
        bulletY = 653
        bullet_state = 'ready'

    if bullet_state is 'fire': 
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletY_change
    
    for i in range(num_of_enemies):

        collision1 = isCollision(enemyX[i], enemyY[i], playerX, playerY)
        if collision1:
            for j in range(num_of_enemies):
                enemyX[j] = 2000
                enemyY[j] = 2000
            game_over_text()
            break
        if enemyY[i] >= 700:
            for a in range(num_of_enemies):
                enemyX[a] = 2000
                enemyY[a] = 2000
            game_over_text()
            break
        
        if score_value == 100:
            for j in range(num_of_enemies):
                enemyX[j] = 2000
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 436:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]
    
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('audio/explosion.wav')
            explosion_sound.play()
            bulletY = playerY
            bullet_state = 'ready'
            score_value += 1
            print(score_value, end = ' ')
            enemyX[i] = random.randint(0,430)
            enemyY[i] = random.randint(100,150)

        enemy(enemyX[i],enemyY[i],i)

       
    player(playerX, playerY)
    show_score(textX, textY) 
    pygame.display.update()
    

