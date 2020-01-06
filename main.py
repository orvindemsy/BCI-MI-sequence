'''
UPDATED VERSION OF SEQ3
Created by: Orvin Demsy
Assignment for on BCI motor imagery sequence
Due Date: 27 November 2019

Sequence for calibration
fixation cross -> beep -> arrow -> b.s


Sequence for test
fixation cross -> beep -> arrow -> b.s -> bar -> b.s

Each display will last for:
- Fixation 2s
- Beep 200ms
- Arrow 2s
- Black screen (b.s.) 2s
- Bar 4s

Other modification request:
- Consider dropdown menu with default mode options (calibration or test)
- Checkbox (radio?) for direction (vertical or horizontal)
- Arrow in red, bar in yellow
'''

import pygame as pg
from colors import *
import random
import pggraph
from etc import checkbox

pg.init()
# t0 = pg.time.get_ticks()
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT1 = pg.font.Font(None, 35)
FONT2 = pg.font.Font(None, 30)

# Generate screen
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

# Horizontal or vertical test
hor_test = False
ver_test = False

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
    beep = pg.mixer.Sound('short_beep_200ms.wav')
    while not playedOnce:
        beep.play()
        screen.fill((0, 255, 0))
        playedOnce = True

def arrow(dir_list, screen, color, idx):
        if dir_list[idx] == 1:
            pggraph.arrow_left(screen, color)
        elif dir_list[idx] == 2:
            pggraph.arrow_right(screen, color)
        if dir_list[idx] == 3:
            pggraph.arrow_down(screen, color)
        elif dir_list[idx] == 4:
            pggraph.arrow_up(screen, color)

def bar(screen, width, height, id):
        if id == 1 or id == 2:
            # Then horizontal bar
            pggraph.horizontal_bar(screen, yellow, width, height)
        elif id == 3 or  id == 4:
            # Then vertical bar
            pggraph.vertical_bar(screen, yellow, width, height)

# CALIBRATION SEQUENCE
def seq_cal(list, idx, n, n_idx):
    # Time inisialization
    clock = pg.time.Clock()
    t0 = pg.time.get_ticks()

    run = True

    # Start time and end time of each arrow
    s = [0, 2, 4, 6.2, 8]
    e = [2, 4, 6.2, 8, 10]

    # Declare playedOnce indicator for sound
    playedOnce = False

    x_n = 610
    y_n = 0

    while run:
        screen.fill(black)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        text_disp(str(n[n_idx]), screen, x_n, y_n)

        if s[0] < count_time(t0) <= e[0]:
            pggraph.fixation_cross(screen, white)
            if count_time(t0) > s[1] - 0.5:
                while not playedOnce:
                    beep = pg.mixer.Sound('short_beep_200ms.wav')
                    beep.play()
                    playedOnce = True


        elif s[1] < count_time(t0) <= e[1]:
            arrow(list, screen, red, idx)


        elif s[2] < count_time(t0) <= e[2]:
            screen.fill(black)
            text_disp(str(n[n_idx]), screen, x_n, y_n)

        elif s[3] < count_time(t0) <= e[3]:
            run = False

        disp_timer(screen, t0, 0, 0)
        pg.display.flip()
        clock.tick(30)

# TEST SEQUENCE
def seq_test(list, idx, n, n_idx, bar_w, bar_h, hv_id):
    # Time inisialization
    clock = pg.time.Clock()
    t0 = pg.time.get_ticks()

    run = True

    # # Define width and height for evaluation bar
    # bar_width = random.randint(100, 430)
    # bar_height = random.randint(100, 320)

    # Bar percentage corresponds to MI performance
    if id == 1 or id == 2:
        score = bar_w / 430 * 100
        score = round(score, 2)
    else:
        score = bar_h / 320 * 100
        score = round(score, 2)

    # Start time and end time of each arrow
    s = [0, 2, 4, 6, 10, 12.5]
    e = [2, 4, 6, 10, 12.5, 14]

    # Declare playedOnce indicator for sound
    playedOnce = False

    # Text position
    x_n = 610
    y_n = 0

    while run:
        screen.fill(black)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        text_disp(str(n[n_idx]), screen, x_n, y_n)

        if s[0] < count_time(t0) <= e[0]:
            pggraph.fixation_cross(screen, white)
            if count_time(t0) > s[1] - 0.5:
                while not playedOnce:
                    beep = pg.mixer.Sound('short_beep_200ms.wav')
                    beep.play()
                    playedOnce = True


        elif s[1] < count_time(t0) <= e[1]:
            arrow(list, screen, red, idx)


        elif s[2] < count_time(t0) <= e[2]:
            screen.fill(black)
            text_disp(str(n[n_idx]), screen, x_n, y_n)

        elif s[3] < count_time(t0) <= e[3]:
            text_disp("Evaluation", screen, 500, 20)
            text_disp(str(n[n_idx]), screen, x_n, y_n)
            if id == 1 or id == 2:
                text_disp(str(score) + "%", screen, 110, 150)
            else:
                text_disp(str(score) + "%", screen, 200, 100)

            bar(screen, bar_w, bar_h, hv_id)

        elif s[4] < count_time(t0) <= e[4]:
            screen.fill(black)
            text_disp(str(n[n_idx]), screen, x_n, y_n)

        elif s[5] < count_time(t0) <= e[5]:
            run = False

        disp_timer(screen, t0, 0, 0)
        pg.display.flip()
        clock.tick(30)

# SHOW BAR, id 1 => horizontal, 3 or 4 => vertical
def bar_display(w, h, id):
    # Time initialization
    clock = pg.time.Clock()
    t0 = pg.time.get_ticks()

    run = True

    # Bar percentage corresponds to MI performance
    if id == 1 or id == 2:
        score = w/430*100
        score = round(score, 2)
    else:
        score = h/320*100
        score = round(score, 2)

    # Start time and end time of each arrow
    s = [0, 4, 6]
    e = [4, 6, 7]

    while run:
        screen.fill(black)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        text_disp("Evaluation", screen, 500, 0)
        if id == 1 or id == 2:
            text_disp(str(score)+"%", screen, 110, 150)
        else:
            text_disp(str(score)+"%", screen, 200, 100)


        if s[0] < count_time(t0) <= e[0]:
            bar(screen, w, h, id)

        if s[1] < count_time(t0) <= e[1]:
            screen.fill(black)

        if s[2] < count_time(t0) <= e[2]:
            run = False

        disp_timer(screen, t0, 0, 0)
        pg.display.flip()
        clock.tick(30)

# CALIBRATION PHASE
def horizontal_cal_run():
    a = [1 for i in range(5)]
    b = [2 for i in range(5)]
    l_h = a + b
    random.shuffle(l_h)
    print(l_h)

    n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    for i in range (10):
        seq_cal(l_h, i, n, i)

    main_menu()

def vertical_cal_run():
    a = [3 for i in range(5)]
    b = [4 for i in range(5)]
    l_v = a + b
    random.shuffle(l_v)
    print(l_v)

    n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    for i in range(10):
        seq_cal(l_v, i, n, i)

    main_menu()

# TEST PHASE
def horizontal_test_run():
    a = [1 for i in range(5)]
    b = [2 for i in range(5)]
    l_h = a + b
    random.shuffle(l_h)
    print(l_h)

    n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    for i in range(10):
        # Random number to generate bar's width
        bar_width = random.randint(100, 430)
        seq_test(l_h, i, n, i, bar_w=bar_width, bar_h=50, hv_id=1)

    main_menu()

def vertical_test_run():
    a = [3 for i in range(5)]
    b = [4 for i in range(5)]
    l_v = a + b
    random.shuffle(l_v)
    print(l_v)

    n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    for i in range(10):
        # Random number to generate bar's length
        bar_height = random.randint(100, 320)
        seq_test(l_v, i, n, i, bar_w=50, bar_h=bar_height, hv_id=3)

    main_menu()

# MAIN MENU
def main_menu():
    clock = pg.time.Clock()
    # Create input box and button objects
    input_box1 = InputBox(320, 100, 140, 32)
    button1 = Button((255, 100, 100), 80, 280, 150, 50, "Test")
    button2 = Button((255, 100, 100), 80, 350, 150, 50, "Calibration")
    button3 = Button((255, 100, 100), 400, 280, 150, 50, "Vertical")
    button4 = Button((255, 100, 100), 400, 350, 150, 50, "Horizontal")

    # Checkbox instantiation
    chkbox1 = checkbox.Checkbox(screen, 80, 280, 1)
    chkbox2 = checkbox.Checkbox(screen, 80, 350, 2)

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
                if event.button == 1 and button3.isOver(pos) and chkbox2.checked:
                    vertical_cal_run()
                    menu = False

                elif event.button == 1 and button4.isOver(pos) and chkbox2.checked:
                    horizontal_cal_run()
                    menu = False

                elif event.button == 1 and button3.isOver(pos) and chkbox1.checked:
                    vertical_test_run()
                    menu = False

                elif event.button == 1 and button4.isOver(pos) and chkbox1.checked:
                    horizontal_test_run()
                    menu = False

            chkbox1.update_checkbox(event)
            chkbox2.update_checkbox(event)

        screen.fill((30, 30, 30))
        text_disp("Subject No.: ", screen, 150, 105)
        input_box1.draw(screen)
        input_box1.update()

        # Button declaration
        button1.draw(screen, 1)
        button2.draw(screen, 1)
        button3.draw(screen, 1)
        button4.draw(screen, 1)

        # Render checkbox
        chkbox1.render_checkbox()
        chkbox2.render_checkbox()

        # Checkbox instruction
        if chkbox1.checked and chkbox2.checked:
            text_disp("Unable to Choose Both Phase", screen, 150, 200)
        else:
            text_disp("Please choose Calibration or Test Phase", screen, 90, 200)

        # Update screen
        pg.display.flip()
        clock.tick(30)


def main():

    done = False

    while not done:
        main_menu()
        # horizontal_run()
        # vertical_run()

# if __name__ == '__main__':
    # print(l_h)
    # print(l_v)
main()
pg.quit()