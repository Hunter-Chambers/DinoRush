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
    #############################################################################################
    SCREEN.blit(CloudsBack, (0,0))
    SCREEN.blit(CloudsFront, (0,0))
    SCREEN.blit(BGBack, (0,0))
    SCREEN.blit(BGFront, (0,0))
    SCREEN.blit(tree_2, (120,9))
    SCREEN.blit(tree_2, (1176,637))
    SCREEN.blit(tree_1, (381,444))
    #############################################################################################
    draw_map(SCREEN, list(game_map.keys()))
    pygame.display.flip()
# end draw


##################################################################
### game loop
##################################################################
if __name__ == "__main__":
    pygame.init()

    pygame.display.set_caption('Dino Rush!')
    pygame.display.set_icon(pygame.image.load('assets/title_icon.png'))

    SCREEN = pygame.display.set_mode(WINDOW_SIZE)
    CLOCK = pygame.time.Clock()

    BG_COLOR = pygame.Color('black')

    #############################################################################################
    BGBack = pygame.transform.scale(pygame.image.load('assets/BGBack.png'), WINDOW_SIZE)
    BGFront = pygame.transform.scale(pygame.image.load('assets/BGFront.png'), WINDOW_SIZE)
    CloudsBack = pygame.transform.scale(pygame.image.load('assets/CloudsBack.png'), WINDOW_SIZE)
    CloudsFront = pygame.transform.scale(pygame.image.load('assets/CloudsFront.png'), WINDOW_SIZE)
    tree_1 = pygame.transform.scale(pygame.image.load('assets/tree_1.png'), (186,324))
    tree_2 = pygame.transform.scale(pygame.image.load('assets/tree_2.png'), (171,231))
    #############################################################################################

    load_map('map1.txt')

    while True:
        handle_events()
        update()
        draw()
    # end while

# end if