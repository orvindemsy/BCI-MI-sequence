'''
UPDATED VERSION OF SEQ3, draft
Created by: Orvin Demsy
Assignment for on BCI motor imagery sequence
Due Date: 6 January 2019

Task:
- Organize the code neatly

Message requirement for DataRec.exe:
received_data = [T/O] + [Su] + [S] + [R] + [D] + [L] + [t]
                  0      1,2    3     4     5     6     7
[T/R/O/F]: Training (Relax) / Online Test (Feedback)
[Su]: Number of subject 00, 01, 02, ..., 99
[S]:  Number of session 0, 1, ..., 9
[R]:  Number of run 0, 1, ..., 9
[D]:  Duration of recording in seconds 0, 1, ..., 9
[L]:  Label of task 0, 1, 2
[t]:  Number of trial during a run 0, 1, ..., 9
'''

import pygame as pg
import dropdownmode as ddl
import dropdowndir as ddr
import subprocess
import socket
import widget
import sequence

# Define port for UDP connection
UDP_IP = "127.0.0.1"  # IP address
UDP_PORT = 1010  # port

pg.init()

# Generating screen
w_scr = 640
h_scr = 480
size_scr = (w_scr, h_scr)
screen = pg.display.set_mode(size_scr)
pg.display.set_caption("Classical BCI GUI")

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

# MAIN MENU
def main_menu():
    clock = pg.time.Clock()
    # Create input box and button objects
    input_subno = widget.InputBox(230, 80, 80, 30)
    input_noses = widget.InputBox(230, 120, 80, 30)
    input_norun = widget.InputBox(230, 160, 80, 30)
    button_run = widget.Button((255, 200, 100), 80, 230, 180, 50, "Run")
    button_trn = widget.Button((255, 200, 100), 360, 230, 180, 50, "Train")
    button_udp = widget.Button((255, 200, 100), 360, 110, 180, 50, "Send UDP")

    # Dropdown list instatiation
    dd_mode = ddl.DropDown(80, 320, 180, 50)
    dd_dir = ddr.DropDown(360, 320, 180, 50)

    # Variable to carry message to be sent through UDP
    message = ''

    # Create object for class Sequence
    seq = sequence.Sequence(screen)

    # Run DataRec.exe
    subprocess.Popen(r'D:\TohokuUniversity\BCI-task\BCI-tools\gUSBamp\DataRec\DataRec\bin\x64\Debug\DataRec.exe',shell=False)

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
                    seq.vertical_test()

                elif event.button == 1 and button_run.isOver(pos) and \
                        dd_mode.active_list1 and dd_dir.active_list2:
                    seq.horizontal_test()

                elif event.button == 1 and button_run.isOver(pos) and \
                        dd_mode.active_list2 and dd_dir.active_list1:
                    seq.vertical_cal()

                elif event.button == 1 and button_run.isOver(pos) and \
                        dd_mode.active_list2 and dd_dir.active_list2:
                    seq.horizontal_cal()

                elif event.button == 1 and button_udp.isOver(pos):
                    print(message)
                    sock = socket.socket(socket.AF_INET,  # Internet
                                         socket.SOCK_DGRAM)  # UDP

                    # Sending command by UDP
                    sock.sendto(bytes(message, 'utf-8'), (UDP_IP, UDP_PORT))

        '''
        received_data = [T/O] + [Su] + [S] + [R] + [D] + [L] + [t]
                  0      1,2    3     4     5     6     7
        [T/R/O/F]: Training (Relax) / Online Test (Feedback)
        [Su]: Number of subject 00, 01, 02, ..., 99
        [S]:  Number of session 0, 1, ..., 9
        [R]:  Number of run 0, 1, ..., 9
        [L]:  Label of task 0, 1, 2
        [t]:  Number of trial during a run 0, 1, ..., 9
        
        The duration isn't included in the message
        '''
        message = 'T' + input_subno.text2UDP + input_noses.text2UDP + input_norun.text2UDP + '1' + '7'

        screen.fill((30, 30, 30))
        sequence.text_disp("Subject No.: ", screen, 80, 80)
        sequence.text_disp("Session No.: ", screen, 80, 120)
        sequence.text_disp("Run No.      : ", screen, 80, 160)
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
        button_run.draw(screen)
        button_trn.draw(screen)
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