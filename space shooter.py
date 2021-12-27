#hi
import pygame
# imported operating system so that we can get files from the device into the code 
import os
# it will initialize the pygame font library
pygame.font.init()
# this initializes the pygame music library
pygame.mixer.init()

#lines 10&11 are to give the dimensions of the window
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#to change the name of the display window
pygame.display.set_caption("Space Shooters")

# in python, colours are characterized by numbers 0 - 255 known as rgb
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# // makes sure the output is an integer not a floating point
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# to assign sound to an action
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# because of the while loop, the white is drawing on the screen multiple times per second which is dtermined by 
# the user's processing speed so some users may have the game slower than others. To prevent this, we make a 
# a standard base speed for all users i.e. frames per seconds
FPS = 60
VELOCITY = 7
BULLET_VEL = 10
MAX_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# this is to create a new event. the plus number is needed if it is more than one
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('spaceship_yellow.png'))
# pygame.transform.scale is to resize an object into desired (width, height)
# pygame.transform.rotate is to rotate an image to desired degree
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    # you always put 1 when doing text
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    #you use WIN.blit when you want to draw a surface onto the screen
    # for pygame, the origin (0,0) is at the top left corner. Increasing the value of x, will draw the
    # object downwards and increasing the value of x will draw the image to the right
    # the red/yellow.x and red/yellow.y is corresponded to the coordinates in main function
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)


    pygame.display.update()

# the function is to take in the keys_pressed list and the yellow character
def yellow_handle_movement(keys_pressed, yellow):
    # the and portion is so that if the difference between x coordinate and the velocity is greater than 0 (origin),
    # it wont let the player move anymore to the left i.e. if the player wants to move out of the screen
    # it wont be allowed to
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0: #LEFT
        yellow.x -= VELOCITY
    # since the origin is at the left, when the player moves right towards the border,
    # it will still overlap cause of the origin isnt there. so x + speed + width should
    # be less than border width. i dont even understand what I'm saying
    if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x: #RIGHT
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0: #UP
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT - 15: #DOWN
        yellow.y += VELOCITY

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width: #LEFT
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT]  and red.x + VELOCITY + red.width < WIDTH: #RIGHT
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0: #UP
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT  - 15: #DOWN
        red.y += VELOCITY

# this function is going to move the bullets, handle the collision of the bullets and handle
# removing bullets when they get off the screen or collide with a character
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        # this is for the bullet to move to the right at the velocity
        bullet.x += BULLET_VEL
        # colliderect allows you to check if the rectangle representing the yellow spaceship collided
        # with the rectangle representing the bullet. this only works if both objects are rectangles
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        # this is to remove the bullet once it's off the screen
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    # this is so that the winner text will pause on the screen in milliseconds
    pygame.time.delay(10000)


#define a main function to put all of the code that handles the main game loop in pygame. e.g. redrawing the 
#window, checking for collisions, updating the score
def main():
    # defined two rectangles to represent the red and yellow spaceships respectively so that I can control
    # where they are moving to
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    # lines 156 & 159 is to control the speed of the while loop. it will make sure it will run this while loop
    # 60 times per second no matter what unless a computer cant keeep up with that speed
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            #first event you check for is if the user quit the window
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            #line 164 will quit pygame and close the window

            if event.type == pygame.KEYDOWN:
                # if the amount of bullets that we have which is defined by the length or
                # the number of bullets in this list is less than max bullets
                # player can fire another one, if not, another bullet will not fire
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    # this is to create the bullet. the bracket is to well position the bullet so 
                    # yellow.x + yellow.width is so the bullet will be placed at the edge of the
                    # spaceship to the right and the yellow.y and yellow.height/2 is to put the bullet
                    # in the middle of the spaceship (coordinates, width, height)
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    # dont forget append is to add to list which in this case is the yellow_bullets list
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            # this is to remove a health bar when a player gets hit
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        # this will print the text when the opponent player's health reaches 0
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        
        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text) # SOMEONE WON
            break

            # this tells us what keys are currently being pressed down. this also that if the key
            # stays pressed down it would still register it's being pressed
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
            
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        
    # the run = false ends the while loop
    main()
    
# these two lines will make sure that when the file is ran, it will run the main loop
if __name__ == "__main__":
    main()