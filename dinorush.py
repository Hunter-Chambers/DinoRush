#!/usr/bin/env python


#############################################################
### IMPORTS
#############################################################
import pygame
from pygame.locals import *

import sys
# NOTE:
#import socket
#import json
#from threading import Thread

#from src import constants, game_map, menus, player
from src import constants, menus, game_map, menu_functions


#############################################################
### GLOBALS
#############################################################
SCREEN = None  # defined in setup
BG_COLOR = pygame.Color('black')
CLOCK = pygame.time.Clock()

# NOTE:
# note sure if I will keep active_threads.
# works best for now, though
ACTIVE_THREADS = []

# NOTE:
#LOOP = True
#players = {}
#character = None

#TEST_IMG = pygame.image.load('assets/animations/cyan/jump/jump_0.png')
#TEST_IMG = pygame.transform.scale(TEST_IMG, (45, 54))


'''
##################################################################
### RECV THREAD
##################################################################
def recv_thread(client_connection):
    # NOTE:
    # Need more logic still
    while (LOOP):
        try:
            msg, server = client_connection.recvfrom(constants.BUFFER_SIZE)
        except socket.timeout:
            continue
        # end try/except

        msg = json.loads(msg.decode())
        player_ids = list(msg.keys())[1:]

        for player_id in player_ids:
            if (player_id != character.get_id()):
                players[player_id] = msg[player_id]
            # end if
        # end for
    # end while

    client_connection.close()
# end recv_thread
'''


##################################################################
### PYGAME SETUP
##################################################################
pygame.init()
SCREEN = pygame.display.set_mode((constants.WINDOW_SIZE))
pygame.display.set_caption('Dino Rush!')
pygame.display.set_icon(pygame.image.load('assets/imgs/title_icon.png'))


##################################################################
### GAME LOOP
##################################################################
if __name__ == "__main__":
    # NOTE:
    #at_main_menu = True

    level = game_map.Game_Map('main_menu_map.txt')

    main_menu_extras = [[False, pygame.image.load('assets/imgs/Failed_to_connect.png'), (330, 700)],
                        [False, pygame.image.load('assets/imgs/Connecting.png'), (0, 0)]]
    main_menu = menus.Menu('main_options.png', [(545, 315), (460, 428), (575, 541)],
      [(menu_functions.connect_to_server, [main_menu_extras, level, SCREEN, BG_COLOR]), (menu_functions.empty_function,), (menu_functions.quit_game,)],
      None, True, main_menu_extras)

    while True:
        #while (at_main_menu):
        while (len(ACTIVE_THREADS) <= 0):
            events = pygame.event.get()

            for event in events:
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
            # end for

            # NOTE:
            #at_main_menu, connection_message = main_menu.handle_events(events)
            main_menu.handle_events(events)

            SCREEN.fill(BG_COLOR)
            level.draw(SCREEN)
            main_menu.draw(SCREEN)
            pygame.display.flip()
            CLOCK.tick(60)
        # end while

        '''
        ##################################################################
        level = game_map.Game_Map(connection_message['map_name'])
        character = player.Player(connection_message['player_id'], connection_message['player_color'], connection_message['position'], connection_message['send_port'])
        in_game = True
        client_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_connection.settimeout(1)
        client_connection.bind((socket.gethostbyname(socket.gethostname()), constants.RECV_PORT))
        new_thread = Thread(target=recv_thread, args=(client_connection,))
        ACTIVE_THREADS.append(new_thread)
        new_thread.start()
        ##################################################################

        while (in_game):
            events = pygame.event.get()

            for event in events:
                if (event.type == pygame.QUIT):
                    LOOP = False

                    for active_thread in ACTIVE_THREADS:
                        active_thread.join()
                    # end for

                    pygame.quit()
                    sys.exit()
            # end for

            character.handle_events(events)
            character.update(level.get_tile_rects())

            SCREEN.fill(BG_COLOR)
            level.draw(SCREEN)

            # NOTE:
            for player_id in players:
                SCREEN.blit(TEST_IMG, players[player_id])
            # end for

            character.draw(SCREEN)
            pygame.display.flip()
            CLOCK.tick(60)
        # end while
        '''
    # end while
# end if