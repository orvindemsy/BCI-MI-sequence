'''
This module contains four sequences for BCI application:
- vertical sequence test
- vertical sequence calibration
- horizontal sequence test
- horizontal sequence calibration
'''
import pygame as pg
import subprocess
from colors import *
import random
import pggraph
import socket
import widget
import os

# # Define port for UDP connection
UDP_IP = "127.0.0.1"  # IP address
UDP_PORT = 1010  # port
# sock = socket.socket(socket.AF_INET,  # Internet
#                      socket.SOCK_DGRAM)  # UDP

screen = pg.display.set_mode((640, 480))
pg.display.set_caption("Just Testing")
'''
received_data = [T/O] + [Su] + [S] + [R] + [L] + [t]
          0      1,2     3      4     5     6     7
[T/R/O/F]: Training (Relax) / Online Test (Feedback)
[Su]: Number of subject 00, 01, 02, ..., 99
[S]:  Number of session 0, 1, ..., 9
[R]:  Number of run 0, 1, ..., 9
[L]:  Label of task 0, 1, 2
[t]:  Number of trial during a run 0, 1, ..., 9

The duration isn't included in the message
'''

# Set up the main.py folder dir
maindir = os.path.dirname(__file__)

def send2UDP(message, iter, dir_idx):
    # variable message contains 'Subj No.' + 'Session No.' + 'Run No.'
    #                               XX          X               X
    # Define port for UDP connection
    # UDP_IP = "127.0.0.1"  # IP address
    # UDP_PORT = 1010  # port
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    message = str(message)
    subprocess.Popen(os.path.join(maindir,'DataRec.exe'),
                     shell=False)
    sock.sendto(bytes(str(message) + 'x' + str(dir_idx) + str(iter), 'utf-8'), (UDP_IP, UDP_PORT))

def disp_timer(win, t0, x, y):
    t1 = pg.time.get_ticks()
    dt = (t1-t0)/1000
    dt_surf = widget.FONT2.render(str(dt), True, (255, 255, 255))
    win.blit(dt_surf, (x, y))
    return dt

def arrow(dir_list, screen, color, idx):
    if dir_list[idx] == 1:
        pggraph.arrow_left(screen, color)
    elif dir_list[idx] == 2:
        pggraph.arrow_right(screen, color)
    if dir_list[idx] == 3:
        pggraph.arrow_down(screen, color)
    elif dir_list[idx] == 4:
        pggraph.arrow_up(screen, color)

def text_disp(text, win, x, y):
    text_surf = widget.FONT1.render(text, True, (255, 255, 255))
    win.blit(text_surf, (x, y))

def count_time(t0):
    t1 = pg.time.get_ticks()
    dt = (t1-t0)/1000
    return dt

def bar(screen, width, height, id):
    if id == 1 or id == 2:
        # Then horizontal bar
        pggraph.horizontal_bar(screen, yellow, width, height)
    elif id == 3 or id == 4:
        # Then vertical bar
        pggraph.vertical_bar(screen, yellow, width, height)

class Sequence():
    def __init__(self, win):
        self.start_time = [0, 2, 4, 6.2, 8, 10]
        self.end_time = [2, 4, 6.2, 8, 10, 12]
        self.pg_clock = pg.time.Clock()
        self.playedOnce = False
        self.dataRecOnce = False
        self.win = win
        self.message2UDP = ''
        # self.message2UDP = 'T0234'

        # List of sequence iteration
        self.n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        # Text position
        self.x_n = 610
        self.y_n = 0

    # -------------------------------------- CALIBRATION --------------------------------------- #
    def cal_sequence(self, hv_list, iter_idx):
        t0 = pg.time.get_ticks()
        run = True

        while run:
            self.win.fill(black)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # pg.display.quit()
                    pg.quit()

            text_disp(str(self.n[iter_idx]), self.win, self.x_n, self.y_n)

            if self.start_time[0] < count_time(t0) < self.end_time[0]:
                pggraph.fixation_cross(self.win, white)
                # Record starts
                while not self.dataRecOnce:
                    # print(iter_idx)
                    # print(self.message2UDP)
                    # print(hv_list[iter_idx])
                    send2UDP(self.message2UDP, iter_idx, hv_list[iter_idx])
                    self.dataRecOnce = True

                # Play beep once
                if count_time(t0) > self.start_time[1] - 0.5:
                    while not self.playedOnce:
                        beep = pg.mixer.Sound("short_beep_200ms.wav")
                        beep.play()
                        self.playedOnce = True

            elif self.start_time[1] < count_time(t0) < self.end_time[1]:
                arrow(hv_list, self.win, red, iter_idx)

            elif self.start_time[2] < count_time(t0) <= self.end_time[2]:
                pass

            elif self.start_time[3] < count_time(t0) <= self.end_time[3]:
                run = False
                self.playedOnce = False
                self.dataRecOnce = False

            disp_timer(self.win, t0, 0, 0)
            pg.display.flip()
            self.pg_clock.tick(30)


    def horizontal_cal(self):
        a = [1 for _ in range(5)]
        b = [2 for _ in range(5)]
        h_list = a + b
        random.shuffle(h_list)
        print(h_list)

        # 1 => LEFT
        # 2 => RIGHT
        for i in range(10):
            self.cal_sequence(h_list, i)


    def vertical_cal(self):
        a = [3 for _ in range(5)]
        b = [4 for _ in range(5)]
        v_list = a + b
        random.shuffle(v_list)
        print(v_list)

        # 3 => DOWN
        # 4 => UP
        for i in range(10):
            self.cal_sequence(v_list, i)

    # ------------------------------------------ TEST ------------------------------------------ #
    def test_sequence(self, hv_list, iter_idx, bar_w, bar_h, hv_id):
        # Time inisialization
        t0 = pg.time.get_ticks()

        run = True

        # Bar percentage corresponds to MI performance
        # Horizontal
        # bar_w is width of bar random number between 100-430
        if hv_id == 1 or hv_id == 2:
            score = bar_w / 430 * 100
            score = round(score, 2)

        # Vertical
        # bar_w is height of bar random number between 100-320
        else:
            score = bar_h / 320 * 100
            score = round(score, 2)


        while run:
            subprocess.Popen(
                r'D:\TohokuUniversity\BCI-task\BCI-tools\gUSBamp\DataRec\DataRec\bin\x64\Debug\DataRec.exe',
                shell=False)
            self.win.fill(black)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

            text_disp(str(self.n[iter_idx]), self.win, self.x_n, self.y_n)

            if self.start_time[0] < count_time(t0) <= self.end_time[0]:
                pggraph.fixation_cross(self.win, white)
                # Record starts
                while not self.dataRecOnce:
                    send2UDP(self.message2UDP, iter_idx, hv_list[iter_idx])
                    self.dataRecOnce = True

                # Play beep once
                if count_time(t0) > self.start_time[1] - 0.5:
                    while not self.playedOnce:
                        beep = pg.mixer.Sound('short_beep_200ms.wav')
                        beep.play()
                        self.playedOnce = True

            # idx is the index of array of direction 1, 2 or 3, 4
            elif self.start_time[1] < count_time(t0) <= self.end_time[1]:
                arrow(hv_list, self.win, red, iter_idx)

            elif self.start_time[2] < count_time(t0) <= self.end_time[2]:
                pass

            elif self.start_time[3] < count_time(t0) <= self.end_time[3]:
                text_disp("Evaluation", self.win, 500, 20)
                if hv_id == 1 or hv_id == 2:
                    text_disp(str(score) + "%", self.win, 110, 150)
                else:
                    text_disp(str(score) + "%", self.win, 200, 100)

                bar(self.win, bar_w, bar_h, hv_id)

            elif self.start_time[4] < count_time(t0) <= self.end_time[4]:
                pass

            elif self.start_time[5] < count_time(t0) <= self.end_time[5]:
                run = False
                self.playedOnce = False
                self.dataRecOnce = False

            disp_timer(self.win, t0, 0, 0)
            pg.display.flip()
            self.pg_clock.tick(30)


    def horizontal_test(self):
        a = [1 for _ in range(5)]
        b = [2 for _ in range(5)]
        h_list = a + b
        random.shuffle(h_list)
        print(h_list)

        # 1 => LEFT
        # 2 => RIGHT
        for i in range(10):
            # Random number to generate bar's width
            bar_width = random.randint(100, 430)
            self.test_sequence(h_list, i, bar_w=bar_width, bar_h=50, hv_id=1)

    def vertical_test(self):
        a = [3 for _ in range(5)]
        b = [4 for _ in range(5)]
        v_list = a + b
        random.shuffle(v_list)
        print(v_list)

        # 3 => DOWN
        # 4 => UP
        for i in range(10):
            # Random number to generate bar's length
            bar_height = random.randint(100, 320)
            self.test_sequence(v_list, i, bar_w=50, bar_h=bar_height, hv_id=3)

        # main_menu()

if __name__ == "__main__":
    seq = Sequence(screen)

    seq.horizontal_cal()
    # seq.vertical_cal()
    # seq.horizontal_test()
    # seq.vertical_test()


# CALIBRATION SEQUENCE
# CALIBRATION PHASE


# TEST SEQUENCE
# TEST PHASE
