'''
MODIFICATION OF SEQ1
Created by: Orvin Demsy
Assignment for on BCI motor imagery sequence
Due Date: 31 October 2019

Initial sequence:
Seconds     Action
0           Fixation Cross
1           Fixation Cross
2           Beep, Fixation Cross
3           Fixation Cross gone, Arrow appeared for 1250ms either left or right
4.25        Arrow gone
4.25 ~      Classification

Please create a display with following specification:
1. Random set of arrow

2. A sequence should have 1 cross followed by 10 arrows appearing at random order

3. At first a prompt should appear inquiring these:
    - subject number, calibration or test mode, and horizontal or vertical orientation
    - 'start' button to initiate the sequence

4. Arrows should be appearing in the orientation specified, but in a random order
    e.g.: horizontal is chosen -> 5 right 5 left or 4 left 6 right or 2 right 3 left 5 right, etc.
        vertical is chosen -> 5 up 5 down or 4 up 6 down or 2 up 3 down 5 down, etc.

5. Calibration and test are just dummy options, no need to set any algorithm for them.
'''

import time
import sys
import pygame as pg
from colors import *
import random
pg.init()
# t0 = pg.time.get_ticks()
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT1 = pg.font.Font(None, 35)
FONT2 = pg.font.Font(None, 30)

# Generating screen
w_scr = 640
h_scr = 480
size_scr = (w_scr, h_scr)
screen = pg.display.set_mode(size_scr)
pg.display.set_caption("BCI Motor Imagery Test")

# For button
color_inactive = pg.Color('lightskyblue3')
color_active = pg.Color('dodgerblue2')
color = color_inactive
active = False
text = ''

# List for picture and their positions
pic_list = []
pos_list = []

class JustText():
    def __init__(self, text=''):
        self.text = text

class Button():
    def __init__(self, color, x, y, w, h, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text

    def draw(self, win, outline = None):
        if outline:
            pg.draw.rect(win, self.color, (self.x - 2, self.y - 2, self.w + 4, self.h + 4), 0)

        pg.draw.rect(win, self.color, (self.x, self.y, self.w, self.h), 0)

        if self.text != '':
            font = pg.font.SysFont(None, 30)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (self.x + (self.w / 2 - text.get_width() / 2), self.y + (self.h / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                return True

        return False


class InputBox():
    # Input box class declaration
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT2.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT2.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

    # def draw(self, win, color, width):
    #     self.a = pg.draw.rect(win, color, (self.x, self.y, self.width, self.height), width)
    #
    # def text(self, color, win):
    #     text = 'Love'
    #     font = pg.font.SysFont(None, 30)
    #     text_surf = font.render(text, True, color)
    #     win.blit(text_surf, (self.x+5, self.y+5))
    #
    # def handle_event(self, event):
    #     if event.type == pg.MOUSEBUTTONDOWN:
    #         # If the user clicked on the input_box rect.
    #         if self.a.collidepoint(event.pos):

def disp_timer(win, t0, x, y):
    t1 = pg.time.get_ticks()
    dt = (t1-t0)/1000
    dt_surf = FONT2.render(str(dt), True, (255, 255, 255))
    win.blit(dt_surf, (x, y))
    return dt

def count_time(t0):
    t1 = pg.time.get_ticks()
    dt = (t1-t0)/1000
    return dt

def pic_disp(win, pic_name, xy):
    # var_load = pg.image.load("pic" + "\\" + pic_name)
    # var = pg.transform.scale(var_load, (200, 200))
    win.blit(pic_name, xy)

def center_pos(pic, win, list):
    pic_pos = pic.get_rect()
    pic_pos.centerx = win.get_rect().centerx
    pic_pos.centery = win.get_rect().centery
    list.append(pic_pos)

def pic_pos(pic, list, x, y):
    pic_pos = pic.get_rect()
    pic_pos.centerx = x
    pic_pos.centery = y
    list.append((x, y))

def pic_load(pic_name):
    var_load = pg.image.load("pic" + "\\" + pic_name)
    var = pg.transform.scale(var_load, (200, 200))
    return var

def text_disp(text, win, x, y):
    text_surf = FONT1.render(text, True, (255, 255, 255))
    win.blit(text_surf, (x, y))

def add_pic(list, pic):
    list.append(pic)

def play_sound():
    beep = pg.mixer.Sound('short_beep.wav')
    while not playedOnce:
        # beep.play()
        screen_fill((0, 255, 0))
        playedOnce = True

def main_menu():
    clock = pg.time.Clock()
    # Create input box and button objects
    input_box1 = InputBox(320, 100, 140, 32)
    button1 = Button((255, 100, 100), 80, 280, 150, 50, "Test")
    button2 = Button((255, 100, 100), 80, 350, 150, 50, "Calibration")
    button3 = Button((255, 100, 100), 400, 280, 150, 50, "Vertical")
    button4 = Button((255, 100, 100), 400, 350, 150, 50, "Horizontal")

    menu = True
    while menu:
        for event in pg.event.get():
            pos = pg.mouse.get_pos()

            if event.type == pg.QUIT:
                pg.quit()
                quit()

            input_box1.handle_event(event)

            if event.type == pg.MOUSEMOTION:
                if button1.isOver(pos):
                    button1.color = (100, 100, 100)
                else:
                    button1.color = (150, 150, 120)

                if button2.isOver(pos):
                    button2.color = (100, 100, 100)
                else:
                    button2.color = (150, 150, 120)

                if button3.isOver(pos):
                    button3.color = (100, 100, 100)
                else:
                    button3.color = (150, 150, 120)

                if button4.isOver(pos):
                    button4.color = (100, 100, 100)
                else:
                    button4.color = (150, 150, 120)

            if event.type == pg.MOUSEBUTTONDOWN:
                # if event.button == 1 and button1.isOver(pos):
                #     t0 = pg.time.get_ticks()
                #     menu = False
                #
                # if event.button == 1 and button2.isOver(pos):
                #     t0 = pg.time.get_ticks()
                #     menu = False

                if event.button == 1 and button3.isOver(pos):
                    vertical_seq()
                    menu = False
                    # v_seq = True

                if event.button == 1 and button4.isOver(pos):
                    horizontal_seq()
                    menu = False
                    # h_seq = True

        screen.fill((30, 30, 30))
        text_disp("Subject No.: ", screen, 150, 105)
        input_box1.draw(screen)
        input_box1.update()

        # Button declaration
        button1.draw(screen, 1)
        button2.draw(screen, 1)
        button3.draw(screen, 1)
        button4.draw(screen, 1)

        # Update screen
        pg.display.flip()
        clock.tick(30)



def horizontal_seq():
    l_h = [random.randint(1, 2) for i in range(10)]
    print(l_h)
    clock = pg.time.Clock()
    h_seq = True
    t0 = pg.time.get_ticks()

    # Declare playedOnce indicator for sound
    playedOnce = False

    # Start time and end time of each arrow
    s = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
    e = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26]
    n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    x_n = 610
    y_n = 0
    while h_seq:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        screen.fill((70, 70, 70))
        # Displaying arrows
        if s[0] < count_time(t0) <= e[0]:
            pic_disp(screen, pic_list[0], pos_list[0])

            if count_time(t0) > s[1]-1:
                while not playedOnce:
                    beep = pg.mixer.Sound('short_beep.wav')
                    beep.play()
                    playedOnce = True

        elif s[1] < count_time(t0) <= e[1]:
            text_disp(str(n[0]), screen, x_n, y_n)
            pic_disp(screen, pic_list[l_h[0]], pos_list[l_h[0]])

        elif s[2] < count_time(t0) <= e[2]:
            text_disp(str(n[1]), screen, x_n, y_n)
            pic_disp(screen, pic_list[l_h[1]], pos_list[l_h[1]])

        elif s[3] < count_time(t0) <= e[3]:
            text_disp(str(n[2]), screen, x_n, y_n)
            pic_disp(screen, pic_list[l_h[2]], pos_list[l_h[2]])

        elif s[4] < count_time(t0) <= e[4]:
            text_disp(str(n[3]), screen, x_n, y_n)
            pic_disp(screen, pic_list[l_h[3]], pos_list[l_h[3]])

        elif s[5] < count_time(t0) <= e[5]:
            text_disp(str(n[4]), screen, x_n, y_n)
            pic_disp(screen, pic_list[l_h[4]], pos_list[l_h[4]])

        elif s[6] < count_time(t0) <= e[6]:
            text_disp(str(n[5]), screen, x_n, y_n)
            pic_disp(screen, pic_list[l_h[5]], pos_list[l_h[5]])

        elif s[7] < count_time(t0) <= e[7]:
            text_disp(str(n[6]), screen, x_n, y_n)
            pic_disp(screen, pic_list[l_h[6]], pos_list[l_h[6]])

        elif s[8] < count_time(t0) <= e[8]:
            text_disp(str(n[7]), screen, x_n, y_n)
            pic_disp(screen, pic_list[l_h[7]], pos_list[l_h[7]])

        elif s[9] < count_time(t0) <= e[9]:
            text_disp(str(n[8]), screen, x_n, y_n)
            pic_disp(screen, pic_list[l_h[8]], pos_list[l_h[8]])

        elif s[10] < count_time(t0) <= e[10]:
            text_disp(str(n[9]), screen, x_n, y_n)
            pic_disp(screen, pic_list[l_h[9]], pos_list[l_h[9]])

        elif s[11] < count_time(t0) <= e[11]:
            pic_disp(screen, pic_list[5], pos_list[l_v[9]])
            # text_disp("Done", screen, 300, 600)

        elif s[12] < count_time(t0) <= e[12]:
            pg.time.wait(500)
            h_seq = False
            v_seq = False
            # menu = True
            main_menu()


        disp_timer(screen, t0, 0, 0)
        pg.display.flip()
        clock.tick(30)

def vertical_seq():
    l_v = [random.randint(3, 4) for i in range(10)]
    print(l_v)
    clock = pg.time.Clock()
    v_seq = True
    t0 = pg.time.get_ticks()

    # Declare playedOnce indicator for sound
    playedOnce = False

    print(pic_list)
    # Start time and end time of each arrow
    s = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
    e = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26]
    n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    x_n = 610
    y_n = 0
    while v_seq:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        screen.fill((70, 70, 70))

        # Displaying arrows
        if s[0] < count_time(t0) <= e[0]:
            pic_disp(screen, pic_list[0], pos_list[0])

            if count_time(t0) > s[1]-1:
                while not playedOnce:
                    beep = pg.mixer.Sound('short_beep.wav')
                    beep.play()
                    playedOnce = True

        elif s[1] < count_time(t0) <= e[1]:
            text_disp(str(n[0]), screen, x_n, y_n)
            pic_disp(screen, pic_list[l_v[0]], pos_list[l_v[0]])

        elif s[2] < count_time(t0) <= e[2]:
            text_disp(str(n[1]), screen, x_n, y_n)
            pic_disp(screen, pic_list[l_v[1]], pos_list[l_v[1]])

        elif s[3] < count_time(t0) <= e[3]:
            text_disp(str(n[2]), screen, x_n, y_n)
            pic_disp(screen, pic_list[l_v[2]], pos_list[l_v[2]])

        elif s[4] < count_time(t0) <= e[4]:
            text_disp(str(n[3]), screen, x_n, y_n)
            pic_disp(screen, pic_list[l_v[3]], pos_list[l_v[3]])

        elif s[5] < count_time(t0) <= e[5]:
            text_disp(str(n[4]), screen, x_n, y_n)
            pic_disp(screen, pic_list[l_v[4]], pos_list[l_v[4]])

        elif s[6] < count_time(t0) <= e[6]:
            text_disp(str(n[5]), screen, x_n, y_n)
            pic_disp(screen, pic_list[l_v[5]], pos_list[l_v[5]])

        elif s[7] < count_time(t0) <= e[7]:
            text_disp(str(n[6]), screen, x_n, y_n)
            pic_disp(screen, pic_list[l_v[6]], pos_list[l_v[6]])

        elif s[8] < count_time(t0) <= e[8]:
            text_disp(str(n[7]), screen, x_n, y_n)
            pic_disp(screen, pic_list[l_v[7]], pos_list[l_v[7]])

        elif s[9] < count_time(t0) <= e[9]:
            text_disp(str(n[8]), screen, x_n, y_n)
            pic_disp(screen, pic_list[l_v[8]], pos_list[l_v[8]])

        elif s[10] < count_time(t0) <= e[10]:
            text_disp(str(n[9]), screen, x_n, y_n)
            pic_disp(screen, pic_list[l_v[9]], pos_list[l_v[9]])

        elif s[11] < count_time(t0) <= e[11]:
            pic_disp(screen, pic_list[5], pos_list[l_v[9]])
            # text_disp("Done", screen, 300, 600)

        elif s[12] < count_time(t0) <= e[12]:
            pg.time.wait(500)
            # h_seq = False
            v_seq = False
            # menu = True
            main_menu()


        disp_timer(screen, t0, 0, 0)
        pg.display.flip()
        clock.tick(60)


# Random list of 1 and 2
# l_h = [random.randint(1, 2) for i in range(10)]
# Random list of 3 and 4
l_v = [random.randint(3, 4) for i in range(10)]

def main():
    # Load all pictures and their position
    add_pic(pic_list, pic_load("white_cross.png"))
    center_pos(pic_list[0], screen, pos_list)

    # Arrow in horizontal direction
    add_pic(pic_list, pic_load("left_arrow.png"))
    center_pos(pic_list[1], screen, pos_list)
    add_pic(pic_list, pic_load("right_arrow.png"))
    center_pos(pic_list[2], screen, pos_list)

    # Arrow in vertical direction
    add_pic(pic_list, pic_load("up_arrow.png"))
    center_pos(pic_list[3], screen, pos_list)
    add_pic(pic_list, pic_load("down_arrow.png"))
    center_pos(pic_list[4], screen, pos_list)

    # Add horizontal bar
    add_pic(pic_list, pic_load("blue_h_bar.png"))
    center_pos(pic_list[5], screen, pos_list)

    done = False

    while not done:
        main_menu()
        horizontal_seq()
        vertical_seq()

if __name__ == '__main__':
    # print(l_h)
    # print(l_v)
    main()
    pg.quit()