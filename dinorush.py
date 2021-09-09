#!/usr/bin/env python


import pygame
from pygame.locals import *

import sys
from src import constants, game_map, menus, player


##################################################################
### game loop
##################################################################
if __name__ == "__main__":
    pygame.init()

    pygame.display.set_caption('Dino Rush!')
    pygame.display.set_icon(pygame.image.load('assets/imgs/title_icon.png'))

    level = game_map.Game_Map('main_menu_map.txt')
    main_menu = menus.Main_Menu()

    while True:
        while (main_menu.get_at_main_menu()):
            events = pygame.event.get()

            for event in events:
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
            # end for

            main_menu.handle_events(events)

            constants.SCREEN.fill(constants.BG_COLOR)
            level.draw()
            main_menu.draw()
            pygame.display.flip()
            constants.CLOCK.tick(60)
        # end while

        ##################################################################
        level = game_map.Game_Map('main_menu_map.txt')
        character = player.Player('jump/jump_0.png', 3)
        character.set_id(main_menu.get_connection_return_message())
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
            character.draw()
            pygame.display.flip()
            constants.CLOCK.tick(60)
        # end while
    # end while
# end if