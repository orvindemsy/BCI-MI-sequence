'''
UPDATED VERSION OF SEQ3, draft
Created by: Orvin Demsy
Assignment for on BCI motor imagery sequence
Due Date: 16-20 December 2019

Task:
- Add UDP communication protocol so that Program.cs (C# file) can read sent message
- Add input box for session no. and run no.
- Message has to comply with the requirement stated below

Message requirement:
received_data = [T/O] + [Su] + [S] + [R] + [D] + [L] + [t]
                  0      1,2    3     4     5     6     7
[T/R/O/F]: Training (Relax) / Online Test (Feedback)
[Su]: Number of subject 00, 01, 02, ..., 99
[S]:  Number of session 0, 1, ..., 9
[R]:  Number of run 0, 1, ..., 9
[D]:  Duration of recording in seconds 0, 1, ..., 9
[L]:  Label of task 0, 1, 2
[t]:  Number of trial during a run 0, 1, ..., 9

* For now 'T/R/O/F', 'L' and 't' can be any character and are predetermined (dummy)
'''

import pygame as pg
from colors import *
import random
import pggraph
import dropdownmode as ddl
import dropdowndir as ddr
import subprocess
import socket

# Define port for UDP connection
UDP_IP = "127.0.0.1"  # IP address
UDP_PORT = 1010  # port

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
        self.text2UDP = ''

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
                    self.text2UDP = '' + self.text
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT2.render(self.text, True, self.color)

        return self.text2UDP

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.rect.w, self.txt_surface.get_width()+10)
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

    # Bar percentage corresponds to MI performance
    if hv_id == 1 or hv_id == 2:
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

        # idx is the index of array of direction 1, 2 or 3, 4
        elif s[1] < count_time(t0) <= e[1]:
            arrow(list, screen, red, idx)


        elif s[2] < count_time(t0) <= e[2]:
            screen.fill(black)
            text_disp(str(n[n_idx]), screen, x_n, y_n)

        elif s[3] < count_time(t0) <= e[3]:
            text_disp("Evaluation", screen, 500, 20)
            text_disp(str(n[n_idx]), screen, x_n, y_n)
            if hv_id == 1 or hv_id == 2:
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
    input_subno = InputBox(230, 80, 80, 30)
    input_noses = InputBox(230, 120, 80, 30)
    input_norun = InputBox(230, 160, 80, 30)
    button_run = Button((255, 100, 100), 80, 230, 180, 50, "Run")
    button_trn = Button((255, 100, 100), 360, 230, 180, 50, "Train")
    button_udp = Button((255, 100, 100), 360, 110, 180, 50, "Send UDP")

    # Dropdown list instatiation
    dd_mode = ddl.DropDown(80, 320, 180, 50)
    dd_dir = ddr.DropDown(360, 320, 180, 50)

    # Variable to carry message to be sent through UDP
    message = ''

    # Run DataRec.exe
    # os.system(r'D:\TohokuUniversity\BCI-task\BCI-tools\gUSBamp\DataRec\DataRec\bin\Debug\DataRec')
    # subprocess.call([r"D:\TohokuUniversity\BCI-task\BCI-tools\gUSBamp\DataRec\DataRec\bin\Debug\DataRec.exe"])
    # subprocess.run([r"D:\TohokuUniversity\BCI-task\BCI-tools\gUSBamp\DataRec\DataRec\bin\Debug\DataRec.exe"])
    # This console app is using .NET Core
    # subprocess.run(r'D:\TohokuUniversity\C#-Test\simpleText\simpleText\bin\Debug\netcoreapp3.1\simpleText.exe')
    # This console app is using .NET Framework 4.7
    # os.system(r'D:\TohokuUniversity\C#-Test\simpleText-NetFramework\simpleText-NetFramework\bin\Debug\simpleText-NetFramework.exe')


    ### 27 DEC 2019 ###
    # _thread.start_new_thread(os.system(r'D:\TohokuUniversity\C#-Test\simpleText\simpleText\bin\Debug\netcoreapp3.1\simpleText.exe'))
    # subprocess.Popen(r'D:\TohokuUniversity\C#-Test\simpleText\simpleText\bin\Debug\netcoreapp3.1\simpleText.exe', shell = False)
    # subprocess.Popen(r'D:\TohokuUniversity\BCI-task\BCI-tools\gUSBamp\DataRec\DataRec\bin\Debug\DataRec.exe',shell=False)
    # subprocess.Popen(r'D:\TohokuUniversity\BCI-task\BCI-tools\gUSBamp\DataRec\DataRec\bin\x64\Debug\DataRec.exe',shell=False)
    # print(subprocess.decode("utf-8"))

    menu = True
    while menu:
        for event in pg.event.get():
            pos = pg.mouse.get_pos()

            if event.type == pg.QUIT:
                pg.quit()
                quit()

            input_subno.handle_event(event)
            input_noses.handle_event(event)
            input_norun.handle_event(event)

            dd_mode.handle_event(event)
            dd_dir.handle_event(event)

            # Hovering generates color chane
            if event.type == pg.MOUSEMOTION:
                if button_run.isOver(pos):
                    button_run.color = (180, 180, 180)
                else:
                    button_run.color = (150, 150, 150)

            if event.type == pg.MOUSEMOTION:
                if button_trn.isOver(pos):
                    button_trn.color = (180, 180, 180)
                else:
                    button_trn.color = (150, 150, 150)

            if event.type == pg.MOUSEMOTION:
                if button_udp.isOver(pos):
                    button_udp.color = (180, 180, 180)
                else:
                    button_udp.color = (150, 150, 150)

            # Executing test or calibration
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and button_run.isOver(pos) and \
                        dd_mode.active_list1 and dd_dir.active_list1:
                    vertical_test_run()

                elif event.button == 1 and button_run.isOver(pos) and \
                        dd_mode.active_list1 and dd_dir.active_list2:
                    horizontal_test_run()

                elif event.button == 1 and button_run.isOver(pos) and \
                        dd_mode.active_list2 and dd_dir.active_list1:
                    vertical_cal_run()

                elif event.button == 1 and button_run.isOver(pos) and \
                        dd_mode.active_list2 and dd_dir.active_list1:
                    horizontal_cal_run()

                elif event.button == 1 and button_udp.isOver(pos):
                    print(message)
                    sock = socket.socket(socket.AF_INET,  # Internet
                                         socket.SOCK_DGRAM)  # UDP

                    # Sending command by UDP
                    sock.sendto(bytes(message, 'utf-8'), (UDP_IP, UDP_PORT))

        message = 'T0211' + input_subno.text2UDP + input_noses.text2UDP + input_norun.text2UDP + '1' + '1' + '9'

        screen.fill((30, 30, 30))
        text_disp("Subject No.: ", screen, 80, 80)
        text_disp("Session No.: ", screen, 80, 120)
        text_disp("Run No.      : ", screen, 80, 160)
        input_subno.draw(screen)
        input_subno.update()

        input_noses.draw(screen)
        input_noses.update()

        input_norun.draw(screen)
        input_norun.update()

        # Drop down list declaration
        dd_mode.draw()
        dd_mode.option()
        dd_dir.draw()
        dd_dir.option()

        # Button declaration
        button_run.draw(screen, 1)
        button_trn.draw(screen, 1)
        button_udp.draw(screen)


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