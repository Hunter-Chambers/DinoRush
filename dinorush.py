#!/usr/bin/env python


import sys
import pygame
from pygame.locals import *

from src.map import *
from src.constants import *


##################################################################
### functions
##################################################################
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
# end handle_events

def update():
    pass
# end update

def draw():
    SCREEN.fill(BG_COLOR)
    draw_map(SCREEN, list(game_map.keys()))
    '''
    ##################################################################
    for rect in tile_rects:
        pygame.draw.rect(SCREEN, (255,0,0), rect, 3)
    ##################################################################
    '''
    pygame.display.flip()
# end draw


##################################################################
### game loop
##################################################################
if __name__ == "__main__":
    pygame.init()

    pygame.display.set_caption('Dino Rush!')
    pygame.display.set_icon(pygame.image.load('assets/imgs/title_icon.png'))

    SCREEN = pygame.display.set_mode(WINDOW_SIZE)
    CLOCK = pygame.time.Clock()

    BG_COLOR = pygame.Color('black')

    load_map('map1.txt')

    while True:
        handle_events()
        update()
        draw()
    # end while

# end if