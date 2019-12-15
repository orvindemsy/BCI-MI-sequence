import pygame as pg
from colors import *

pg.init()
clock = pg.time.Clock()
# Generating screen
w_scr = 640
h_scr = 480
size_scr = (w_scr, h_scr)
screen = pg.display.set_mode(size_scr)
pg.display.set_caption("BCI Motor Imagery Test")

# Define color
COLOR_MAIN_INACTIVE = orange
COLOR_MAIN_ACTIVE = light_orange
COLOR_LIST_INACTIVE = (160, 160, 160)
COLOR_LIST_ACTIVE = (255, 210, 170)

# font declaration
font = pg.font.Font(None, 30)

class DropDown():
    # Test List
    def __init__(self, x, y, w, h):
        self.rect_main = pg.Rect(x, y, w, h)
        self.rect_list1 = pg.Rect(x, y + h, w, h)
        self.rect_list2 = pg.Rect(x, y + 2*h, w, h)
        self.active_main = True
        self.active_list1 = False
        self.active_list2 = False
        self.color_main = COLOR_MAIN_INACTIVE
        self.color_list = COLOR_LIST_INACTIVE
        self.text_main = 'Select Mode'
        self.main_surface = font.render(self.text_main, True, black)
        self.list1_surface = font.render('Test', True, black)
        self.list2_surface = font.render('Calibration', True, black)


    def handle_event(self, event):
        # Mouse hovering to default select mode button changes the color
        if event.type == pg.MOUSEMOTION:
            if self.rect_main.collidepoint(event.pos):
                self.color_main = COLOR_MAIN_ACTIVE
            else:
                self.color_main = COLOR_MAIN_INACTIVE

        # Clicking the default select mode button will trigger option list
        if event.type == pg.MOUSEBUTTONDOWN:
            # Default condition
            if (self.active_main and not self.active_list1) or (self.active_main and not self.active_list2):
                if self.rect_main.collidepoint(event.pos):
                    self.active_main = False
                    self.active_list1 = True
                    self.active_list2 = True
                    # print("Self.active_main: " + str(self.active_main) + "  Self.active.list1: " + str(
                    #     self.active_list1) + "  Self.active.list2: " + str(self.active_list1))

            # During the option list active status
            if not self.active_main and self.active_list1 and self.active_list2:
                if self.rect_list1.collidepoint(event.pos):
                    # Select test mode
                    print("Test")
                    self.active_main = True
                    self.active_list1 = True
                    self.active_list2 = False

                elif self.rect_list2.collidepoint(event.pos):
                    # Select calibration mode
                    print("Calibration")
                    self.active_main = True
                    self.active_list1 = False
                    self.active_list2 = True

                else:
                    # Default condition
                    print("hey")
                    self.active_main = False
                    self.active_list1 = True
                    self.active_list2 = True

            # else:
            #     self.active_main = True
            #     self.active_list1 = False
            #     self.active_list2 = False
            #     print("ea Self.active_main and: " + str(self.active_main) + "  Self.active.list: " + str(self.active_list1))


    def draw(self):
        # This method draw the drop down menu
        pg.draw.rect(screen, self.color_main, self.rect_main, 0)
        if self.active_main and self.active_list1 and not self.active_list2:
            # Draw test mode to main selection box
            screen.blit(self.list1_surface, (self.rect_main.x + (self.rect_main.w/2 - self.list1_surface.get_width()/ 2),
                                            self.rect_main.y + (self.rect_main.h/2 - self.list1_surface.get_height()/ 2)))

        elif self.active_main and not self.active_list1 and self.active_list2:
            # Draw calibration mode to calibration box
            screen.blit(self.list2_surface, (self.rect_main.x + (self.rect_main.w/2 - self.list2_surface.get_width()/ 2),
                                            self.rect_main.y + (self.rect_main.h/2 - self.list2_surface.get_height()/ 2)))

        else:
            # Draw default select mode
            screen.blit(self.main_surface, (self.rect_main.x + (self.rect_main.w/2 - self.main_surface.get_width()/ 2),
                                            self.rect_main.y + (self.rect_main.h/2 - self.main_surface.get_height()/ 2)))

    def option(self):
        # If dropdown list condition is satisfied, show these options
        if not self.active_main and self.active_list1 and self.active_list2:
            # Drawing the test mode
            pg.draw.rect(screen, self.color_list, self.rect_list1, 0)
            # Drawing the button outline
            pg.draw.rect(screen, gray, (self.rect_list1.x, self.rect_list1.y, self.rect_list1.w, self.rect_list1.h -1), 2)
            screen.blit(self.list1_surface, (self.rect_list1.x + (self.rect_list1.w/2 - self.list1_surface.get_width()/ 2),
                                            self.rect_list1.y + (self.rect_list1.h/2 - self.list1_surface.get_height()/ 2)))

            # Drawing the calibration mode
            pg.draw.rect(screen, self.color_list, self.rect_list2, 0)
            # Drawing the button outline
            pg.draw.rect(screen, gray, (self.rect_list2.x, self.rect_list2.y, self.rect_list2.w, self.rect_list2.h), 2)
            screen.blit(self.list2_surface, (self.rect_list2.x + (self.rect_list2.w/2 - self.list2_surface.get_width()/ 2),
                                            self.rect_list2.y + (self.rect_list2.h/2 - self.list2_surface.get_height()/ 2)))



    def handle_option(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.active_main == False and self.active_list1 == True and self.active_list2 == True:
                if self.rect_list1.collidepoint(event.pos):
                    print("Test")
                elif self.rect_list2.collidepoint(event.pos):
                    print("Calibration")
                    screen.blit(self.list2_surface, (self.rect_main.x + 5, self.rect_main.y + 5))
                else:
                    print("hey")



'''
# Declare element
list1 = DropDown(50, 50, 200, 50)

# Run program

menu = True
while menu:

    screen.fill((255, 255, 255))

    for event in pg.event.get():
        pos = pg.mouse.get_pos()

        if event.type == pg.QUIT:
            pg.quit()
            quit()

        list1.handle_event(event)
        # list1.handle_option(event)

    list1.option()
    list1.draw()
    pg.display.flip()
    clock.tick(30)


pg.quit()
'''