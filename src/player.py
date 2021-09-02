import pygame

from dinorush import collision_test
from src.map import tile_rects
from src.constants import *


#players = []

sprint_velocity = 0

this_player_img = pygame.image.load('assets/animations/jump/jump_0.png')
width = this_player_img.get_width()
height = this_player_img.get_height()
this_player_img = pygame.transform.scale(this_player_img, (width * 3, height * 3))

this_player_moving_right = False
this_player_moving_left = False

this_player_air_timer = 0

this_player_location = [0,0]
this_player_y_momentum = 0

this_player_rect = pygame.Rect(this_player_location[0],
                               this_player_location[1],
                               this_player_img.get_width(),
                               this_player_img.get_height())


def this_player_move():
    global this_player_y_momentum, this_player_air_timer

    collision_types = {'top':False,'bottom':False,'right':False,'left':False}

    if (this_player_y_momentum > 18):
        this_player_y_momentum = 18
    # end if

    movement = [0,this_player_y_momentum]
    if (this_player_moving_right and this_player_rect.x + this_player_rect.width < WINDOW_SIZE[0]):
        movement[0] = PLAYER_VELOCITY + sprint_velocity
    if (this_player_moving_left and this_player_rect.x > 0):
        movement[0] = -PLAYER_VELOCITY - sprint_velocity
    # end if


    this_player_rect.x += movement[0]
    hit_list = collision_test(this_player_rect, tile_rects)
    for tile in hit_list:
        if (movement[0] > 0):
            this_player_rect.right = tile.left
            collision_types['right'] = True
        elif (movement[0] < 0):
            this_player_rect.left = tile.right
            collision_types['left'] = True
        # end if
    # end for

    this_player_rect.y += movement[1]
    this_player_air_timer += 1
    hit_list = collision_test(this_player_rect, tile_rects)
    for tile in hit_list:
        if (movement[1] > 0):
            this_player_rect.bottom = tile.top
            collision_types['bottom'] = True
            this_player_y_momentum = 0
            this_player_air_timer = 0
        elif (movement[1] < 0):
            this_player_rect.top = tile.bottom
            collision_types['top'] = True
            this_player_y_momentum = 0
        # end if
    # end for

    return collision_types
# end move

def draw_player(screen):
    screen.blit(this_player_img, this_player_location)
# end draw_player