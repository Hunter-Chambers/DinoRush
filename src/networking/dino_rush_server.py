#!/usr/bin/env python


#############################################################
### IMPORTS
#############################################################
import constants
import engine
from networking.server import Server
from player.dino_rush_player import DinoRushPlayer
from world.game_world import GameWorld

import pickle
import pygame
import time


#############################
# TODO: DELETE THESE LATER
player_scale = 3
player_character = "doux"
player_positions = [(912, 613), (0, 0)]
next_player_id = 0

world = GameWorld("test_world_01", True)
#############################


class DinoRushServer(Server):
    def __init__(self):
        super().__init__()
        # self.CLIENTS looks like:
        # {
        #     (<client_ip>, <port>): {
        #         # <player> will be the state of the player on this machine.
        #         # i.e. it references the client-side player when on the client
        #         # and the server-side player when on the server
        #
        #         "player": <player>,
        #         "recv_buffer_window": {
        #             "next_msg_num": <next expected message sequence number>,
        #             "buffer": {
        #                 <received buffered message sequence number>: <message>,
        #                 ...
        #             }
        #         },
        #         "sent_buffer_window": {
        #             "next_ack_num": <next expected acknowlegdement number>,
        #             "buffer": {
        #                 <sent buffered message sequence number>: <message>,
        #                 ...
        #             }
        #         }
        #     },
        #     ...
        # }
    # end __init__

    def create_player(self, addr, current_time, _):
        global next_player_id, player_scale, player_character, player_positions

        player_id = next_player_id
        next_player_id += 1

        player = DinoRushPlayer(
            player_character, player_scale, *player_positions[player_id],
            player_id, last_update_timestamp=current_time,
            loading_on_server=True)

        self.CLIENTS[addr] = {
            "player": player,
            "recv_buffer_window": {
                "next_msg_num": 0,
                "buffer": {}
            },
            "sent_buffer_window": {
                "next_ack_num": 0,
                "buffer": {}
            }
        }

        player_data = player.get_serializable_data()
        player_data["INITIAL_CONNECTION"] = True
        player_data["next_msg_num"] = self.LAST_MSG_ID_SENT
        self.get_socket().sendto(pickle.dumps(player_data), addr)

        print(f"[DinoRush Server] --- [INFO] --- created connection to client {addr}...")
    # end create_player

    def process_player_data(self, addr, player_data, current_time):
        global world
        pressed_keys = player_data["player_data"]["pressed_keys"]
        player = self.CLIENTS[addr]["player"]
        player.update(pressed_keys, current_time)
        engine.handle_collisions(player, world)
    # end process_player_data

    def start(self):
        clock = pygame.time.Clock()

        while (self.RUNNING):
            try:
                current_time = time.time()

                world.update()

                DinoRushServer.handle_message(self, current_time)
                self.send_all_player_data_to_all_clients()

                clock.tick(constants.FPS)
            except KeyboardInterrupt:
                self.RUNNING = False
            # end try/except
        # end while
    # end start
# end DinoRushServer class


if (__name__ == "__main__"):
    server = DinoRushServer()
    print(f"[DinoRush Server] --- [INFO] --- listening for messages on port {constants.SERVER_CONNECTION_INFO[1]}...")
    server.start()
    server.close()
# end if