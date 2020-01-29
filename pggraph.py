'''
Creating graphic that is compatible with pygame module
'''

import pygame as pg

def arrow_right(screen, color):
    screen_rect = screen.get_rect()
    pg.draw.rect(screen, color, (screen_rect.width/2 - screen_rect.width/4, screen_rect.height/4 + 80, 200, 80))
    pg.draw.polygon(screen, color, ((screen_rect.width/2 + 40, screen_rect.height/2 - 80),
                                        (screen_rect.width/2 + 40, screen_rect.height/2 + 80),
                                        (screen_rect.width/2 + 150, screen_rect.height/2 + 5)))

def arrow_left(screen, color):
    screen_rect = screen.get_rect()
    pg.draw.rect(screen, color, (screen_rect.width/2 + screen_rect.width/4, screen_rect.height/4 + 80, -200, 80))
    pg.draw.polygon(screen, color, ((screen_rect.width/2 - 40, screen_rect.height/2 - 80),
                                        (screen_rect.width/2 - 40, screen_rect.height/2 + 80),
                                        (screen_rect.width/2 - 150, screen_rect.height/2 + 5)))

def arrow_up(screen, color):
    screen_rect = screen.get_rect()
    pg.draw.rect(screen, color, (screen_rect.width / 2 - 30, screen_rect.height / 2.5, 80, 200))
    pg.draw.polygon(screen, color, ((screen_rect.width / 2 - 80, screen_rect.height / 2.5),
                                        (screen_rect.width / 2 + 100, screen_rect.height / 2.5),
                                        (screen_rect.width / 2, screen_rect.height / 2 - 150)))

def arrow_down(screen, color):
    screen_rect = screen.get_rect()
    pg.draw.rect(screen, color, (screen_rect.width / 2 - 30, screen_rect.height/4.5, 80, 200))
    pg.draw.polygon(screen, color, ((screen_rect.width / 2 - 80, screen_rect.height / 2 + 50),
                                        (screen_rect.width / 2 + 100, screen_rect.height / 2 + 50),
                                        (screen_rect.width / 2 + 5, screen_rect.height / 2 + 150)))

def fixation_cross(screen, color):
    screen_rect = screen.get_rect()
    pg.draw.rect(screen, color, (screen_rect.width / 2 - 60, screen_rect.height / 2, 45, 10))
    pg.draw.rect(screen, color, (screen_rect.width / 2 + 60, screen_rect.height / 2, -45, 10))
    pg.draw.rect(screen, color, (screen_rect.width / 2 - 5, screen_rect.height / 2 - 55, 10, 45))
    pg.draw.rect(screen, color, (screen_rect.width / 2 - 5, screen_rect.height / 2 + 65, 10, -45))

def horizontal_bar(screen, color, w, h):
    screen_rect = screen.get_rect()
    pg.draw.rect(screen, color, (screen_rect.width/2 - screen_rect.width/3,
                                     screen_rect.height/4 + 80,
                                     w, h))

def vertical_bar(screen, color, w, h):
    screen_rect = screen.get_rect()
    pg.draw.rect(screen, color, (screen_rect.width / 2 - 30,
                                     screen_rect.height/2 + 170,
                                     w, -h))