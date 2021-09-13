#!/usr/bin/env python


#############################################################
### IMPORTS
#############################################################
import pygame
from pygame.locals import *

import socket
import sys
import json
from threading import Thread

from src import constants, game_map, menus, player


#############################################################
### GLOBALS
#############################################################
CLOCK = pygame.time.Clock()
BG_COLOR = pygame.Color('black')

ACTIVE_THREADS = []
LOOP = True
players = {}
character = None

# NOTE:
TEST_IMG = pygame.image.load('assets/animations/cyan/jump/jump_0.png')
TEST_IMG = pygame.transform.scale(TEST_IMG, (45, 54))


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
                SCREEN.blit(TEST_IMG, msg[player_id])
            # end if
        # end for
    # end while

    client_connection.close()
# end recv_thread


##################################################################
### GAME LOOP
##################################################################
if __name__ == "__main__":
    pygame.init()

    SCREEN = pygame.display.set_mode((constants.WINDOW_SIZE))

    pygame.display.set_caption('Dino Rush!')
    pygame.display.set_icon(pygame.image.load('assets/imgs/title_icon.png'))

    level = game_map.Game_Map('main_menu_map.txt')
    main_menu = menus.Main_Menu()
    at_main_menu = True

    while True:
        while (at_main_menu):
            events = pygame.event.get()

            for event in events:
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
            # end for

            at_main_menu, connection_message = main_menu.handle_events(events)

            SCREEN.fill(BG_COLOR)
            level.draw(SCREEN)
            main_menu.draw(SCREEN)
            pygame.display.flip()
            CLOCK.tick(60)
        # end while

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

            '''
            for player_id in constants.players:
                #img = pygame.transform.scale(pygame.image.load('assets/animations/' + constants.players[player_id]['img']), constants.players[player_id]['size'])
                #constants.SCREEN.blit(img, constants.players[player_id]['location'])
                constants.SCREEN.blit(player.TEMP_TEST, constants.players[player_id]['location'])
            # end for
            '''

            character.draw(SCREEN)
            pygame.display.flip()
            CLOCK.tick(60)
        # end while
    # end while
# end if