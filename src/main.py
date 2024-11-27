#!/usr/bin/env python


#############################################################
### IMPORTS
#############################################################
from camera import Camera
import constants
import engine
from networking.dino_rush_client import DinoRushClient
from world.game_world import GameWorld

import pygame
import time


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
    client = DinoRushClient(constants.SERVER_CONNECTION_INFO, world)
    client.connect_to_server()
    player = None
    while (player is None):
        DinoRushClient.handle_message(client, time.time())
        player = client.CONNECTION_DATA["player"]
    # end while
    __CAMERA = Camera(__SCREEN, player._rect, world)
    ###################################################################

    __GAME_IS_RUNNING = True
    while __GAME_IS_RUNNING:
        current_time = time.time()

        events = pygame.event.get()

        for event in events:
            if (event.type == pygame.QUIT):
                __GAME_IS_RUNNING = False
            # end if
        # end for

        pressed_keys = engine.get_pressed_keys_codes(
            PYGAME_KEYS_TO_SERVER_CODES_MAP, pygame.key.get_pressed())

        world.update()
        player.update(pressed_keys, current_time)
        engine.handle_collisions(player, world)

        DinoRushClient.handle_message(client, current_time)
        client.send_player_data_to_server(pressed_keys)

        __CAMERA.update(player._rect)

        __SCREEN.fill(constants.COLOR_BLACK)

        world.draw_background(__SCREEN, __CAMERA)
        player.draw(__SCREEN, __CAMERA)
        for other_player in client.OTHER_PLAYERS.values():
            other_player.draw(__SCREEN, __CAMERA, current_time, True)
        # end for
        world.draw_foreground(__SCREEN, __CAMERA)

        # draw_hitboxes(__SCREEN, __CAMERA, world, player)

        pygame.display.flip()
        __CLOCK.tick(constants.FPS)
    # end while

    pygame.quit()
# end if