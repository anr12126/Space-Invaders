import pygame
import random
import math
import numpy as np
from pygame import mixer
clock = pygame.time.Clock()

# Initialize Pygame
pygame.init()
started = False
pause = False
joysticks = []

# Initialize joystick
pygame.joystick.init()
but_state = False
prev_state = False

# Colors
light_shade = (170, 170, 170)
dark_shade = (100, 100, 100)
white = (255, 255, 255)
black = (0, 0, 0)

# Background and sounds
background = pygame.image.load("images/space.jpg")
mixer.music.load("sounds/techno.mp3")

bullet_sound = mixer.Sound("sounds/laser.mp3")
collision_sound = mixer.Sound("sounds/explode.mp3")
game_over_sound = mixer.Sound("sounds/game_over.mp3")

# Score
score_var = 0
textX = 10
textY = 10

# Game over
overX = 260
overY = 260
over = False
capped = False


def read_joys():
    # Joystick
    global prev_state, but_state, playerX_change, l_joy, joy, player_speed, playerX, laserX, laserY, bullet_sound

    l_joy = joy.get_axis(0)
    if l_joy < 0.1 and l_joy > -0.1:
        if playerX_change < 0.7 and playerX_change > -0.7:
            playerX_change = 0
    else:
        playerX_change = np.interp(
            l_joy, [-1, 1], [-player_speed, player_speed])

    # Shoot button
    but_state = joy.get_button(10)
    if but_state > prev_state:
        for i in range(num_lasers):
            if laser_State[i] == "ready":
                laserX[i] = playerX+16
                fire_laser(laserX[i], laserY[i], i)
                bullet_sound.play()
                break
    prev_state = but_state


def draw_text(words, size, color, x, y):
    new_font = pygame.font.Font("fonts/QuirkyRobot.ttf", size)
    render = new_font.render(words, True, color)
    screen.blit(render, (x, y))


def reset():
    global score_var
    global playerX
    global over
    global capped
    global enemyX_speed
    global num_enemies

    score_var = 0
    enemyX_speed = 1
    for i in range(num_enemies):
        enemyX[i] = random.randint(0, 736)
        enemyY[i] = random.randint(50, 150)
        enemyX_change[i] = enemyX_speed
        explode_bool[i] = False
        last_location[i] = []
        counter[i] = 0
    playerX = 370
    over = False
    capped = False
    num_enemies = 1

    for i in range(num_lasers):
        laser_State[i] = "ready"
    mixer.music.play(-1)


def paused():
    draw_button("QUIT", 10, 10, 55, "l")
    draw_button("RESUME", -150, 10, -125, "r")
    player(player_Image, playerX, playerY)
    show_score(textX, textY)
    draw_text("PAUSED", 64, white, width/2-83, 250)
    pygame.display.update()


def game_over(x, y):
    draw_text("GAME OVER", 64, white, x, y)
    # Draw right button
    draw_button("QUIT", 10, 10, 55, "l")
    # Draw left button
    draw_button("TRY AGAIN", -150, 10, -145, "r")
    show_score(textX, textY)
    player(player_Image, playerX, playerY)
    pygame.display.update()


def start_menu():
    draw_start(-275, -100, 250)
    player(player_Image, playerX, playerY)
    if joysticks:
        draw_text("Controller Connected", 32, white, 570, 570)
    pygame.display.update()


def game_end():
    global over
    for j in range(num_enemies):
        enemyY[j] = 2000
        draw_enemy(enemy_Image[j], enemyX[j], enemyY[j])
    mixer.music.pause()
    game_over_sound.play()
    over = True


def show_score(textX, textY):
    draw_text("Score: " + str(score_var), 64, (255, 255, 255), textX, textY)
    draw_text("Pause = P", 32, white, textX, 570)

    if joysticks:
        draw_text("Controller Connected", 32, white, 570, 570)


# Create the screen
screen = pygame.display.set_mode((800, 600))
width = screen.get_width()
height = screen.get_height()

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("images/spaceship.png")
pygame.display.set_icon(icon)

# Player
player_Image = pygame.image.load("images/battleship.png")
player_speed = 5
playerX = 370
playerY = 480
playerX_change = 0


def player(pic, x, y):
    screen.blit(pic, (x, y))


def update_player_position():
    global playerX, playerX_change
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


# draw_enemy
enemy_Image = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
explode_bool = []
last_location = []
counter = []

num_enemies = 1
enemyX_speed = 1
explode_image = pygame.image.load("images/blast.png")
alien_image = pygame.image.load("images/alien.png")

for i in range(num_enemies):
    enemy_Image.append(alien_image)
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(enemyX_speed)
    enemyY_change.append(40)
    explode_bool.append(False)
    last_location.append([])
    counter.append(0)


def draw_enemy(pic, x, y):
    screen.blit(pic, (x, y))


def update_enemy_positions():
    for i in range(num_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0 or enemyX[i] >= 736:
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += 40


# Laser
laser_Image = []
laserX = []
laserY = []
laserY_change = []
laser_State = []

num_lasers = 3

for i in range(num_lasers):
    laser_Image.append(pygame.image.load("images/laser.png"))
    laserX.append(playerX+16)
    laserY.append(playerY)
    laserY_change.append(8)
    laser_State.append("ready")


def fire_laser(x, y, i):
    global laser_State
    laser_State[i] = "fire"
    screen.blit(laser_Image[i], (x, y))


collision_range = 27


def isCollision(enemyX, enemyY, laserX, laserY):
    distance = math.sqrt((enemyX-laserX)**2+(enemyY-laserY)**2)
    if distance < collision_range:
        return True
    else:
        return False

# Draw text boxes


def draw_button(text, x, y, off, dir):
    global screen
    if dir == "l":
        shift = -5
    else:
        shift = 5

    x_pos = width/2+x
    y_pos = height/2+y
    x_text = width/2+off
    y_text = height/2+20

    # Check mouse position
    if x_pos <= mouse[0] <= x_pos+140 and y_pos <= mouse[1] <= y_pos+40:
        # Display highlighted button
        pygame.draw.rect(screen, dark_shade, [
            x_pos+shift, y_pos-5, 140, 40], 0, 50)
        pygame.draw.rect(screen, light_shade, [
            x_pos, y_pos, 140, 40], 0, 50)
        draw_text(text, 32, black, x_text, y_text)
    else:
        # Display unhighlighted button
        pygame.draw.rect(screen, light_shade, [
            x_pos+shift, y_pos-5, 140, 40], 0, 50)
        pygame.draw.rect(screen, dark_shade, [
            x_pos, y_pos, 140, 40], 0, 50)
        draw_text(text, 32, white, x_text, y_text)


def draw_start(x, y, size):
    x_text = width/2+x
    y_text = height/2+y
    if x_text <= mouse[0] <= x_text+580 and y_text <= mouse[1] <= y_text+150:
        draw_text("START", size, light_shade, x_text, y_text)
    else:
        draw_text("START", size, white, x_text, y_text)


# Draw player and background
screen.blit(background, (-100, -75))
player(player_Image, playerX, playerY)
pygame.display.update()


# Game loop
running = True
while running:
    # Set framerate
    clock.tick(120)

    # Get mouse input and draw background
    mouse = pygame.mouse.get_pos()
    screen.blit(background, (-100, -75))

    # Loop through events
    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            running = False

        # Create joystick when connected
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks.append(joy)
            draw_text("Connected", 32, white, 50, 50)

        # Joystick disconnected
        if event.type == pygame.JOYDEVICEREMOVED:
            joysticks.clear()

        # Check keyboard keystokes
        if event.type == pygame.KEYDOWN:

            # Move left
            if event.key == pygame.K_LEFT:
                playerX_change = -player_speed

            # Move right
            if event.key == pygame.K_RIGHT:
                playerX_change = player_speed

            # Shoot laser
            if event.key == pygame.K_SPACE:

                # Check for available laser
                for i in range(num_lasers):
                    if laser_State[i] == "ready":
                        laserX[i] = playerX+16
                        fire_laser(laserX[i], laserY[i], i)
                        bullet_sound.play()
                        break

            # Debug quit game
            if event.key == pygame.K_q:
                game_end()

            # Pause menu
            if event.key == pygame.K_p:
                mixer.music.pause()
                pause = not pause

        # Stop moving on upward keystroke
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

        # Mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check end screen buttons
            if over is True:
                # Quit game
                if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
                    running = False

                # Try again
                if width/2-10 >= mouse[0] >= width/2-150 and height/2+10 <= mouse[1] <= height/2+50:
                    reset()

            # Pause menu
            if pause is True:
                # Quit game
                if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40:
                    running = False

                # Resume
                if width/2-10 >= mouse[0] >= width/2-150 and height/2+10 <= mouse[1] <= height/2+50:
                    pause = False
                    mixer.music.play(-1)

            # Start Menu
            if started is not True:
                # Start
                if width/2-275 <= mouse[0] <= width/2-275+580 and height/2-100 <= mouse[1] <= height/2-100+150:
                    started = True
                    mixer.music.play(-1)

    # Pause loop
    if pause:
        paused()
        continue

    elif not started:
        start_menu()
        continue

    # Joystick control
    elif joysticks:
        read_joys()

    # Game over
    elif over is True:
        # Draw text
        game_over(overX, overY)
        continue

    # Check boundaries
    update_enemy_positions()

    # Update enemy position
    for i in range(num_enemies):

        if enemyY[i] > 430:
            # Toggle game over
            game_end()

        # Check collision
        for j in range(num_lasers):
            if laser_State[j] == "fire":
                collision = isCollision(
                    enemyX[i]+32, enemyY[i]+32, laserX[j]+16, laserY[j])
            # Debug collision boxes
            # pygame.draw.circle(screen,(255,0,0),[enemyX[i]+32, enemyY[i]+32],collision_range/2 ,2)
            # pygame.draw.circle(screen,(255,0,0),[laserX[j]+16, laserY[j]],collision_range/2,2)

                if collision:
                    # Explode
                    explode_bool[i] = True
                    last_location[i] = [enemyX[i], enemyY[i]]

                    # Reset
                    laserY[j] = playerY
                    laser_State[j] = "ready"
                    score_var += 1
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(50, 150)
                    collision_sound.play()

        # Check explode
        if explode_bool[i] is True:
            counter[i] += 1
            screen.blit(explode_image,
                        (last_location[i][0], last_location[i][1]))
            if counter[i] >= 20:
                counter[i] = 0
                explode_bool[i] = False

        draw_enemy(enemy_Image[i], enemyX[i], enemyY[i])

    # Update laser positions
    for i in range(num_lasers):
        if laser_State[i] == "fire":
            laserY[i] -= laserY_change[i]
            fire_laser(laserX[i], laserY[i], i)

        if laserY[i] <= 0:
            laserY[i] = playerY
            laser_State[i] = "ready"

    # Difficulty adjustment
    if capped is False:
        if num_enemies > 6:
            capped = True
        elif score_var // 5 == num_enemies:
            num_enemies += 1
            enemy_Image.append(pygame.image.load("images/alien.png"))
            enemyX.append(random.randint(0, 736))
            enemyY.append(random.randint(50, 150))
            enemyX_change.append(enemyX_speed)
            enemyY_change.append(40)
            explode_bool.append(False)
            last_location.append([])
            counter.append(0)

            # Increase speed
            enemyX_speed += 0.8
            for i in range(num_enemies):
                enemyX_change[i] = enemyX_speed*np.sign(enemyX_change[i])

    # Show score and player
    update_player_position()
    show_score(textX, textY)
    player(player_Image, playerX, playerY)
    pygame.display.update()
