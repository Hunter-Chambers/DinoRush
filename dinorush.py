#!/usr/bin/env python


import pygame
from pygame.locals import *

import sys
from src import constants, game_map, menus, player


CLOCK = pygame.time.Clock()
BG_COLOR = pygame.Color('black')


##################################################################
### game loop
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

            connection_message = main_menu.handle_events(events, at_main_menu)

            SCREEN.fill(BG_COLOR)
            level.draw(SCREEN)
            main_menu.draw(SCREEN)
            pygame.display.flip()
            CLOCK.tick(60)
        # end while

        ##################################################################
        level = game_map.Game_Map('main_menu_map.txt')
        character = player.Player('jump/jump_0.png', 3)
        constants.id = main_menu.get_connection_return_message()
        main_menu.set_connection_return_message('')
        in_game = True
        ##################################################################

        while (in_game):
            events = pygame.event.get()

            for event in events:
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
            # end for

            character.handle_events(events)
            character.update(level.get_tile_rects())

            constants.SCREEN.fill(constants.BG_COLOR)
            level.draw()

            '''
            ##################################################################
            for rect in level.get_tile_rects():
                pygame.draw.rect(constants.SCREEN, (255,0,0), rect, 3)
            pygame.draw.rect(constants.SCREEN, (0,0,255), character.get_rect(), 3)
            ##################################################################
            '''

            for player_id in constants.players:
                #img = pygame.transform.scale(pygame.image.load('assets/animations/' + constants.players[player_id]['img']), constants.players[player_id]['size'])
                #constants.SCREEN.blit(img, constants.players[player_id]['location'])
                constants.SCREEN.blit(player.TEMP_TEST, constants.players[player_id]['location'])
            # end for

            character.draw()
            pygame.display.flip()
            constants.CLOCK.tick(60)
        # end while
    # end while
# end if