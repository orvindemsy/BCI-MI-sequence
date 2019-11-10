'''
Created by: Orvin Demsy

Creating a sequence of crosshair, and arrow to guide user for motor-imagery BCI system
with the following specification:
Seconds		Action
0			Fixation Cross
1			Fixation Cross
2			Beep, Fixation Cross
3			Fixation Cross gone, Arrow appeared for 1250ms either left or right
4.25		Arrow gone
4.25 ~      Classification
Reference:
Motor imagery and direct brain-computer communication
'''

from colors import *
import pygame

pygame.init()
start_time = pygame.time.get_ticks()
clock = pygame.time.Clock()
FPS = 60

screen_width = 500
screen_length = 500
size = (screen_length, screen_width)

# Display screen and determine screen size
screen = pygame.display.set_mode(size)
pygame.display.set_caption("BCI Motor Imagery Sequence")

# Declare all necessary images
white_cross = pygame.image.load("pic/white_cross.png")
white_cross = pygame.transform.scale(white_cross, (300, 300))
black_cross = pygame.image.load("pic/black_cross.png")
left_arr = pygame.image.load("pic/left_arrow.png")
left_arr = pygame.transform.scale(left_arr, (300, 300))
right_arr = pygame.image.load("pic/right_arrow.png")
right_arr = pygame.transform.scale(right_arr, (300, 300))

# Position each graphic to center
white_cross_pos = white_cross.get_rect()
white_cross_pos.centerx = screen.get_rect().centerx
white_cross_pos.centery = screen.get_rect().centery

left_arr_pos = left_arr.get_rect()
left_arr_pos.centerx = screen.get_rect().centerx
left_arr_pos.centery = screen.get_rect().centery

right_arr_pos = right_arr.get_rect()
right_arr_pos.centerx = screen.get_rect().centerx
right_arr_pos.centery = screen.get_rect().centery

# checking type of text
# print(type(white_cross))
# print(type(white_cross_pos))
# print(left_arr_pos)
# print(right_arr_pos)

def message(msg, color, size, x, y):
    font = pygame.font.SysFont(None, size)
    text = font.render(msg, True, color)
    screen.blit(text, (x, y))


# sound play
beep = pygame.mixer.Sound('short_beep.wav')
playSound = True
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    seconds = (pygame.time.get_ticks() - start_time)/1000

    # text = font.render("Hello", True, black)
    if seconds <= 3:
        # if count == 1:
        screen.fill(black)
        screen.blit(white_cross, white_cross_pos)
        message(str(seconds), white, 25, 0, 0)
        count = 1
        if playSound == True and seconds >= 2:
            beep.play()
            playSound = False
        # if seconds > 2 and count == 1:

        # count += 1
        # pygame.time.wait(1000)
    elif 3 < seconds <= 4.25:
        screen.fill(black)
        screen.blit(right_arr, right_arr_pos)
        message(str(seconds), white, 25, 0, 0)
        # pygame.time.wait(3000)
    elif 4.25 < seconds < 15:
        screen.fill(black)
        message(str(seconds), white, 25, 0, 0)
        # pygame.time.wait(3000)

    clock.tick(FPS)
    # count += 1
    # screen.blit(text, (0, 0))
    pygame.display.update()
    # print(seconds)

pygame.quit()