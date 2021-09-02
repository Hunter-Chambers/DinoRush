#!/usr/bin/env python


import sys
import pygame
from pygame.locals import *

from src.map import *
from src.constants import *
from src import player


##################################################################
### engine functions
##################################################################
def handle_events():
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            sys.exit()
        elif (event.type == pygame.KEYDOWN):
            if (event.key == K_d):
                player.this_player_moving_right = True
            elif (event.key == K_a):
                player.this_player_moving_left = True
            elif (event.key == K_SPACE and player.this_player_air_timer < 6):
                player.this_player_y_momentum = -14
            elif (event.key == K_LSHIFT and player.this_player_air_timer < 6):
                player.sprint_velocity = 3
            # end if
        elif (event.type == pygame.KEYUP):
            if (event.key == K_d):
                player.this_player_moving_right = False
            elif (event.key == K_a):
                player.this_player_moving_left = False
            elif (event.key == K_LSHIFT):
                player.sprint_velocity = 0
            # end if
        # end if
    # end for
# end handle_events

def update():
    player.this_player_y_momentum += 0.5
    player.this_player_location[1] += player.this_player_y_momentum
    player.this_player_location[0] = player.this_player_rect.x
    player.this_player_location[1] = player.this_player_rect.y
    player.this_player_move()
# end update

def draw():
    SCREEN.fill(BG_COLOR)
    draw_map(SCREEN)
    '''
    ##################################################################
    for rect in tile_rects:
        pygame.draw.rect(SCREEN, (255,0,0), rect, 3)
    pygame.draw.rect(SCREEN, (0,0,255), player.this_player_rect, 3)
    ##################################################################
    '''
    player.draw_player(SCREEN)
    pygame.display.flip()
# end draw


##################################################################
### calculation functions
##################################################################
def collision_test(rect, tiles):
    hit_list = []

    for tile in tiles:
        if (rect.colliderect(tile)):
            hit_list.append(tile)
        # end if
    # end for

    return hit_list
# end collision_test


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
        CLOCK.tick(60)
    # end while

# end if