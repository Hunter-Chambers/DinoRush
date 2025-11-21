#!/usr/bin/env python


#############################################################
### IMPORTS
#############################################################
import constants
import engine
from networking.dino_rush_client import DinoRushClient
from world.game_world import GameWorld

import pygame


##################################################################
### PYGAME SETUP
##################################################################
pygame.init()
pygame.display.set_caption(constants.GAME_TITLE)
pygame.display.set_icon(pygame.image.load(
    constants.BASE_PATH + '/assets/imgs/title_icon.png'))


##################################################################
### CLASS CONSTANTS
##################################################################
PYGAME_KEYS_TO_SERVER_CODES_MAP = {
    constants.LEFT: (pygame.K_a, pygame.K_LEFT),
    constants.DOWN: (pygame.K_s, pygame.K_DOWN),
    constants.RIGHT: (pygame.K_d, pygame.K_RIGHT),
    constants.JUMP: (pygame.K_SPACE,),
}


##################################################################
### GAME LOOP
##################################################################
if __name__ == "__main__":
    __CLOCK = pygame.time.Clock()
    __SCREEN = pygame.display.set_mode((constants.WINDOW_SIZE))

    ###################################################################
    world = GameWorld("test_world_01")
    client = DinoRushClient(world)
    client.send_message({"INITIAL_CONNECTION": True}, constants.SERVER_CONNECTION_INFO)
    ###################################################################

    __GAME_IS_RUNNING = True
    while (__GAME_IS_RUNNING):
        try:
            events = pygame.event.get()
            for event in events:
                if (event.type == pygame.QUIT):
                    __GAME_IS_RUNNING = False
                    client.send_message({"CLOSING_CONNECTION": True}, constants.SERVER_CONNECTION_INFO)
                    client.remove_client()
                # end if
            # end for

            client.process_messages()

            if (client.is_initialized()):
                pressed_keys = engine.get_pressed_keys_codes(
                    PYGAME_KEYS_TO_SERVER_CODES_MAP, pygame.key.get_pressed())

                client.process_input(pressed_keys)
                client.interpolate_entities()

                __SCREEN.fill(constants.COLOR_BLACK)

                client.draw(__SCREEN)

                pygame.display.flip()
            # end if

            __CLOCK.tick(constants.FPS)
        except (ConnectionResetError, KeyboardInterrupt):
            __GAME_IS_RUNNING = False
        # end try/except
    # end while

    client.save_last_used_port()
    client.close()
    pygame.quit()
# end if