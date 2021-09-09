import pygame
from pygame.locals import *

from src import constants, engine


class Player:

    ####################################################
    ### CONSTRUCTOR
    ####################################################
    def __init__(self, img_path, img_scale):
        self.__img_path = img_path

        self.__img = pygame.image.load('assets/animations/' + img_path)
        self.__img = pygame.transform.scale(self.__img, (self.__img.get_width() * img_scale, self.__img.get_height() * img_scale))

        self.__moving_right = False
        self.__moving_left = False
        self.__sprint_vel = 0
        self.__air_timer = 0
        self.__location = [0,0]
        self.__y_momentum = 0

        self.__rect = pygame.Rect(self.__location[0],
                                  self.__location[1],
                                  self.__img.get_width(),
                                  self.__img.get_height())
    # end init


    ####################################################
    ### GETTERS
    ####################################################
    def get_rect(self):
        return self.__rect
    # end get_rect


    '''
    ####################################################
    ### SETTERS
    ####################################################
    def set_id(self, id):
        self.set_id = id
    # end set_id
    '''


    ####################################################
    ### INSTANCE METHODS
    ####################################################
    def move(self, tile_rects):
        if (self.__y_momentum > 18):
            self.__y_momentum = 18
        # end if

        movement = [0,self.__y_momentum]
        if (self.__moving_right and self.__rect.x + self.__rect.width < constants.WINDOW_SIZE[0]):
            movement[0] = constants.PLAYER_VELOCITY + self.__sprint_vel
        if (self.__moving_left and self.__rect.x > 0):
            movement[0] = -constants.PLAYER_VELOCITY - self.__sprint_vel
        # end if

        self.__rect.x += movement[0]
        hit_list = engine.collision_test(self.__rect, tile_rects)
        for tile in hit_list:
            if (movement[0] > 0):
                self.__rect.right = tile.left
            elif (movement[0] < 0):
                self.__rect.left = tile.right
            # end if
        # end for

        self.__rect.y += movement[1]
        self.__air_timer += 1
        hit_list = engine.collision_test(self.__rect, tile_rects)
        for tile in hit_list:
            if (movement[1] > 0):
                self.__rect.bottom = tile.top
                self.__y_momentum = 0
                self.__air_timer = 0
            elif (movement[1] < 0):
                self.__rect.top = tile.bottom
                self.__y_momentum = 0
            # end if
        # end for
    # end move

    def handle_events(self, events):
        for event in events:
            if (event.type == pygame.KEYDOWN):
                if (event.key == K_d):
                    self.__moving_right = True
                elif (event.key == K_a):
                    self.__moving_left = True
                elif (event.key == K_SPACE and self.__air_timer < 6):
                    self.__y_momentum = -14
                elif (event.key == K_LSHIFT and self.__air_timer < 6):
                    self.__sprint_vel = 3
                # end if
            elif (event.type == pygame.KEYUP):
                if (event.key == K_d):
                    self.__moving_right = False
                elif (event.key == K_a):
                    self.__moving_left = False
                elif (event.key == K_LSHIFT):
                    self.__sprint_vel = 0
                # end if
            # end if
        # end for
    # end handle_events

    def update(self, tile_rects):
        self.__y_momentum += 0.5
        self.move(tile_rects)
        self.__location[0] = self.__rect.x
        self.__location[1] = self.__rect.y

        constants.location = self.__location
        constants.img = self.__img_path
        constants.size = self.__rect.size
    # end update

    def draw(self):
        constants.SCREEN.blit(self.__img, self.__location)
    # end draw_player
# end Player class