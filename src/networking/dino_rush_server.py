#!/usr/bin/env python


#############################################################
### IMPORTS
#############################################################
import constants
from dino_rush_player import DinoRushPlayer
from networking.server import Server
from world.game_world import GameWorld


#############################
# TODO: DELETE THESE LATER
player_scale = 3
player_character = "doux"
player_positions = [(912, 613), (0, 0)]
next_player_id = 0

game_world = GameWorld("test_world_01", True)
#############################


class DinoRushServer(Server):
    def __init__(self, world):
        super().__init__(world)
    # end __init__

    def initialize_client(self, client, _):
        global next_player_id, player_character, player_scale, player_positions
        entity_id = next_player_id
        next_player_id += 1

        self.add_client(client, entity_id)

        sprite_id = player_character
        scale_factor = player_scale
        position = player_positions[entity_id]
        entity = DinoRushPlayer(
            sprite_id, scale_factor, *position, entity_id, True)
        self.add_entity(entity)

        entity_data = entity.get_serializable_data()
        entity_data["INITIAL_CONNECTION"] = True
        self.send_message(entity_data, client)
    # end initialize_client
# end DinoRushServer class


if (__name__ == "__main__"):
    server = DinoRushServer(game_world)
    print(f"[DinoRush Server] --- [INFO] --- listening for messages on port {constants.SERVER_CONNECTION_INFO[1]}...")
    server.start()
    print(f"[DinoRush Server] --- [INFO] --- closing...")
    server.close()
# end if