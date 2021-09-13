import pygame
from pygame.locals import *

import socket
import json

from src import constants


class Player:

    ####################################################
    ### CONSTRUCTOR
    ####################################################
    def __init__(self, player_id, dino_color, starting_location, send_port):
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__connection.settimeout(1)
        self.__send_port = send_port

        img_path = dino_color + '/jump/jump_0.png'

        ########################################################
        # NOTE:
        # maybe load all possible images
        self.__img = pygame.image.load('assets/animations/' + img_path)
        self.__img = pygame.transform.scale(self.__img, (45, 54))
        ########################################################

        self.__id = player_id
        self.__moving_right = False
        self.__moving_left = False
        self.__sprinting = False
        self.__jumping = False
        self.__air_timer = 0
        self.__location = starting_location
        self.__y_momentum = 0

        self.__hitbox = pygame.Rect(self.__location[0],
                                  self.__location[1],
                                  45, 54)
    # end init


    ####################################################
    ### GETTERS
    ####################################################
    def get_id(self):
        return self.__id
    # end get_id


    ####################################################
    ### INSTANCE METHODS
    ####################################################
    def move(self, tile_rects):
        if (self.__y_momentum > 18):
            self.__y_momentum = 18
        # end if

        movement = [0, self.__y_momentum]
        if (self.__moving_right and self.__hitbox.x + self.__hitbox.width < constants.WINDOW_SIZE[0]):
            movement[0] = constants.PLAYER_VELOCITY
            if (self.__sprinting):
                movement[0] += constants.SPRINT_VELOCITY
            # end if
        if (self.__moving_left and self.__hitbox.x > 0):
            movement[0] = -constants.PLAYER_VELOCITY
            if (self.__sprinting):
                movement[0] -= constants.SPRINT_VELOCITY
            # end if
        # end if

        self.__hitbox.x += movement[0]
        hit_list = Player.collision_test(self.__hitbox, tile_rects)
        for tile in hit_list:
            if (movement[0] > 0):
                self.__hitbox.right = tile.left
            elif (movement[0] < 0):
                self.__hitbox.left = tile.right
            # end if
        # end for

        self.__hitbox.y += movement[1]
        self.__air_timer += 1
        hit_list = Player.collision_test(self.__hitbox, tile_rects)
        for tile in hit_list:
            if (movement[1] > 0):
                self.__hitbox.bottom = tile.top
                self.__y_momentum = 0
                self.__air_timer = 0
                self.__jumping = False
            elif (movement[1] < 0):
                self.__hitbox.top = tile.bottom
                self.__y_momentum = 0
            # end if
        # end for
    # end move

    def update(self, tile_rects):
        self.__y_momentum += 0.5
        self.move(tile_rects)

        self.__location[0] = self.__hitbox.x
        self.__location[1] = self.__hitbox.y

        self.__send()
    # end update

    def handle_events(self, events):
        for event in events:
            if (event.type == pygame.KEYDOWN):
                if (event.key == K_d):
                    self.__moving_right = True
                elif (event.key == K_a):
                    self.__moving_left = True
                elif (event.key == K_SPACE and self.__air_timer < 6):
                    self.__jumping = True
                    self.__y_momentum = -14
                elif (event.key == K_LSHIFT and self.__air_timer < 6):
                    self.__sprinting = True
                # end if
            elif (event.type == pygame.KEYUP):
                if (event.key == K_d):
                    self.__moving_right = False
                elif (event.key == K_a):
                    self.__moving_left = False
                elif (event.key == K_LSHIFT):
                    self.__sprinting = False
                # end if
            # end if
        # end for
    # end handle_events

    def draw(self, screen):
        screen.blit(self.__img, self.__location)
    # end draw


    ####################################################
    ### CONNECTION METHODS
    ####################################################
    def __send(self):
        # NOTE:
        # still need to append to this clients messages
        message = json.dumps({
            socket.gethostbyname(socket.gethostname()):{
                'moving_right':self.__moving_right,
                'moving_left':self.__moving_left,
                'sprinting':self.__sprinting,
                'jumping':self.__jumping
            }
        }).encode()

        self.__connection.sendto(message, (constants.SERVER, self.__send_port))
    # end send


    ####################################################
    ### CLASS METHODS
    ####################################################
    def collision_test(hitbox, tiles):
        hit_list = []

        for tile in tiles:
            if (hitbox.colliderect(tile)):
                hit_list.append(tile)
            # end if
        # end for

        return hit_list
    # end collision_test
# end Player class