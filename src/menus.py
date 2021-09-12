import pygame
from pygame.locals import *

import socket
import json
import sys

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
    def set_location(self, x=0, y=0):
        self.__location[0] = x
        self.__location[1] = y
    # end set_location


    ####################################################
    ### INSTANCE METHODS
    ####################################################
    def draw(self, screen):
        screen.blit(self.__img, self.__location)
    # end draw
# end Cursor class


class Main_Menu:

    ####################################################
    ### CONSTRUCTOR
    ####################################################
    def __init__(self):
        self.__option = 1

        self.__main_options_img = pygame.image.load('assets/imgs/main_options.png')
        main_options_rect = self.__main_options_img.get_rect()
        main_options_rect.center = constants.SCREEN_CENTER
        self.__location = (main_options_rect.x, main_options_rect.y)

        self.__cursor = Cursor([self.__location[0] - 20, self.__location[1] - 5])

        self.__error_occurred = False
        self.__failed_to_connect_img = pygame.image.load('assets/imgs/Failed_to_connect.png')
    # end init


    ####################################################
    ### INSTANCE METHODS
    ####################################################
    def handle_events(self, events, at_main_menu):
        for event in events:
            if (event.type == pygame.KEYDOWN):
                cursor_location = self.__cursor.get_location()

                if (event.key == K_s or event.key == K_DOWN):
                    if (self.__option == 1):
                        self.__cursor.set_location(cursor_location[0] - 85, cursor_location[1] + 113)
                        self.__option = 2
                    elif (self.__option == 2):
                        self.__cursor.set_location(cursor_location[0] + 115, cursor_location[1] + 113)
                        self.__option = 3
                    else:
                        self.__cursor.set_location(cursor_location[0] - 30, cursor_location[1] - 226)
                        self.__option = 1
                    # end if
                elif (event.key == K_w or event.key == K_UP):
                    if (self.__option == 1):
                        self.__cursor.set_location(cursor_location[0] + 30, cursor_location[1] + 226)
                        self.__option = 3
                    elif (self.__option == 2):
                        self.__cursor.set_location(cursor_location[0] + 85, cursor_location[1] - 113)
                        self.__option = 1
                    else:
                        self.__cursor.set_location(cursor_location[0] - 115, cursor_location[1] - 113)
                        self.__option = 2
                    # end if
                elif (event.key == K_SPACE or event.key == K_RETURN):
                    if (self.__option == 1):
                        '''
                        - attempt connection
                        '''

                        conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        try:
                            conn.sendto('initial connection'.encode(), (constants.SERVER, constants.PORT))
                            message, addr = conn.recvfrom(constants.BUFFER_SIZE)
                            message = message.decode()
                        except socket.error:
                            self.__error_occurred = True
                        # end try/except

                        pygame.event.clear()

                        #at_main_menu = False

                        print(json.loads(message))
                        return json.loads(message)
                    elif (self.__option == 2):
                        pass
                    else:
                        pygame.quit()
                        sys.exit()
                    # end if
                # end if
            # end if
        # end for
    # end handle_events

    def draw(self, screen):
        screen.blit(self.__main_options_img, self.__location)
        self.__cursor.draw(screen)
        if (self.__error_occurred):
            screen.blit(self.__failed_to_connect_img, self.__location)
        # end if
    # end draw
# end Main_Menu class