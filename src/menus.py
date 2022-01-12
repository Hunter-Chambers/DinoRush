import pygame
from pygame.locals import *

from src import constants


class Cursor:

    ####################################################
    ### CONSTRUCTOR
    ####################################################
    def __init__(self, location):
        self.__img = pygame.image.load('assets/imgs/cursor.png')
        self.__location = location
    # end init


    ####################################################
    ### GETTERS
    ####################################################
    def get_location(self):
        return self.__location
    # end get_location


    ####################################################
    ### SETTERS
    ####################################################
    def set_location(self, new_location):
        self.__location = new_location
    # end set_location


    ####################################################
    ### INSTANCE METHODS
    ####################################################
    def draw(self, screen):
        screen.blit(self.__img, self.__location)
    # end draw
# end Cursor class


class Menu:

    ####################################################
    ### CONSTRUCTOR
    ####################################################
    def __init__(self, img, cursor_locations, functions, location=None, has_extras=False, extras=None):
        self.__option = 0
        self.__cursor_locations = cursor_locations

        self.__main_options_img = pygame.image.load('assets/imgs/' + img)

        if (location is None):
            main_options_rect = self.__main_options_img.get_rect()
            main_options_rect.center = constants.SCREEN_CENTER
            self.__location = (main_options_rect.x, main_options_rect.y)
        else:
            self.__location = location
        # end if

        self.__cursor = Cursor(self.__cursor_locations[self.__option])

        self.__functions = functions

        self.__has_extras = has_extras
        self.__extras = extras
    # end init


    ####################################################
    ### INSTANCE METHODS
    ####################################################
    def handle_events(self, events):
        for event in events:
            if (event.type == pygame.KEYDOWN):
                if (event.key == K_s or event.key == K_DOWN):
                    self.__option += 1

                    if (self.__option >= len(self.__cursor_locations)):
                        self.__option = 0
                    # end if

                    self.__cursor.set_location(self.__cursor_locations[self.__option])
                elif (event.key == K_w or event.key == K_UP):
                    self.__option -= 1

                    if (self.__option < 0):
                        self.__option = len(self.__cursor_locations) - 1
                    # end if

                    self.__cursor.set_location(self.__cursor_locations[self.__option])
                elif (event.key == K_SPACE or event.key == K_RETURN):
                    try:
                        self.__functions[self.__option][0](self.__functions[self.__option][1])
                    except IndexError:
                        self.__functions[self.__option][0]()
                    # end try/except
                # end if
            # end if
        # end for
    # end handle_events

    def draw(self, screen):
        screen.blit(self.__main_options_img, self.__location)
        self.__cursor.draw(screen)

        if (self.__has_extras):
            for extra in self.__extras:
                if extra[0]:
                    screen.blit(extra[1], extra[2])
                # end if
            # end for
        # end if
    # end draw
# end Main_Menu class