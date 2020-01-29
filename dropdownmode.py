import pygame as pg
from colors import *

pg.init()
# clock = pg.time.Clock()
# # Generating screen
# w_scr = 640
# h_scr = 480
# size_scr = (w_scr, h_scr)
# screen = pg.display.set_mode(size_scr)
# pg.display.set_caption("Classical BCI GUI")

# Define color
COLOR_MAIN_INACTIVE = orange
COLOR_MAIN_ACTIVE = light_orange
COLOR_LIST_INACTIVE = (160, 160, 160)
# COLOR_LIST_ACTIVE = (255, 210, 170)

# font declaration
font = pg.font.Font(None, 30)

class DropDown():
    # Test List
    def __init__(self, x, y, w, h, screen):
        self.rect_main = pg.Rect(x, y, w, h) # True is the initial condition of main, main refers to "Select Mode"
        self.rect_list1 = pg.Rect(x, y + h, w, h) # False is the initial condition of list1, list1 refers to "Test"
        self.rect_list2 = pg.Rect(x, y + 2*h, w, h) # False is the initial condition of list1, list1 refers to "Calibration"
        self.screen = screen;
        self.active_main = True
        self.active_list1 = False
        self.active_list2 = False
        self.color_main = COLOR_MAIN_INACTIVE
        self.color_list = COLOR_LIST_INACTIVE
        self.main_surface = font.render('Select Mode', True, black)
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
            # If button is clicked within the area of 'Select Mode', then change respective values to:
            if self.rect_main.collidepoint(event.pos):
                self.active_main = False
                self.active_list1 = True
                self.active_list2 = True

            # When the active main is False, or when the 'Select Mode' is pressed once
            if not self.active_main and self.active_list1 and self.active_list2:
                if self.rect_list1.collidepoint(event.pos):
                    # Select 'Test', change respective value to
                    print("Test")
                    self.active_main = True
                    self.active_list1 = True
                    self.active_list2 = False

                elif self.rect_list2.collidepoint(event.pos):
                    # Select 'Calibration', change respective value to
                    print("Calibration")
                    self.active_main = True
                    self.active_list1 = False
                    self.active_list2 = True

    # This function is responsible for drawing either 'Test' or 'Calibration' on the main selection replacing
    # 'Select Mode' if pressed
    def draw(self):
        # This method draw the main rectangle button
        pg.draw.rect(self.screen, self.color_main, self.rect_main, 0)
        if self.active_main and self.active_list1 and not self.active_list2:
            # If list1 'vertical' is selected, draw vertical to main selection box
            self.screen.blit(self.list1_surface, (self.rect_main.x + (self.rect_main.w/2 - self.list1_surface.get_width()/ 2),
                                            self.rect_main.y + (self.rect_main.h/2 - self.list1_surface.get_height()/ 2)))

        elif self.active_main and not self.active_list1 and self.active_list2:
            # If list2 'horizontal' is selected, draw horizontal to main selection box
            self.screen.blit(self.list2_surface, (self.rect_main.x + (self.rect_main.w/2 - self.list2_surface.get_width()/ 2),
                                            self.rect_main.y + (self.rect_main.h/2 - self.list2_surface.get_height()/ 2)))

        else:
            # Draw default 'Select Mode'
            self.screen.blit(self.main_surface, (self.rect_main.x + (self.rect_main.w/2 - self.main_surface.get_width()/ 2),
                                            self.rect_main.y + (self.rect_main.h/2 - self.main_surface.get_height()/ 2)))

    # This function is responsible for drawing both options when 'Select Direction' is clicked
    def option(self):
        # If main (select mode) is selected, then draw list1 (test) and list2 (calibration) on the screen
        if not self.active_main and self.active_list1 and self.active_list2:
            # Drawing the button list1 (test)
            pg.draw.rect(self.screen, self.color_list, self.rect_list1, 0)
            # Drawing the button outline for list1 and write 'Test'
            pg.draw.rect(self.screen, gray, (self.rect_list1.x, self.rect_list1.y, self.rect_list1.w, self.rect_list1.h -1), 2)
            self.screen.blit(self.list1_surface, (self.rect_list1.x + (self.rect_list1.w/2 - self.list1_surface.get_width()/ 2),
                                            self.rect_list1.y + (self.rect_list1.h/2 - self.list1_surface.get_height()/ 2)))

            # Drawing the button list1 (horizontal)
            pg.draw.rect(self.screen, self.color_list, self.rect_list2, 0)

            # Drawing the button outline for list2 and write 'Horizontal'
            pg.draw.rect(self.screen, gray, (self.rect_list2.x, self.rect_list2.y, self.rect_list2.w, self.rect_list2.h), 2)
            self.screen.blit(self.list2_surface, (self.rect_list2.x + (self.rect_list2.w/2 - self.list2_surface.get_width()/ 2),
                                            self.rect_list2.y + (self.rect_list2.h/2 - self.list2_surface.get_height()/ 2)))



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