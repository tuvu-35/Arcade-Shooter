import pygame
import random
import math

from pygame import mixer

# Initialize pygame
pygame.init()

# Make a screen
screen = pygame.display.set_mode((800, 600))  # Width: 800px Height: 600px

running = True

# Set title of game
pygame.display.set_caption("Space Invader")

# Set icon of game
icon_img = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon_img)

# Set background image
background = pygame.image.load("img/background.png")

# Set background sound
mixer.music.load("audio/background.wav")
mixer.music.play(-1)  # -1 mean playing on loop

# Player
player_img = pygame.image.load('img/spaceship.png')
playerX = 370.0
playerY = 480.0
playerX_change = 0

# Enemies
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
enemy_img = pygame.image.load('img/enemy.png')

for i in range(num_of_enemies):
    X = random.randint(0, 800)
    Y = random.randint(50, 150)
    enemyX.append(X)
    enemyY.append(Y)
    enemyX_change.append(2)
    enemyY_change.append(50)

# Bullet
bullet_img = pygame.image.load("img/bullet.png")
bulletX = 0
bulletY = 480.0
bulletY_change = -4
bullet_state = "ready"

# Score
score_value = 0
score_font = pygame.font.Font("freesansbold.ttf", 32)
score_textX = 10
score_textY = 10

# Game over
game_over_font = pygame.font.Font("freesansbold.ttf", 64)

# Display game score to screen
def show_score(x, y):
    score = score_font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (int(x), int(y)))

# Display game over message
def show_game_over(x, y):
    message = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(message, (int(x), int(y)))

# Draw player onto screen given its position
def player(x, y):
    screen.blit(player_img, (int(x), int(y)))

# Draw bullet onto screen given its position
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (int(x + 16), int(y - 35)))

# Draw enemy onto screen given its position
def enemy(x, y):
    screen.blit(enemy_img, (int(x), int(y)))

# Check if two objects collided
def is_collision(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance < 32

# Make screen stays running until user pressed exit button
while running:
    '''All game logic go here'''
    # Set background color in RGB
    screen.fill((0, 0, 0))

    # Draw background image
    screen.blit(background, (0, 0))

    # Go through every event happening in game window
    for event in pygame.event.get():
        # Check if close button is pressed:
        if event.type == pygame.QUIT:
            running = False

        # Check if a keystroke is pressed
        if event.type == pygame.KEYDOWN:
            # Player goes left
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            # Player goes right
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            # Player shoots a bullet
            if event.key == pygame.K_SPACE:
                # Only fire the bullet if it's in ready state
                if bullet_state == "ready":
                    # Play bullet sound
                    bullet_sound = mixer.Sound("audio/laser.wav")
                    bullet_sound.play()

                    fire_bullet(playerX, bulletY)
                    bulletX = playerX

        # Check if a keystroke is released
        if event.type == pygame.KEYUP:
            # Player stops moving when key released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player movement
    playerX += playerX_change

    # Bound checking for player
    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY += bulletY_change

    # Bound checking for bullet
    if bulletY < 0:
        # When the bullet goes out of bound, player can start shooting again
        bullet_state = "ready"
        bulletY = 480.0

    # Enemy movement
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]

        # Bound checking for enemy
        if enemyX[i] < 0 or enemyX[i] >= 736:
            # Flip movement direction of enemy when it hits a wall
            enemyX_change[i] *= -1

            # Enemy also move down a little when it hits a wall
            enemyY[i] += enemyY_change[i]

            # Bound checking for enemy
            if enemyX[i] >= 736:
                enemyX[i] = 736
            elif enemyX[i] < 0:
                enemyX[i] = 0

        # Check if bullet hits enemy -> Increase score
        if is_collision(bulletX, bulletY, enemyX[i], enemyY[i]):
            # Play sound
            hit_sound = mixer.Sound("audio/explosion.wav")
            hit_sound.play()

            # When the bullet hits an enemy, player can start shooting again
            bullet_state = "ready"
            bulletY = 480.0

            # Update score
            score_value += 1

            # Enemy will respond to new location
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        # Check if enemy hits player -> GAME OVER
        if is_collision(playerX, playerY, enemyX[i], enemyY[i]):
            # Make all enemies disappear
            for i in range(num_of_enemies):
                enemyY[i] = 2000
            show_game_over(200, 250)
            running = False
            break

        enemy(enemyX[i], enemyY[i])

    # Load player
    player(playerX, playerY)

    # Display score
    show_score(score_textX, score_textY)

    # Update all changes to screen
    pygame.display.update()